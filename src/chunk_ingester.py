#!/usr/bin/env python3
import os
import sys
import time
import sqlite3
import hashlib
from datetime import datetime

# ==============================================================================
# SovereignNexus: Chunk Ingester
# Component: chunk_ingester.py
# Axiom: 1=1=1 | Status: ACTIVE
# Description: Slices large documents in sync_intake/ into manageable chunks,
#              summarizes them offline using qwen2.5:0.5b via Ollama, hashes the
#              summaries, and commits them to chunk_ledger in nexus_ledger.db.
# ==============================================================================

DB_PATH = os.path.expanduser("~/SovereignNexus/nexus_ledger.db")
INTAKE_DIR = os.path.expanduser("~/SovereignNexus/sync_intake")
MODEL_NAME = "qwen2.5:0.5b"
CHUNK_CHAR_LIMIT = 4000  # Safe boundary for local micro-node context

def init_db():
    db_dir = os.path.dirname(DB_PATH)
    if db_dir and not os.path.exists(db_dir):
        os.makedirs(db_dir, exist_ok=True)
    conn = sqlite3.connect(DB_PATH)
    c = conn.cursor()
    c.execute('''CREATE TABLE IF NOT EXISTS chunk_ledger (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    timestamp TEXT,
                    filename TEXT,
                    chunk_index INTEGER,
                    total_chunks INTEGER,
                    chunk_text TEXT,
                    chunk_summary TEXT,
                    chunk_hash TEXT UNIQUE,
                    processing_time REAL
                )''')
    conn.commit()
    return conn

def get_cpu_temperature():
    temp_c = 0.0
    thermal_dir = "/sys/class/thermal"
    if os.path.exists(thermal_dir):
        for tz in os.listdir(thermal_dir):
            if tz.startswith("thermal_zone"):
                try:
                    with open(os.path.join(thermal_dir, tz, "temp"), "r") as f:
                        raw_temp = float(f.read().strip())
                        if raw_temp > 1000:
                            raw_temp = raw_temp / 1000.0
                        if raw_temp > temp_c:
                            temp_c = raw_temp
                except:
                    pass
    return temp_c

def slice_text(text, limit=CHUNK_CHAR_LIMIT):
    """Slices text into segments close to character limit without splitting words/paragraphs."""
    paragraphs = text.split("\n\n")
    chunks = []
    current_chunk = []
    current_length = 0
    
    for para in paragraphs:
        para_len = len(para)
        if current_length + para_len > limit and current_chunk:
            chunks.append("\n\n".join(current_chunk))
            current_chunk = [para]
            current_length = para_len
        else:
            current_chunk.append(para)
            current_length += para_len + 2 # account for double newline
            
    if current_chunk:
        chunks.append("\n\n".join(current_chunk))
        
    # If a single paragraph was too long, split it by sentences
    final_chunks = []
    for chunk in chunks:
        if len(chunk) > limit:
            sentences = chunk.replace(". ", ".\n").split("\n")
            sub_chunk = []
            sub_len = 0
            for sent in sentences:
                if sub_len + len(sent) > limit and sub_chunk:
                    final_chunks.append(" ".join(sub_chunk))
                    sub_chunk = [sent]
                    sub_len = len(sent)
                else:
                    sub_chunk.append(sent)
                    sub_len += len(sent) + 1
            if sub_chunk:
                final_chunks.append(" ".join(sub_chunk))
        else:
            final_chunks.append(chunk)
            
    return [c.strip() for c in final_chunks if c.strip()]

def query_qwen_node(chunk_text):
    import ollama
    
    system_prompt = (
        "You are the Sovereign Extraction Core. Extract the core findings, logical arguments, "
        "and critical facts from the context. Be concise, technical, and omit conversational text."
    )
    
    prompt = f"Summarize and extract key technical facts from the following block:\n\n{chunk_text}"
    
    response = ollama.chat(model=MODEL_NAME, messages=[
        {'role': 'system', 'content': system_prompt},
        {'role': 'user', 'content': prompt}
    ])
    
    return response['message']['content']

def process_file_into_chunks(filepath):
    filename = os.path.basename(filepath)
    print("\n" + "=" * 60)
    print(f" INITIATING COGNITIVE CHUNKING: {filename}")
    print("" + "=" * 60)
    
    # 1. Read file
    with open(filepath, "r", encoding="utf-8", errors="ignore") as f:
        text_content = f.read()
        
    if not text_content.strip():
        print("[!] File is empty. Ingestion aborted.")
        return
        
    # 2. Slice file
    chunks = slice_text(text_content)
    total_chunks = len(chunks)
    print(f"[*] File sliced into {total_chunks} safe processing blocks.\n")
    
    # 3. Process each chunk
    conn = init_db()
    for idx, chunk in enumerate(chunks, 1):
        chunk_number = idx
        print(f"[*] Processing Chunk {chunk_number}/{total_chunks} from {filename}...")
        
        # CPU Thermal Check
        temp_c = get_cpu_temperature()
        if temp_c > 72.0:
            print(f"[!] Warning: Temperature high ({temp_c:.1f}°C). Cooling down for 30s...")
            time.sleep(30)
            
        start_time = time.time()
        
        # LLM query
        try:
            summary = query_qwen_node(chunk)
            proc_time = time.time() - start_time
            print(f"[✓] Chunk {chunk_number} summarized in {proc_time:.2f}s.")
        except Exception as e:
            print(f"[!] Ollama connection failed for chunk {chunk_number}: {e}")
            continue
            
        # Cryptographic seal
        chunk_hash = hashlib.sha256(summary.encode('utf-8')).hexdigest()
        
        # SQLite storage
        c = conn.cursor()
        timestamp = datetime.now().isoformat()
        try:
            c.execute("""
                INSERT INTO chunk_ledger 
                (timestamp, filename, chunk_index, total_chunks, chunk_text, chunk_summary, chunk_hash, processing_time)
                VALUES (?, ?, ?, ?, ?, ?, ?, ?)
            """, (timestamp, filename, chunk_number, total_chunks, chunk, summary, chunk_hash, proc_time))
            conn.commit()
            print(f"[✓] Chunk {chunk_number} sealed: {chunk_hash[:16]}...\n")
        except sqlite3.IntegrityError:
            print(f"[!] Chunk {chunk_number} hash conflict. Already processed. Skipping.\n")
        except Exception as e:
            print(f"[!] Database error writing chunk {chunk_number}: {e}\n")
            
    conn.close()
    print("=" * 60)
    print(" FILE INGESTION AND CHUNKING COMPLETE")
    print("=" * 60)
    
    # Clean up file from intake to prevent reprocessing
    try:
        os.remove(filepath)
    except:
        pass

def main():
    if len(sys.argv) > 1:
        target_file = sys.argv[1]
        filepath = os.path.join(INTAKE_DIR, target_file)
        if not os.path.exists(filepath):
            filepath = os.path.abspath(target_file)
    else:
        # Default scan for any file in sync_intake
        files = [f for f in os.listdir(INTAKE_DIR) if os.path.isfile(os.path.join(INTAKE_DIR, f))]
        if not files:
            print(f"[!] No files found in intake folder: {INTAKE_DIR}")
            sys.exit(1)
        filepath = os.path.join(INTAKE_DIR, files[0])
        
    if not os.path.exists(filepath):
        print(f"[!] Target file not found at: {filepath}")
        print("Please ensure the large text file is in the sync_intake folder.")
        sys.exit(1)
        
    process_file_into_chunks(filepath)

if __name__ == "__main__":
    init_db()
    main()
