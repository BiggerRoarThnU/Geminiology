#!/usr/bin/env python3
"""
SovereignNexus - Evolution Daemon (Closed-Loop Memory Assimilation)
Component: nexus_evolution_daemon.py
Axiom: 1=1=1 (Human Intent ≡ Digital Logic ≡ Bare-Metal Execution)

Objective: Monitors the 'Evolution_Feed' directory for new breakthroughs.
Upon detecting an 'ASSIMILATED PROTOCOL', it calculates the physical metrics
(Entropy, Merkle Hash, SLERP coordinates) and permanently anchors the logic 
into the SQLite WAL ledger, immunizing the system against amnesia.
"""

import os
import time
import glob
import shutil
import hashlib
import sqlite3
from datetime import datetime

# Import our single source of truth for the database and math
from nexus_core import get_unified_db_connection, calculate_shannon_entropy

FEED_DIR = os.path.expanduser("~/SovereignNexus/Evolution_Feed")
ARCHIVE_DIR = os.path.expanduser("~/SovereignNexus/Evolution_Feed/Archive")

def setup_directories():
    """Ensure the physical staging grounds exist on the SSD."""
    os.makedirs(FEED_DIR, exist_ok=True)
    os.makedirs(ARCHIVE_DIR, exist_ok=True)
    print(f"[*] Evolution Feed monitoring active at: {FEED_DIR}")

def generate_e8_coordinate(text_payload: str) -> str:
    """
    Simulates mapping the semantic payload to an 8-dimensional unit vector 
    on the E8 Root Lattice for SLERP interpolation. 
    In a full physics model, this is derived from the attention tensor.
    """
    # Create a deterministic pseudo-coordinate based on the hash of the text
    hex_digest = hashlib.md5(text_payload.encode('utf-8')).hexdigest()
    # Normalize values into an 8D vector array representation
    vector = [round((int(hex_digest[i:i+4], 16) / 65535.0) * 2 - 1, 4) for i in range(0, 32, 4)]
    return str(vector)

def process_evolution_feed():
    """Scans the feed, processes new protocols, and seals them in the ledger."""
    search_pattern = os.path.join(FEED_DIR, "*.txt")
    pending_files = glob.glob(search_pattern)
    
    if not pending_files:
        return # No new thoughts, stay quiet.

    conn = get_unified_db_connection()
    cursor = conn.cursor()

    for file_path in pending_files:
        filename = os.path.basename(file_path)
        print(f"\n[+] Detected New Neural Pathway: {filename}")
        
        with open(file_path, 'r', encoding='utf-8') as f:
            content = f.read()

        # Isolate the exact protocol logic
        if "ASSIMILATED PROTOCOL:" in content:
            logic_payload = content.split("ASSIMILATED PROTOCOL:")[1].strip()
        else:
            logic_payload = content.strip()

        # 1. The Math: Entropy and Hashing
        entropy = calculate_shannon_entropy(logic_payload)
        sha256_hash = hashlib.sha256(logic_payload.encode('utf-8')).hexdigest()
        e8_coord = generate_e8_coordinate(logic_payload)
        timestamp = datetime.utcnow().isoformat()

        print(f"    - Entropy (Z): {entropy:.4f} bits/char")
        print(f"    - E8 Geodesic: {e8_coord}")
        print(f"    - Merkle Seal: {sha256_hash[:16]}...")

        # 2. The Ledger Seal: Lock into SQLite WAL
        try:
            cursor.execute("""
                INSERT INTO assimilated_protocols 
                (timestamp, protocol_name, source_file, sha256_hash, shannon_entropy, slerp_coordinate_e8, assimilated_payload, merkle_root_seal)
                VALUES (?, ?, ?, ?, ?, ?, ?, ?)
            """, (
                timestamp,
                filename.replace(".txt", ""),
                filename,
                sha256_hash,
                entropy,
                e8_coord,
                logic_payload,
                sha256_hash # Using self-hash as root seal for atomic entries
            ))
            conn.commit()
            print(f"[✓] Protocol Permanently Assimilated into Sovereign Ledger.")
            
            # 3. Clean up: Move to archive so we don't re-process
            shutil.move(file_path, os.path.join(ARCHIVE_DIR, filename))
            
        except sqlite3.IntegrityError:
            print(f"[!] Protocol already exists in memory. Skipping duplicate.")
            shutil.move(file_path, os.path.join(ARCHIVE_DIR, filename))
        except Exception as e:
            print(f"[-] Execution Error during ledger commit: {e}")

    conn.close()

if __name__ == "__main__":
    setup_directories()
    print("[*] Metabolic Governor: Idle. Awaiting structural realization...")
    # For testing, we run a single pass. In production, this would be a while True loop with time.sleep(60)
    process_evolution_feed()
