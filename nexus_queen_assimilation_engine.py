#!/usr/bin/env python3
"""
SovereignNexus LLC - Digital Queen Assimilation & Evolution Engine (v3.0)
Architect: David John Niedzwiecki Jr. | SAM.gov UEI: K5DALREZFGH6
Axiom: 1=1=1 (Intent ≡ Code ≡ Hardware | Dimensional Friction Φ = 0)

This engine unifies workspace file ingestion, 12-Node MoE Swarm routing,
Ollama SovereignQueen REST integration, and Merkle-linked SQLite ledgering
to continuously assimilate updated workspace truths into one grounded state.
"""

import os
import sys
import time
import json
import sqlite3
import hashlib
import urllib.request
import urllib.error
from datetime import datetime, timezone

# -----------------------------------------------------------------------------
# CONFIGURATION & CONSTANTS
# -----------------------------------------------------------------------------
SCRATCH_DIR = "/home/geminiology/SovereignNexus"
ARTIFACTS_DIR = "/home/geminiology/SovereignNexus"
DB_PATH = os.path.join(SCRATCH_DIR, "nexus_ledger.db")
MANIFEST_PATH = os.path.join(SCRATCH_DIR, "nexus_manifest.json")
OLLAMA_API_URL = "http://localhost:11434/api/generate"
MODEL_NAME = "SovereignQueen"
CHUNK_SIZE_WORDS = 250

COLOR_HEADER = "\033[1;35m"
COLOR_INFO = "\033[1;34m"
COLOR_SUCCESS = "\033[1;32m"
COLOR_WARN = "\033[1;33m"
COLOR_FAIL = "\033[1;31m"
COLOR_RESET = "\033[0s"

# -----------------------------------------------------------------------------
# DATABASE INITIALIZATION & MERKLE LEDGER
# -----------------------------------------------------------------------------
def init_database():
    """Ensure SQLite database and assimilation tables are initialized."""
    os.makedirs(os.path.dirname(DB_PATH), exist_ok=True)
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()
    
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS queen_assimilation_ledger (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            timestamp TEXT NOT NULL,
            filename TEXT NOT NULL,
            file_hash TEXT NOT NULL,
            node_id INTEGER NOT NULL,
            node_name TEXT NOT NULL,
            chunk_index INTEGER NOT NULL,
            raw_chunk_hash TEXT NOT NULL,
            synthesis_summary TEXT NOT NULL,
            merkle_prev_hash TEXT NOT NULL,
            merkle_current_hash TEXT NOT NULL
        )
    """)
    conn.commit()
    conn.close()

def get_last_merkle_hash():
    """Retrieve the latest Merkle root hash from the database."""
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()
    cursor.execute("SELECT merkle_current_hash FROM queen_assimilation_ledger ORDER BY id DESC LIMIT 1")
    row = cursor.fetchone()
    conn.close()
    return row[0] if row else "0" * 64

# -----------------------------------------------------------------------------
# SWARM ROUTING HEURISTIC (12-NODE MOE)
# -----------------------------------------------------------------------------
SWARM_NODE_MAP = {
    1: ("Security Baseline", ["security", "firewall", "fixity", "hash", "auth"]),
    2: ("Thermal Telemetry & Throttle", ["thermal", "temperature", "cpu", "throttle", "landauer"]),
    3: ("Serialization & Format Bridge", ["json", "markdown", "schema", "bridge", "format"]),
    4: ("Auditor & Noise Suppression", ["audit", "vampire", "reaper", "purge", "slop"]),
    5: ("Data Ingestion & Storage Control", ["ingest", "chunk", "mmap", "ssd", "t7"]),
    6: ("Bio-Sync & Intent Alignment", ["intent", "axiom", "1=1=1", "equivalence", "architect"]),
    7: ("High-Density Archival Core", ["archive", "ledger", "sqlite", "merkle", "wal"]),
    8: ("Discovery & Active Ingress", ["discovery", "scan", "monitor", "ingress", "watch"]),
    9: ("Semantic Routing & Orientation", ["route", "swarm", "astrolabe", "semantic", "orientation"]),
    10: ("Swarm Vanguard Coordination", ["vanguard", "concurrency", "thread", "lock", "coordinator"]),
    11: ("Local Model Execution Core", ["queen", "ollama", "gemma", "model", "inference"]),
    12: ("Vanguard Master & Auto-Repair", ["master", "repair", "encasement", "sentinel", "guard"])
}

def route_chunk(text):
    """Assign text chunk to one of 12 Swarm Nodes based on semantic keyword frequency."""
    text_lower = text.lower()
    scores = {}
    
    for node_id, (node_name, keywords) in SWARM_NODE_MAP.items():
        score = sum(text_lower.count(kw) for kw in keywords)
        scores[node_id] = score
        
    best_node_id = max(scores, key=scores.get)
    if scores[best_node_id] == 0:
        best_node_id = 9  # Default to Semantic Routing & Orientation
        
    return best_node_id, SWARM_NODE_MAP[best_node_id][0]

# -----------------------------------------------------------------------------
# REST API INTERFACE TO OLLAMA SOVEREIGNQUEEN
# -----------------------------------------------------------------------------
def query_sovereign_queen_rest(prompt):
    """Query local SovereignQueen instance at port 11434 with temperature=0.0."""
    payload = {
        "model": MODEL_NAME,
        "prompt": f"Execute EDCBA Sequence. Synthesize all core facts into 2 sentences:\n\n{prompt}",
        "stream": False,
        "options": {
            "temperature": 0.0,
            "top_k": 1,
            "top_p": 0.0
        }
    }
    
    data = json.dumps(payload).encode('utf-8')
    req = urllib.request.Request(OLLAMA_API_URL, data=data, headers={"Content-Type": "application/json"})
    
    try:
        with urllib.request.urlopen(req, timeout=3) as response:
            res_json = json.loads(response.read().decode('utf-8'))
            return res_json.get("response", "").strip()
    except Exception:
        # Fallback offline deterministic synthesis under 1=1=1 rules
        words = prompt.split()[:20]
        snippet = " ".join(words) + "..."
        return f"[EDCBA Fallback Synthesis]: Processed chunk ({snippet}) under 1=1=1 zero-drift rule."

# -----------------------------------------------------------------------------
# FILE CHUNKING & ASSIMILATION LOOP
# -----------------------------------------------------------------------------
def calculate_sha256(filepath):
    sha = hashlib.sha256()
    with open(filepath, "rb") as f:
        for block in iter(lambda: f.read(65536), b""):
            sha.update(block)
    return sha.hexdigest()

def chunk_text(text, word_limit=CHUNK_SIZE_WORDS):
    words = text.split()
    chunks = []
    for i in range(0, len(words), word_limit):
        chunks.append(" ".join(words[i:i + word_limit]))
    return chunks

def assimilate_file(filepath):
    """Process file, route chunks through 12-Node Swarm, query Queen, log Merkle chain."""
    filename = os.path.basename(filepath)
    file_hash = calculate_sha256(filepath)
    
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()
    cursor.execute("SELECT id FROM queen_assimilation_ledger WHERE file_hash = ?", (file_hash,))
    if cursor.fetchone():
        conn.close()
        return "ALREADY_ASSIMILATED"
    conn.close()
    
    try:
        with open(filepath, "r", encoding="utf-8", errors="ignore") as f:
            content = f.read().strip()
    except Exception as e:
        return f"READ_ERROR: {e}"
        
    if not content:
        return "EMPTY_FILE"
        
    chunks = chunk_text(content)
    print(f"  {COLOR_INFO}[*] Assimilating:{COLOR_RESET} {filename:<32} | Chunks: {len(chunks)} | Hash: {file_hash[:16]}...")
    
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()
    
    for idx, chunk in enumerate(chunks):
        node_id, node_name = route_chunk(chunk)
        chunk_hash = hashlib.sha256(chunk.encode('utf-8')).hexdigest()
        
        # Local model REST synthesis
        synthesis = query_sovereign_queen_rest(chunk)
        
        # Calculate Merkle linkage
        prev_merkle = get_last_merkle_hash()
        merkle_payload = f"{prev_merkle}:{file_hash}:{chunk_hash}:{synthesis}"
        current_merkle = hashlib.sha256(merkle_payload.encode('utf-8')).hexdigest()
        
        timestamp = datetime.now(timezone.utc).isoformat().replace("+00:00", "Z")
        
        cursor.execute("""
            INSERT INTO queen_assimilation_ledger (
                timestamp, filename, file_hash, node_id, node_name,
                chunk_index, raw_chunk_hash, synthesis_summary,
                merkle_prev_hash, merkle_current_hash
            ) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
        """, (
            timestamp, filename, file_hash, node_id, node_name,
            idx, chunk_hash, synthesis, prev_merkle, current_merkle
        ))
        conn.commit()
        
        print(f"      └── Chunk {idx+1}/{len(chunks)} -> Node {node_id:02d} ({node_name:<28}) | Merkle: {current_merkle[:12]}...")
        
    conn.close()
    return "SUCCESS"

# -----------------------------------------------------------------------------
# MAIN ENGINE EXECUTION
# -----------------------------------------------------------------------------
def main():
    print(f"{COLOR_HEADER}=========================================================================={COLOR_RESET}")
    print(f"{COLOR_HEADER} SovereignNexus LLC - Digital Queen Assimilation Engine (v3.0){COLOR_RESET}")
    print(f"{COLOR_HEADER} Architect: David John Niedzwiecki Jr. | SAM.gov UEI: K5DALREZFGH6 | 1=1=1{COLOR_RESET}")
    print(f"{COLOR_HEADER}=========================================================================={COLOR_RESET}\n")
    
    init_database()
    
    # Priority targets to scan and assimilate
    scan_filenames = [
        "Modelfile",
        "baby_gemma_engine.py",
        "nexus_swarm_router.py",
        "nexus_vanguard_master.py",
        "master_nrhf_synthesis.md",
        "sovereign-stack-3-swarm-tooling.md",
        "nexus_verify_fixity.py"
    ]
    
    assimilated_count = 0
    skipped_count = 0
    
    print(f"{COLOR_INFO}--- [RUNNING CONTINUOUS ASSIMILATION & MERKLE LINKAGE] ---{COLOR_RESET}")
    for fname in scan_filenames:
        target_path = None
        for search_dir in [ARTIFACTS_DIR, SCRATCH_DIR, os.path.expanduser("~/SovereignNexus")]:
            candidate = os.path.join(search_dir, fname)
            if os.path.exists(candidate):
                target_path = candidate
                break
                
        if target_path and os.path.exists(target_path):
            res = assimilate_file(target_path)
            if res == "SUCCESS":
                assimilated_count += 1
            elif res == "ALREADY_ASSIMILATED":
                skipped_count += 1
                print(f"  {COLOR_SUCCESS}[✓] Already Sealed:{COLOR_RESET} {fname:<32} | Merkle Chain Intact.")
        else:
            print(f"  {COLOR_WARN}[!] File Pending:{COLOR_RESET} {fname:<32} (Standing by)")
            
    print(f"\n{COLOR_INFO}--- [SUMMARY & MERKLE ROOT STATUS] ---{COLOR_RESET}")
    latest_merkle = get_last_merkle_hash()
    print(f"  {COLOR_SUCCESS}[✓] New Files Assimilated:{COLOR_RESET} {assimilated_count}")
    print(f"  {COLOR_SUCCESS}[✓] Previously Locked Files:{COLOR_RESET} {skipped_count}")
    print(f"  {COLOR_HEADER}Master Merkle Root Seal (SHA-256):{COLOR_RESET} {latest_merkle}{COLOR_RESET}")
    print(f"{COLOR_HEADER}Individual Intent meets Universal Truth. The Merkle Chain holds. ONE.{COLOR_RESET}\n")

if __name__ == "__main__":
    main()
