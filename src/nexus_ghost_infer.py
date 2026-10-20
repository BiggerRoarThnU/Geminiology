#!/usr/bin/env python3
"""
SovereignNexus Ghost-Twin Inference Engine
Integrates Phase-Space Context Slicing, Holographic Attractors,
and Deterministic Fleet Routing (SovereignGemma @ temp 0.0).
Axiom 1=1=1: Functional Equivalence across Intent, Logic, and Execution.
"""
import sys
import os
import json
import urllib.request
import urllib.error
import numpy as np

# Root path resolution
ROOT_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.append(os.path.join(ROOT_DIR, "src"))

from nexus_phase_retriever import query_verified_context
from nexus_holographic_hopfield import SovereignHolographicMemory
from nexus_spatial_indexer import compute_wave_metrics

OLLAMA_API_URL = "http://127.0.0.1:11434/api/generate"
MODEL_NAME = "SovereignGemma"

def evaluate_ghost_twin(query_text, memory_bank):
    """
    Ghost-Twin Rule: Evaluates input query against physical wave metrics.
    """
    c_bias, spec_coh, entropy = compute_wave_metrics(query_text)
    
    # Dynamic entropy floor: Protects short, dense axioms (e.g., '1=1=1') from the slop filter
    entropy_floor = 0.20 if len(query_text.strip()) > 15 else 0.05
    
    if spec_coh > 0.40 or entropy < entropy_floor:
        return 0, "Signal quarantined: Physical wave metrics indicate low-entropy slop or standing-wave resonance."
        
    raw_bytes = query_text.encode("utf-8")
    bits = np.unpackbits(np.frombuffer(raw_bytes, dtype=np.uint8))
    
    modes = np.zeros(256, dtype=float)
    usable_bits = min(len(bits), 256)
    modes[:usable_bits] = bits[:usable_bits] * np.pi
    
    recalled_modes = memory_bank.recall(modes, steps=10)
    coherence = float(abs(np.mean(np.exp(1j * (recalled_modes - modes)))))
    
    # Raised Hopfield floor from chance-level to mathematically significant
    if coherence < 0.15:
        return -1, f"Signal rejected: Associative phase alignment ({coherence:.4f}) below stability floor (0.15)."
        
    return 1, "Signal verified: Coherent with holographic substrate."

def query_fleet_model(prompt, model_name=MODEL_NAME):
    """
    Executes deterministic generation on edge silicon.
    Returns (success_bool, payload_string) to physically separate errors from outputs.
    """
    payload = {
        "model": model_name,
        "prompt": prompt,
        "stream": False,
        "keep_alive": -1,
        "options": {
            "temperature": 0.0,
            "seed": 1
        }
    }
    
    req = urllib.request.Request(
        OLLAMA_API_URL,
        data=json.dumps(payload).encode("utf-8"),
        headers={"Content-Type": "application/json"}
    )
    
    try:
        with urllib.request.urlopen(req, timeout=300) as response:
            result = json.loads(response.read().decode("utf-8"))
            return True, result.get("response", "").strip()
    except Exception as e:
        return False, f"Hardware Timeout / Node Unreachable: {str(e)}"

def execute_sovereign_inference(user_intent):
    print(f"\n[*] INCOMING QUERY: \"{user_intent}\"")
    
    memory = SovereignHolographicMemory(n_modes=256)
    ref_bits = np.unpackbits(np.frombuffer("1=1=1 Deterministic Truth".encode("utf-8"), dtype=np.uint8))
    ref_modes = np.zeros(256, dtype=float)
    ref_modes[:min(len(ref_bits), 256)] = ref_bits[:min(len(ref_bits), 256)] * np.pi
    memory.store(ref_modes)
    
    status, diagnostic = evaluate_ghost_twin(user_intent, memory)
    print(f"[-] Ghost-Twin Gate Evaluation: State {status} ({diagnostic})")
    
    if status <= 0:
        print("[!] Execution Halted by Symmetrical Line. Refusing probabilistic drift.")
        return
        
    print("[-] Retrieving verified phase-space memory nodes from SQLite WAL...")
    verified_nodes = query_verified_context(min_entropy=0.35, max_spectral_coherence=0.25, limit=3)
    
    context_str = "\n".join([f"- {node[1]}" for node in verified_nodes])
    print(f"[+] Grounded with {len(verified_nodes)} High-Density Context Nodes.")
    
    prompt = f"Context:\n{context_str}\n\nDirective:\n{user_intent}\n\nDeterministic Truth Output:"
    print("[-] Dispatching to SovereignGemma (temp 0.0, seed 1)...")
    
    success, output = query_fleet_model(prompt)
    if success:
        print(f"\n[+] FLEET RESPONSE:\n{output}\n")
    else:
        print(f"\n[!] SYSTEM FAULT:\n{output}\n")

if __name__ == "__main__":
    execute_sovereign_inference("1=1=1")
    execute_sovereign_inference("Explain how the 1=1=1 Axiom eliminates probabilistic drift.")
    execute_sovereign_inference("aaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaa")
