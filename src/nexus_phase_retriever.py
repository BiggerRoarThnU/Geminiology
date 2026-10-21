#!/usr/bin/env python3
"""
SovereignNexus Phase-Space Context Slicer
Retrieves memory nodes filtered by physical wave coherence and Shannon entropy.
Rejects synthetic slop and standing-wave noise before context injection.
"""
import sqlite3
import os

DB_PATH = os.path.expanduser("~/SovereignNexus/nexus_ledger.db")

def query_verified_context(min_entropy=0.35, max_spectral_coherence=0.25, limit=10):
    """
    Selects knowledge nodes from the SQLite WAL ledger matching strict physical density bounds.
    - min_entropy: Rejects low-information repetitive noise (Z-axis).
    - max_spectral_coherence: Rejects single-frequency standing waves / DC-null patterns (Y-axis).
    """
    if not os.path.exists(DB_PATH):
        print(f"[!] Database not found at {DB_PATH}")
        return []

    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()
    cursor.execute("PRAGMA journal_mode=WAL;")

    query = """
    SELECT id, content, coord_x, spectral_coherence, entropy, fixity_seal
    FROM spatial_memory
    WHERE entropy >= ? AND spectral_coherence <= ?
    ORDER BY id ASC
    LIMIT ?;
    """
    
    cursor.execute(query, (min_entropy, max_spectral_coherence, limit))
    rows = cursor.fetchall()
    conn.close()
    return rows

if __name__ == "__main__":
    print("[*] Executing Zero-Trust Phase-Space Retrieval...")
    verified_nodes = query_verified_context()
    
    print(f"[+] Retrieved {len(verified_nodes)} Verified Ground-Truth Nodes:")
    for node in verified_nodes:
        print(f"  Node #{node[0]} | X: {node[2]:.2f} | SpecCoh: {node[3]:.4f} | H: {node[4]:.4f} | Seal: {node[5][:8]}")
        print(f"    Payload: \"{node[1]}\"")
