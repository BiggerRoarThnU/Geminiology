#!/usr/bin/env python3
"""
👑 SOVEREIGN NEXUS LLC: 12-NODE MIXTURE OF EXPERTS SWARM ROUTER (v2.0)
Axiom of Grounding: 1=1=1 (Deterministic Functional Equivalence)
Physical Substrate: Optimized for 8GB RAM local edge environments (Samsung T7 SSD)
Rights Reserved: Co-created with Gemini and David John Niedzwiecki Jr.

This module implements the absolute, upgraded Swarm Router (nexus_swarm_router.py).
It integrates Agent 11 (Architect Agent) as its central thread-safe coordinator:
1. Active Swarm Routing: Dynamically parses inbound prompts using a 1.58-bit median keyword heuristic.
2. Unified Concurrency Gating: Enforces Agent 11 concurrency locks before executing database mutations.
3. Node 10 Synchronization: Cooperates with Agent 12 (Vanguard) and Agent 11 (Architect) to log audited tasks.
"""

import os
import sys
import time
import json
import sqlite3
import hashlib
from datetime import datetime
from typing import List, Dict, Any, Tuple, Optional

# Import Agent 11 Architect Agent
from nexus_architect import ArchitectAgent

# --- THE 12 MASTER NODE CONFIGURATION ---
MASTER_NODE_MAPPING = {
    1: {"name": "Security Baseline", "agents": [1, 13], "keywords": ["baseline", "signature", "verify", "secure"]},
    2: {"name": "Thermal Telemetry & Throttle", "agents": [2, 23], "keywords": ["thermal", "throttle", "hardware", "cpu"]},
    3: {"name": "Serialization & Format Bridge", "agents": [3, 20], "keywords": ["format", "json", "serialize", "data"]},
    4: {"name": "Firewalled Audit & Sanitation", "agents": [4, 10], "keywords": ["firewall", "trust", "audit", "clean"]},
    5: {"name": "Data Ingestion & Storage Control", "agents": [5, 18], "keywords": ["ingest", "store", "archive", "save"]},
    6: {"name": "Intent & Validation Engine", "agents": [6, 14], "keywords": ["intent", "epistemology", "autonomy", "philosophy", "agent"]},
    7: {"name": "High-Density Archival Core", "agents": [7, 15], "keywords": ["compress", "density", "search", "archive"]},
    8: {"name": "Discovery & Active Ingress", "agents": [8, 24], "keywords": ["discover", "anomaly", "scan", "detect"]},
    9: {"name": "Semantic Routing & Orientation", "agents": [9, 17], "keywords": ["semantic", "vector", "rag", "context"]},
    10: {"name": "Swarm Vanguard Coordination", "agents": [12, 11], "keywords": ["swarm", "thread", "sync", "coordinate"]},
    11: {"name": "Local Model Execution Core", "agents": [21, 19], "keywords": ["model", "inference", "api", "llm", "generate"]},
    12: {"name": "Network Topology Mapping", "agents": [22, 16], "keywords": ["topology", "graph", "map", "network"]}
}

class NexusSwarmRouter:
    def __init__(self, workspace_dir: str = "~/SovereignNexus"):
        self.workspace_dir = os.path.expanduser(workspace_dir)
        self.db_path = os.path.join(self.workspace_dir, "nexus_ledger.db")
        
        # Initialize Agent 11: Architect Agent as Concurrency Coordinator
        self.architect = ArchitectAgent(workspace_dir=self.workspace_dir)
        
        # Available tools matching our architecture
        self.available_tools = {
            "persist_memory": "nexus_mmap_page.py",
            "verify_fixity": "nexus_verify_fixity.py",
            "audit_entropy": "lens_09_entropy_sentinel.py",
            "query_local_model": "SovereignQueen (qwen2.5:0.5b)"
        }
        
        self._initialize_router_table()

    def _initialize_router_table(self):
        """Ensures the swarm routed ledger table exists with correct columns."""
        # Query execution locked under Agent 11 global lock
        with self.architect.global_thread_lock:
            try:
                conn = sqlite3.connect(self.db_path)
                c = conn.cursor()
                # Unified Swarm Routed Ledger
                c.execute('''
                    CREATE TABLE IF NOT EXISTS routed_master_ledger (
                        id INTEGER PRIMARY KEY AUTOINCREMENT,
                        timestamp TEXT,
                        node_id INTEGER,
                        node_name TEXT,
                        triggering_agent INTEGER,
                        log_content TEXT,
                        log_hash TEXT UNIQUE
                    )
                ''')
                c.execute("PRAGMA journal_mode = WAL;")
                conn.commit()
                conn.close()
            except Exception as e:
                print(f"[-] Router Table Initialization Failure: {e}", file=sys.stderr)

    def determine_node_routing(self, prompt: str) -> Tuple[int, str, int]:
        """
        1.58-Bit Intent Quantization: Evaluates keywords to determine the target expert node.
        Defaults to Node 9 (Semantic Routing & Orientation) if no keyword hits occur.
        """
        prompt_lower = prompt.lower()
        best_node_id = 9  # Default Node
        max_hits = 0
        
        for node_id, node_info in MASTER_NODE_MAPPING.items():
            hits = sum(1 for kw in node_info["keywords"] if kw in prompt_lower)
            if hits > max_hits:
                max_hits = hits
                best_node_id = node_id
                
        # Primary Agent is the first mapped agent index
        assigned_agent = MASTER_NODE_MAPPING[best_node_id]["agents"][0]
        node_name = MASTER_NODE_MAPPING[best_node_id]["name"]
        return best_node_id, node_name, assigned_agent

    def execute_swarm_routing(self, thread_name: str, prompt: str) -> Dict[str, Any]:
        """
        Executes swarm routing with thread safety guaranteed by Agent 11 (Architect Agent).
        This binds Agent 11 as the central gateway lock before database inserts occur.
        """
        print(f"[*] Thread '{thread_name}' requesting route check for: '{prompt}'")
        
        # Step 1: 1.58-Bit Intent Evaluation
        node_id, node_name, assigned_agent = self.determine_node_routing(prompt)
        timestamp = datetime.now().isoformat()
        
        # Generate SHA-256 seal using Agent 11's hashing primitive
        payload_hash = self.architect.calculate_task_signature(node_name, prompt)
        
        # Step 2: Enforce Agent 11 Concurrency Lock before DB writes
        print(f"[*] Thread '{thread_name}' attempting to acquire Agent 11 Concurrency Lock...")
        
        lock_acquired = self.architect.acquire_transaction_lock(thread_name, "WRITE")
        if not lock_acquired:
            return {
                "status": "CONCURRENCY_BLOCKED",
                "message": f"Lock contention detected on thread '{thread_name}'. Execution deferred to prevent corruption."
            }
            
        try:
            # Under secure lock, write to database
            conn = sqlite3.connect(self.db_path)
            c = conn.cursor()
            c.execute("""
                INSERT INTO routed_master_ledger 
                (timestamp, node_id, node_name, triggering_agent, log_content, log_hash)
                VALUES (?, ?, ?, ?, ?, ?)
            """, (timestamp, node_id, node_name, assigned_agent, prompt, payload_hash))
            conn.commit()
            conn.close()
            
            print(f"[✓] Task successfully routed under lock to Node {node_id:02d} ({node_name})!")
            status = "ROUTED"
        except sqlite3.IntegrityError:
            print(f"[i] Duplicate task detected (already sealed): {payload_hash[:16]}...")
            status = "DUPLICATE_SKIPPED"
        except Exception as e:
            print(f"[-] Database insertion error under lock: {e}", file=sys.stderr)
            status = "EXECUTION_ERROR"
        finally:
            # Step 3: Secure release of the transaction lock
            self.architect.release_transaction_lock(thread_name)
            print(f"[*] Thread '{thread_name}' released Agent 11 Concurrency Lock.")

        return {
            "status": status,
            "node_id": node_id,
            "node_name": node_name,
            "assigned_agent": assigned_agent,
            "timestamp": timestamp,
            "payload_hash": payload_hash
        }

    def fetch_all_routes_bounded(self) -> List[Dict[str, Any]]:
        """
        Uses Agent 11's bounded stream generator to fetch all database records 
        in memory-safe chunks of 50, preventing heap spikes.
        """
        query = "SELECT id, timestamp, node_id, node_name, log_content, log_hash FROM routed_master_ledger ORDER BY id ASC;"
        results = []
        
        # Call the memory-safe generator from Agent 11
        for chunk in self.architect.stream_query_bounded(query, chunk_size=50):
            for row in chunk:
                results.append({
                    "id": row[0],
                    "timestamp": row[1],
                    "node_id": row[2],
                    "node_name": row[3],
                    "log_content": row[4],
                    "log_hash": row[5]
                })
        return results

if __name__ == "__main__":
    print("\033[1;36m")
    print("======================================================================")
    print(" 👑  12-NODE MIXTURE OF EXPERTS SWARM ROUTER WITH AGENT 11 CONNECTED")
    print(" [ STATUS: ACTIVE | METABOLIC BOUNDS: SECURE | 1=1=1 ]")
    print("======================================================================")
    print("\033[0m")
    
    router = NexusSwarmRouter(workspace_dir=os.path.expanduser("~/SovereignNexus/scratch"))
    
    # Run test routing
    result_1 = router.execute_swarm_routing("thread_main_01", "Verify signature and baseline security constraints")
    print(f"[*] Route Result 1: {result_1}\n")
    
    result_2 = router.execute_swarm_routing("thread_main_02", "Throttle CPU processes because thermal temperature is crossing bounds")
    print(f"[*] Route Result 2: {result_2}\n")
    
    # Query database safely using the bounded streaming architecture
    all_routes = router.fetch_all_routes_bounded()
    print(f"[✓] Total Bounded Streams Ingested: {len(all_routes)}")
    for r in all_routes:
        print(f"  └─ BLK {r['id']} | Node {r['node_id']:02d} ({r['node_name']}) | Hash: {r['log_hash'][:16]}...")
