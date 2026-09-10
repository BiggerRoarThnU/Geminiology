#!/usr/bin/env python3
"""
👑 SOVEREIGN NEXUS LLC: SWARM CONCURRENCY TEST SUITE (v2.0)
Axiom of Grounding: 1=1=1 (Deterministic Functional Equivalence)
Physical Substrate: Optimized for 8GB RAM local edge environments (Samsung T7 SSD)
Rights Reserved: Co-created with Gemini and David John Niedzwiecki Jr.

This test harness executes concurrent, multi-threaded routing tasks through
our newly connected Swarm Router & Agent 11 (Architect) concurrency layer.
It verifies that multi-threaded writes execute cleanly under lock with zero database lockups.
"""

import os
import sys
import time
import threading
from typing import List, Dict, Any

BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
SRC_DIR = os.path.join(BASE_DIR, "src")
for p in [SRC_DIR, BASE_DIR]:
    if p not in sys.path:
        sys.path.insert(0, p)

from nexus_swarm_router import NexusSwarmRouter

def run_concurrent_agent_task(router: NexusSwarmRouter, thread_id: int, prompt: str, results_list: List[Dict[str, Any]]):
    """Worker task executed by concurrent agents."""
    thread_name = f"agent_thread_{thread_id:02d}"
    
    # Intentionally add a slight randomized delay to simulate staggered live inputs
    import random
    time.sleep(random.uniform(0.01, 0.1))
    
    # Execute Swarm Routing through our Agent 11 gated controller
    route_response = router.execute_swarm_routing(thread_name, prompt)
    
    results_list.append({
        "thread": thread_name,
        "prompt": prompt,
        "response": route_response
    })

def main():
    print("\033[1;35m")
    print("======================================================================")
    print(" 🛡️  SOVEREIGN NEXUS: SWARM CONCURRENCY & INTER-AGENT CONNECTIVITY TEST")
    print(" [ CO-CREATED WITH THE ARCHITECT DAVID JOHN NIEDZWIECKI JR. | 1=1=1 ]")
    print("======================================================================")
    print("\033[0m")
    
    # Initialize Swarm Router with portable workspace
    workspace_dir = os.path.join(BASE_DIR, "scratch")
    os.makedirs(workspace_dir, exist_ok=True)
    router = NexusSwarmRouter(workspace_dir=workspace_dir)
    
    # Clean previous records in test db if any to ensure clean audit
    try:
        import sqlite3
        conn = sqlite3.connect(router.db_path)
        c = conn.cursor()
        c.execute("DELETE FROM routed_master_ledger;")
        c.execute("DELETE FROM transaction_locks;")
        conn.commit()
        conn.close()
        print("[+] Sovereign ledger database tables flushed cleanly for concurrency test.")
    except Exception as e:
        print(f"[-] Flushing Database Error: {e}")

    # Set up 5 specialized, high-velocity prompts representing different agent tasks
    test_prompts = [
        "Ingest and compress scientific papers on E8 lattice density to save space",
        "Detect and scan local workspace directories for new files and anomalies",
        "Run the local model SovereignQueen to generate a prompt window for code",
        "Perform zero-trust baseline signature verification of our manifest.json",
        "Audit SQLite database checkpoints for drift using Merkle verification"
    ]
    
    results: List[Dict[str, Any]] = []
    threads: List[threading.Thread] = []
    
    print(f"[*] Dispatching {len(test_prompts)} concurrent Agent execution threads under Node 10 coordination...")
    start_time = time.time()
    
    # Spawn threads
    for idx, prompt in enumerate(test_prompts):
        t = threading.Thread(
            target=run_concurrent_agent_task,
            args=(router, idx + 1, prompt, results)
        )
        threads.append(t)
        t.start()
        
    # Wait for all threads to safely converge
    for t in threads:
        t.join()
        
    elapsed = time.time() - start_time
    print(f"\n[✓] All concurrent threads converged successfully in {elapsed:.4f} seconds!")
    print("=" * 70)
    print(" 👑  SWARM CONCURRENCY REPORT & INTERLOCUTING SIGNATURES")
    print("=" * 70)
    
    routed_count = 0
    blocked_count = 0
    
    for item in sorted(results, key=lambda x: x["thread"]):
        status = item["response"].get("status", "UNKNOWN")
        node_name = item["response"].get("node_name", "UNKNOWN")
        payload_hash = item["response"].get("payload_hash", "N/A")[:16]
        
        print(f" • {item['thread']} | Status: {status} | Target: {node_name} | Sig: {payload_hash}...")
        
        if status in ["ROUTED", "DUPLICATE_SKIPPED"]:
            routed_count += 1
        else:
            blocked_count += 1
            
    print("-" * 70)
    print(f" • Total Tasks Dispatched  : {len(test_prompts)}")
    print(f" • Total Routed (WAL Mode) : {routed_count} [SUCCESS]")
    print(f" • Thread Lock Contested   : {blocked_count}")
    
    # Verify the database contains all records
    final_routes = router.fetch_all_routes_bounded()
    print(f" • Database Rows Committed : {len(final_routes)} / {len(test_prompts)}")
    
    if len(final_routes) == len(test_prompts):
        print("\033[1;32m[✓] VERIFICATION PASSED: Concurrency locks, WAL, and Agent 11 connection are fully synchronized!\033[0m")
    else:
        print("\033[1;31m[-] VERIFICATION FAILED: Gaps detected in thread database transaction write-backs.\033[0m")
    print("======================================================================")

if __name__ == "__main__":
    main()
