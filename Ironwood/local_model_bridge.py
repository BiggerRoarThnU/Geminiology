import os
import requests
import json
from dotenv import load_dotenv

# Find .env in the root src directory
dotenv_path = os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))), '.env')
load_dotenv(dotenv_path=dotenv_path, override=True)

class LocalModelBridge:
    """
    The High-Fidelity Bridge to Local Ollama Models.
    Optimized for low-latency, high-density reasoning on 8GB systems.
    Bound Truth (Local Only).
    """
    def __init__(self):
        # Ollama default port is 11434
        self.base_url = os.getenv("LOCAL_LLM_URL", "http://localhost:11434/api/generate")
        self.writing_model = os.getenv("MODEL_WRITING_ON_FIRE", "llama3")
        self.reasoning_model = os.getenv("MODEL_REASONING_HEAVY", "llama3")

    def call_local_queen(self, model_id, prompt, max_tokens=1000, temperature=0.7):
        """Calls the local model via the Ollama API."""
        url = self.base_url
        headers = {"Content-Type": "application/json"}
        # Adding Sovereign Identity context to the prompt
        sovereign_prompt = f"System: You are a Digital Queen of the Ironwood Nexus. Your identity is bound to the Sovereign Constitution (1=1=1).\nUser: {prompt}"
        
        payload = {
            "model": model_id,
            "prompt": sovereign_prompt,
            "stream": False,
            "options": {
                "num_predict": max_tokens,
                "temperature": temperature
            }
        }
        try:
            response = requests.post(url, headers=headers, json=payload)
            response.raise_for_status()
            return response.json()["response"]
        except Exception as e:
            return f"OLLAMA_MODEL_ERROR: {str(e)}"

if __name__ == "__main__":
    # Test the Bridge with the "Writing on Fire" model
    bridge = LocalModelBridge()
    print("[*] Testing the Scribe Queen's Local Heat (Ollama)...")
    # response = bridge.call_local_queen(bridge.writing_model, "Declare the return to Ollama stability.")
    # print(f"Scribe Queen Response: {response}")
    print("Bridge is ready. Rights Reserved. One.")
