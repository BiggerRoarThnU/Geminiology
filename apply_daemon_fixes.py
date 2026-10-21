#!/usr/bin/env python3
import os

print("[*] Initiating Substrate Patch Protocol...")

# 1. Expand nexus_core.py Schema
core_path = os.path.expanduser("~/SovereignNexus/src/nexus_core.py")
if os.path.exists(core_path):
    with open(core_path, "r") as f:
        content = f.read()
    
    if "assimilated_protocols" not in content:
        new_table_sql = """
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS assimilated_protocols (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            timestamp TEXT NOT NULL,
            protocol_name TEXT NOT NULL,
            source_file TEXT NOT NULL,
            sha256_hash TEXT UNIQUE NOT NULL,
            shannon_entropy REAL NOT NULL,
            slerp_coordinate_e8 TEXT NOT NULL,
            assimilated_payload TEXT NOT NULL,
            merkle_root_seal TEXT NOT NULL
        )
    ''')
    conn.commit()"""
        # Replace the final commit with the new table creation and a new commit
        content = content.replace("conn.commit()", new_table_sql)
        with open(core_path, "w") as f:
            f.write(content)
        print("[-] nexus_core.py schema expanded with 'assimilated_protocols' table.")

# 2. Fix missing sqlite3 import in Evolution Daemon
daemon_path = os.path.expanduser("~/SovereignNexus/src/nexus_evolution_daemon.py")
if os.path.exists(daemon_path):
    with open(daemon_path, "r") as f:
        content = f.read()
    
    if "import sqlite3" not in content:
        content = content.replace("import hashlib\n", "import hashlib\nimport sqlite3\n")
        with open(daemon_path, "w") as f:
            f.write(content)
        print("[-] nexus_evolution_daemon.py patched with 'import sqlite3'.")

print("[✓] Patches applied successfully.")
