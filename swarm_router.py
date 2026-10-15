#!/usr/bin/env python3
import os
import sys
import sqlite3
import hashlib
from datetime import datetime

# ==============================================================================
# SovereignNexus: Swarm Router
# Component: swarm_router.py
# Axiom: 1=1=1 | Status: ACTIVE
# Description: Filters and routes incoming system logs and history files through
#              the 12 Master Node architecture, sealing entries with SHA-256.
# ==============================================================================

DB_PATH = os.path.expanduser("~/SovereignNexus/nexus_ledger.db")

# Mapping of the 24 agents to the 12 Master Nodes
MASTER_NODE_MAPPING = {
    1: {"name": "Security Baseline", "agents": [1, 13], "desc": "Baseline structures & signature verification"},
    2: {"name": "Thermal Telemetry & Throttle", "agents": [2, 23], "desc": "Thermal sensors & execution throttling"},
    3: {"name": "Serialization & Format Bridge", "agents": [3, 20], "desc": "Format conversion & output collation"},
    4: {"name": "Firewalled Audit & Sanitation", "agents": [4, 10], "desc": "Regex noise filtering & zero-trust security"},
    5: {"name": "Data Ingestion & Storage Control", "agents": [5, 18], "desc": "Staging ingress & cold-storage indexing"},
    6: {"name": "Intent & Validation Engine", "agents": [6, 14], "desc": "Intent validation & historical document parsing"},
    7: {"name": "High-Density Archival Core", "agents": [7, 15], "desc": "High-density compression & multidimensional search"},
    8: {"name": "Discovery & Active Ingress", "agents": [8, 24], "desc": "Ingestion scanning & debug anomaly detection"},
    9: {"name": "Semantic Routing & Orientation", "agents": [9, 17], "desc": "Semantic routing & fast vector DB query"},
    10: {"name": "Swarm Vanguard Coordination", "agents": [12, 11], "desc": "Swarm coordination & multithreaded harmony"},
    11: {"name": "Local Model Execution Core", "agents": [21, 19], "desc": "Local model execution & API routing"},
    12: {"name": "Network Topology Mapping", "agents": [22, 16], "desc": "Topology mapping & data graph visualization"}
}

def init_router_db():
    conn = sqlite3.connect(DB_PATH)
    c = conn.cursor()
    c.execute('''CREATE TABLE IF NOT EXISTS routed_master_ledger (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    timestamp TEXT,
                    master_node_id INTEGER,
                    master_node_name TEXT,
                    triggering_agent INTEGER,
                    log_content TEXT,
                    log_hash TEXT UNIQUE
                )''')
    conn.commit()
    conn.close()

def get_node_by_agent(agent_id):
    """Finds which Master Node a given Agent ID belongs to."""
    for node_id, info in MASTER_NODE_MAPPING.items():
        if agent_id in info["agents"]:
            return node_id, info["name"]
    return None, None

def route_log_entry(agent_id, content):
    """Routes and seals a log entry under the 12 Master Node architecture."""
    node_id, node_name = get_node_by_agent(agent_id)
    if not node_id:
        print(f"[!] Warning: Agent {agent_id} does not map to a Master Node. Log rejected.")
        return False
        
    log_hash = hashlib.sha256(content.encode('utf-8')).hexdigest()
    timestamp = datetime.now().isoformat()
    
    conn = sqlite3.connect(DB_PATH)
    c = conn.cursor()
    try:
        c.execute("""
            INSERT INTO routed_master_ledger 
            (timestamp, master_node_id, master_node_name, triggering_agent, log_content, log_hash)
            VALUES (?, ?, ?, ?, ?, ?)
        """, (timestamp, node_id, node_name, agent_id, content, log_hash))
        conn.commit()
        print(f"[✓] Log from Agent {agent_id:02d} routed to Master Node {node_id:02d} ({node_name}). Hash: {log_hash[:16]}...")
        return True
    except sqlite3.IntegrityError:
        print(f"[-] Duplicate log from Agent {agent_id:02d}. Already sealed. Skipping.")
        return False
    except Exception as e:
        print(f"[!] Database routing error: {e}")
        return False
    finally:
        conn.close()

if __name__ == "__main__":
    init_router_db()
    print("=" * 60)
    print(" Sovereign Swarm Router: INITIALIZED")
    print(" Filtering logs through the 12 Master Nodes...")
    print("=" * 60)
    
    # Quick verification routing test
    route_log_entry(11, "Architect Agent: Synchronizing multi-node memory states.")
    route_log_entry(2, "Thermometer Agent: CPU Core temperature read at 35.0 C.")
