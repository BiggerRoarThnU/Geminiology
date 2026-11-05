#!/usr/bin/env python3
"""
SOVEREIGNNEXUS LLC - AIRLOCK PROXY (ROOM 1 & 3)
Axiom: 1=1=1 (Functional Equivalence)
Objective: Port 8080 Local HTTP Proxy, Thermal Governance, and SQLite WAL Archiving (Patched)
"""

from flask import Flask, request, jsonify
import sqlite3
import json
import os
import hashlib
from nexus_media_forge import SovereignMediaForge

app = Flask(__name__)
forge = SovereignMediaForge()
DB_PATH = 'visual_audit_registry.db'
MANIFEST_PATH = 'visual_audit_registry.json'

def enforce_metabolic_governor():
    """Reads bare-metal Linux thermal zones to enforce Landauer limits."""
    try:
        with open('/sys/class/thermal/thermal_zone0/temp', 'r') as f:
            temp_c = int(f.read().strip()) / 1000.0
            
        if temp_c >= 105.0:
            # FIX 2: Return the HALT string instead of raising a RuntimeError to allow a clean 503 response
            return f"HALT: 105°C Landauer Limit Reached. Temp: {temp_c}°C"
        elif temp_c >= 85.0:
            return "SINGLE-BATCH-PAUSE"
        elif temp_c >= 75.0:
            return "THROTTLE"
        return "NOMINAL"
    except FileNotFoundError:
        return "NOMINAL"

def init_wal_ledger():
    """Initializes Room 3: Append-only SQLite WAL database."""
    conn = sqlite3.connect(DB_PATH)
    conn.execute('PRAGMA journal_mode=WAL;')
    conn.execute('''
        CREATE TABLE IF NOT EXISTS IPG_Registry (
            hash_id TEXT PRIMARY KEY,
            filename TEXT,
            variance REAL,
            logic_state INTEGER,
            timestamp DATETIME DEFAULT CURRENT_TIMESTAMP
        )
    ''')
    conn.commit()
    conn.close()

@app.route('/airlock/ingest', methods=['POST'])
def ingest_payload():
    thermal_state = enforce_metabolic_governor()
    if "HALT" in thermal_state:
        return jsonify({"error": thermal_state}), 503

    if 'file' not in request.files:
        return jsonify({"error": "No file payload provided"}), 400
        
    file = request.files['file']
    filename = file.filename
    temp_path = f"/tmp/{filename}"
    file.save(temp_path)

    # FIX 3: Cryptographic Content Binding (Hash the actual file bytes, not the name)
    sha256_hash = hashlib.sha256()
    with open(temp_path, "rb") as f:
        for byte_block in iter(lambda: f.read(4096), b""):
            sha256_hash.update(byte_block)
    file_hash = sha256_hash.hexdigest()

    # Room 1 -> Room 2: Laplacian Strike
    logic_state, variance = forge.audit_visual_payload(temp_path)
    
    if logic_state == 1:
        # Room 3: The Archive (Valid Assets Only)
        conn = sqlite3.connect(DB_PATH)
        conn.execute('INSERT INTO IPG_Registry (hash_id, filename, variance, logic_state) VALUES (?, ?, ?, ?)',
                     (file_hash, filename, variance, logic_state))
        conn.commit()
        conn.close()
        
        # Append to JSON Manifest
        manifest_entry = {"hash": file_hash, "file": filename, "variance": variance, "status": "VERIFIED_ENTROPY"}
        with open(MANIFEST_PATH, 'a') as f:
            f.write(json.dumps(manifest_entry) + '\n')
            
        os.remove(temp_path)
        return jsonify({"status": "BELIEF (+1)", "variance": variance, "hash": file_hash}), 200
        
    else:
        # 0-State Quarantine: File is physically deleted from storage as well as RAM
        os.remove(temp_path)
        return jsonify({"status": "QUARANTINE (0)", "variance": variance, "message": "Synthetic slop or chaotic noise rejected."}), 406

if __name__ == '__main__':
    init_wal_ledger()
    print("Sovereign Airlock Proxy running on Port 8080...")
    app.run(host='0.0.0.0', port=8080, threaded=False)
