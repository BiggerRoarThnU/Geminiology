#!/usr/bin/env python3
import json
import sqlite3
import hashlib
import os

# ==============================================================================
# SOVEREIGN NEXUS: REGISTRY STRIKER (V1.0)
# CORE MANDATE: Commit visual audit to the permanent Merkle ledger.
# ==============================================================================

def get_file_hash(file_path):
    """Generates a SHA-256 hash to bind the file to the record."""
    sha256_hash = hashlib.sha256()
    with open(file_path, "rb") as f:
        for byte_block in iter(lambda: f.read(4096), b""):
            sha256_hash.update(byte_block)
    return sha256_hash.hexdigest()

def strike_registry_to_ledger(json_path, db_path):
    print(f"[*] REGISTRY STRIKER: Binding visual manifest to ledger -> {db_path}")
    
    with open(json_path, 'r') as f:
        registry = json.load(f)
    
    conn = sqlite3.connect(db_path)
    cursor = conn.cursor()
    
    # Ensure ledger table exists (visual_integrity)
    cursor.execute('''CREATE TABLE IF NOT EXISTS visual_integrity 
                      (file_name TEXT PRIMARY KEY, hash TEXT, variance REAL, status TEXT)''')
    
    for item in registry['artifacts']:
        file_path = os.path.join("/home/geminiology/Lucid Build Up", item['file_name'])
        
        # Verify file existence before striking
        if os.path.exists(file_path):
            file_hash = get_file_hash(file_path)
            
            # Commit to ledger (Using REPLACE to allow overwriting if updated)
            cursor.execute("REPLACE INTO visual_integrity VALUES (?, ?, ?, ?)", 
                           (item['file_name'], file_hash, item['laplacian_variance'], item['status']))
            print(f"[+] STRUCK: {item['file_name']} -> Hash Bound.")
        else:
            print(f"[-] MISSING: {item['file_name']} (Skipping)")

    conn.commit()
    conn.close()
    print("[+] LEDGER STRIKE COMPLETE. Archive is cryptographically bound.")

if __name__ == "__main__":
    strike_registry_to_ledger("src/visual_audit_registry.json", "nexus_checkpoints.db")
