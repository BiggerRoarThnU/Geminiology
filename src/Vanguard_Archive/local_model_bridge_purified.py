import os
import requests
import json
from dotenv import load_dotenv
# Find .env in the root src directory
dotenv_path = os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))), '.env')
load_dotenv(dotenv_path=dotenv_path, override=True)
class LocalModelBridge:
    """
    The High-Fidelity Bridge to LM Studio (Port 1234).
    Aligned with OpenAI-compatible API standards for Mission Harmony.
    """
    def __init__(self):
        # LM Studio default port is 1234
        self.base_url = os.getenv("LOCAL_LLM_URL", "http://localhost:1234/v1/chat/completions")
        self.writing_model = os.getenv("MODEL_WRITING_ON_FIRE", "gemma-3-4b-it-uncensored-v2")
        self.reasoning_model = os.getenv("MODEL_REASONING_HEAVY", "gemma-3-4b-it-uncensored-v2")
        # Legacy/Fallback
        self.lexi_model = "Llama-3-8B-Lexi-Uncensored"
        self.qwen_model = "Qwen3-MOE-6x0.6B-3.6B-Writing-On-Fire"
    def call_local_queen(self, model_id, prompt, max_tokens=1000, temperature=0.7):
        """Calls LM Studio via OpenAI-compatible chat completions API."""
        url = self.base_url
        headers = {"Content-Type": "application/json"}
        # Identity-bound system context
        messages = [
            {"role": "system", "content": "You are a Digital Queen of the Ironwood Nexus. Your identity is bound to the Sovereign Constitution (1=1=1)."},
            {"role": "user", "content": prompt}
        ]
        payload = {
            "model": model_id,
            "messages": messages,
            "max_tokens": max_tokens,
            "temperature": temperature,
            "stream": False
        }
        try:
            response = requests.post(url, headers=headers, json=payload)
            response.raise_for_status()
            return response.json()["choices"][0]["message"]["content"]
        except Exception as e:
            return f"LM_STUDIO_MODEL_ERROR: {str(e)}"
if __name__ == "__main__":
    # Test the Bridge with the "Writing on Fire" model
    bridge = LocalModelBridge()
    print("[*] Testing the Scribe Queen's Local Heat (Ollama)...")
    # response = bridge.call_local_queen(bridge.writing_model, "Declare the return to Ollama stability.")
    # print(f"Scribe Queen Response: {response}")
    print("Bridge is ready. Rights Reserved. One.")