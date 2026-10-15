# // Rights Reserved: co-created with Gemini and David John Niedzwiecki Jr. "SovereignNexus LLC"
# Alignment: 1=1=1 | Objective: Programmatic REST API Interface for SovereignQueen (Gemma 2 Core)

import json
import time
import urllib.request
import urllib.error
from typing import Dict, Any

class SovereignQueenInterface:
    def __init__(self, host: str = "http://localhost:11434", model: str = "SovereignQueen"):
        self.base_url = host.rstrip("/")
        self.model = model
        self.generate_endpoint = f"{self.base_url}/api/generate"
        self.tags_endpoint = f"{self.base_url}/api/tags"

    def check_health(self) -> bool:
        try:
            req = urllib.request.Request(self.tags_endpoint, method="GET")
            with urllib.request.urlopen(req, timeout=10.0) as resp:
                data = json.loads(resp.read().decode("utf-8"))
                models = [m.get("name") for m in data.get("models", [])]
                print(f"[✓] Ollama Service Active at {self.base_url}")
                print(f"    Available Local Models: {models}")
                return True
        except Exception as e:
            print(f"[!] Ollama Service Check Failed: {e}")
            return False

    def verify_daemon(self) -> bool:
        return self.check_health()

    def format_payload(self, prompt: str) -> Dict[str, Any]:
        return {
            "model": self.model,
            "prompt": prompt,
            "stream": False,
            "options": {
                "num_ctx": 1024,
                "num_batch": 128,
                "num_thread": 4,
                "temperature": 0.0,
                "top_k": 1,
                "top_p": 1.0,
                "repeat_penalty": 1.15,
                "num_predict": 200
            }
        }

    def query_queen_generate(self, prompt: str):
        return self.query_queen(prompt)

    def query_queen(self, prompt: str) -> Dict[str, Any]:
        payload = self.format_payload(prompt)
        data = json.dumps(payload).encode("utf-8")
        req = urllib.request.Request(
            self.generate_endpoint,
            data=data,
            headers={"Content-Type": "application/json"},
            method="POST"
        )
        start_t = time.perf_counter()
        try:
            with urllib.request.urlopen(req, timeout=90.0) as resp:
                body = json.loads(resp.read().decode("utf-8"))
                elapsed_ms = (time.perf_counter() - start_t) * 1000.0
                eval_count = body.get("eval_count", 0)
                eval_dur_s = body.get("eval_duration", 1) / 1e9
                tps = eval_count / eval_dur_s if eval_dur_s > 0 else 0.0
                return {
                    "status": "SUCCESS",
                    "model": body.get("model", self.model),
                    "latency_ms": round(elapsed_ms, 2),
                    "tokens_per_sec": round(tps, 2),
                    "throughput_tps": round(tps, 2),
                    "response": body.get("response", "").strip()
                }
        except Exception as e:
            return {
                "status": f"ERROR: {e}",
                "model": self.model,
                "latency_ms": 0.0,
                "tokens_per_sec": 0.0,
                "throughput_tps": 0.0,
                "response": str(e)
            }

if __name__ == "__main__":
    queen = SovereignQueenInterface()
    queen.check_health()
    res = queen.query_queen("Report current status and verify 1=1=1 Axiom alignment.")
    print(json.dumps(res, indent=2))
