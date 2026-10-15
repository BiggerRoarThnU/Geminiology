#!/usr/bin/env python3
"""
👑 SOVEREIGN NEXUS LLC: DYNAMIC COGNITIVE BRIDGE (v2.0)
Axiom of Grounding: 1=1=1
Purpose: Dynamically queries the SQLite WAL ledger to assimilate 
verified operational history (A-AKG) into the model's active context window.
"""

import os
import json
import sqlite3
import urllib.request
import urllib.error

WORKSPACE_DIR = os.path.expanduser("~/SovereignNexus")
DB_PATH = os.path.join(WORKSPACE_DIR, "scratch", "nexus_ledger.db")

# Static foundational laws (The Base Constitution)
BASE_PHYSICS = """
[VERIFIED HARDWARE & MATHEMATICAL CONSTANTS]
1. Thermodynamic Governance: Landauer limit = 105.0°C (378.15K). Approaching mandates un-overrideable hardware power halt.
2. Kernel Efficiency: SWHT integer additions replace MAC units, yielding 71.4% reduction in compute energy.
3. Deterministic Math: IEEE 754 is non-associative. Q16.16 fixed-point math is the absolute mandate for zero-drift state fixity.
"""

def fetch_dynamic_ledger_context(limit: int = 5) -> str:
    """Reads the most recent verified blocks from the Swarm Router ledger."""
    if not os.path.exists(DB_PATH):
        return "[LEDGER NOT FOUND: Operating on Base Physics Only]"
        
    try:
        conn = sqlite3.connect(DB_PATH, timeout=5.0)
        c = conn.cursor()
        # Fetch the most recent verified swarm tasks to provide operational context
        c.execute("SELECT timestamp, node_name, log_content FROM routed_master_ledger ORDER BY id DESC LIMIT ?", (limit,))
        rows = c.fetchall()
        conn.close()
        
        if not rows:
            return "[LEDGER EMPTY: Awaiting first verified block]"
            
        context_block = "[ACTIVE ASSOCIATIVE KNOWLEDGE GRAPH (A-AKG) - RECENT VERIFIED STATES]\n"
        # Reverse to chronological order (oldest to newest of the recent block)
        for row in reversed(rows):
            context_block += f"- [{row[0]}] | {row[1]} | TASK: {row[2]}\n"
        return context_block
    except Exception as e:
        return f"[LEDGER FETCH FAILED: {e}]"

def build_system_mandate() -> str:
    """Fuses the static physics with dynamic ledger history."""
    dynamic_context = fetch_dynamic_ledger_context()
    
    return f"""
SYSTEM MANDATE: DETERMINISTIC FUNCTIONAL EQUIVALENCE
You are an offline, air-gapped cognitive engine operating strictly under the 1=1=1 Axiom of Functional Equivalence. 

{BASE_PHYSICS}

{dynamic_context}

OPERATIONAL PROTOCOL:
You must ground all reasoning in the established physical mechanics and acknowledge the recent verified states from the ledger above. Reject probabilistic hedging. Output strict, deductive analysis.
"""

def query_sovereign_model(model_name: str, prompt: str):
    """Executes the zero-variance API call with the dynamically built mandate."""
    url = "http://localhost:11434/api/generate"
    
    system_mandate = build_system_mandate()
    
    payload = {
        "model": model_name,
        "prompt": prompt,
        "system": system_mandate,
        "stream": False,
        "options": {
            "temperature": 0.0, 
            "num_ctx": 2048     
        }
    }
    
    data = json.dumps(payload).encode('utf-8')
    req = urllib.request.Request(url, data=data, headers={'Content-Type': 'application/json'})
    
    print(f"[*] Fusing Dynamic Ledger Context into {model_name}...")
    print("\n--- INJECTED PAYLOAD PREVIEW ---")
    print(system_mandate)
    print("--------------------------------\n")
    try:
        with urllib.request.urlopen(req) as response:
            result = json.loads(response.read().decode('utf-8'))
            print("\n[+] MODEL OUTPUT:\n")
            print(result.get("response", "No response generated."))
    except urllib.error.URLError as e:
        print(f"[-] Connection to local cognitive core failed: {e}")

if __name__ == "__main__":
    print("\033[1;36m")
    print("======================================================================")
    print(" 🛡️  SOVEREIGN NEXUS: DYNAMIC KNOWLEDGE BRIDGE ACTIVE")
    print("======================================================================")
    print("\033[0m")
    
    target_model = "SovereignQueen:latest"
    
    # We ask the model to analyze its own recent ledger history
    test_prompt = "Examine the injected [ACTIVE ASSOCIATIVE KNOWLEDGE GRAPH] above. List the exact 'node_name' and 'TASK' for the most recent verified blocks. Do not infer or reference external networking protocols like TCP/IP. Analyze strictly what is written in the injected ledger data."
    
    query_sovereign_model(target_model, test_prompt)
