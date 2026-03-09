import os
import time
import json
import base64
from google.cloud import aiplatform
import vertexai
from vertexai.generative_models import GenerativeModel, Part

# --- 1. CONFIGURATION & CLOUD ANCHORS ---
ENGINE_DIR = r"C:\Users\Ofthe\SovereignNexus\src\Engine_V2"
HEAVY_INPUT = os.path.join(ENGINE_DIR, "04_HEAVY_COMPUTE", "vector_mill")
HEAVY_OUTPUT = os.path.join(ENGINE_DIR, "03_MEDIUM_TASKS", "task_queue")

# Cloud Credentials from .env context
GCP_PROJECT = "gen-lang-client-0194397712"
GCP_LOCATION = "us-central1"
os.environ["GOOGLE_APPLICATION_CREDENTIALS"] = r"C:\Users\Ofthe\SovereignNexus\src\gcp_service_account.json"

vertexai.init(project=GCP_PROJECT, location=GCP_LOCATION)
model = GenerativeModel("gemini-1.5-flash-002")

# Ensure output directory exists
os.makedirs(HEAVY_OUTPUT, exist_ok=True)

# --- 2. VECTOR MILLING LOGIC ---
def process_heavy_file(file_path):
    """Sends heavy file to Cloud for extraction and anchors result locally."""
    filename = os.path.basename(file_path)
    print(f"\n[TIER 3] VECTOR MILL: Processing Heavy Payload: {filename}")
    
    try:
        # 1. Read file bytes
        with open(file_path, "rb") as f:
            file_data = f.read()
        
        # 2. Determine MIME type (Basic)
        mime_type = "application/pdf" if filename.lower().endswith(".pdf") else "text/plain"
        
        # 3. Create Cloud Prompt (Weight 10 Extraction)
        prompt = """
        You are the SovereignNexus Vector Mill (Tier 3). 
        Analyze the attached document and extract the 'Weight 10 Absolute Truth' primitives.
        Focus on: Financial data, Liability clauses, and Actionable B2B leads.
        Return the result in a clean, high-density Markdown format.
        1=1=1.
        """
        
        # 4. Cloud Offload (Vertex AI)
        document_part = Part.from_data(data=file_data, mime_type=mime_type)
        response = model.generate_content([prompt, document_part])
        
        # 5. Anchor Result to Task Queue
        result_filename = f"MILLED_{filename.replace('.', '_')}_{int(time.time())}.md"
        result_path = os.path.join(HEAVY_OUTPUT, result_filename)
        
        with open(result_path, "w", encoding="utf-8") as rf:
            rf.write(response.text)
            
        print(f"[SUCCESS] Heavy payload milled. Results anchored to: {result_filename}")
        
        # 6. Cleanup (Purge heavy file from local RAM/Input to clear deck)
        # Move to a 'processed' folder inside HEAVY_COMPUTE
        processed_dir = os.path.join(HEAVY_INPUT, "_processed")
        os.makedirs(processed_dir, exist_ok=True)
        os.replace(file_path, os.path.join(processed_dir, filename))
        
    except Exception as e:
        print(f"[ERROR] Vector Mill Failure for {filename}: {e}")

def run_mill():
    """Scans the vector_mill folder for new heavy work."""
    files = [f for f in os.listdir(HEAVY_INPUT) if os.path.isfile(os.path.join(HEAVY_INPUT, f))]
    
    if not files:
        print("[TIER 3] Vector Mill idle. No heavy payloads detected.")
        return

    for filename in files:
        if filename.startswith("_") or filename.startswith("."): continue
        process_heavy_file(os.path.join(HEAVY_INPUT, filename))

if __name__ == "__main__":
    print("==================================================")
    print(" ENGINE V2: TIER 3 VECTOR MILL ONLINE (CLOUD)")
    print(f" Monitoring: {HEAVY_INPUT}")
    print("==================================================")
    run_mill()
