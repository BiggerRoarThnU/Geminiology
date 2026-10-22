#!/usr/bin/env python3
import os
import re

print("[*] Initiating Core Wiring Protocol...")

# 1. Update Core with the true Royal Seal 2.5-5.2 Entropy Band
core_path = os.path.expanduser("~/SovereignNexus/src/nexus_core.py")
if os.path.exists(core_path):
    with open(core_path, "r") as f: content = f.read()
    content = re.sub(
        r'def verify_entropy_gate.*?(?=def get_unified_db_connection)',
        '''def verify_entropy_gate(text: str) -> bool:
    """
    Unified Lens 09 Rule: Enforces the Royal Seal standard (2.5 - 5.2).
    """
    h = calculate_shannon_entropy(text)
    return 2.5 <= h <= 5.2\n\n''',
        content, flags=re.DOTALL
    )
    with open(core_path, "w") as f: f.write(content)
    print("[-] nexus_core.py updated to strict 2.5-5.2 entropy band.")

# 2. Wire Vanguard Master: Import core, update INSERT columns
vanguard_path = os.path.expanduser("~/SovereignNexus/src/nexus_vanguard_master.py")
if os.path.exists(vanguard_path):
    with open(vanguard_path, "r") as f: content = f.read()
    if "from nexus_core import" not in content:
        content = "from nexus_core import get_unified_db_connection, verify_entropy_gate\n" + content
    # Replace individual sqlite3.connect with unified core connection
    content = re.sub(r'sqlite3\.connect\([^\)]+\)', 'get_unified_db_connection()', content)
    # Fix the INSERT statement to match the new schema
    content = content.replace(
        "(node_id, node_name, log_text, payload_hash, signature)",
        "(node_id, node_name, log_content, log_hash, signature)"
    )
    with open(vanguard_path, "w") as f: f.write(content)
    print("[-] Vanguard wired to core and schema patched.")

# 3. Wire Discovery Lens: Import core, update INSERT columns
discovery_path = os.path.expanduser("~/SovereignNexus/src/nexus_discovery_lens.py")
if os.path.exists(discovery_path):
    with open(discovery_path, "r") as f: content = f.read()
    if "from nexus_core import" not in content:
        content = "from nexus_core import get_unified_db_connection, verify_entropy_gate\n" + content
    content = re.sub(r'sqlite3\.connect\([^\)]+\)', 'get_unified_db_connection()', content)
    content = content.replace(
        "(node_id, node_name, log_text, payload_hash, signature)",
        "(node_id, node_name, log_content, log_hash, signature)"
    )
    with open(discovery_path, "w") as f: f.write(content)
    print("[-] Discovery Lens wired to core and schema patched.")

# 4. Wire Swarm Router: Import core connection
router_path = os.path.expanduser("~/SovereignNexus/src/nexus_swarm_router.py")
if os.path.exists(router_path):
    with open(router_path, "r") as f: content = f.read()
    if "from nexus_core import" not in content:
        content = "from nexus_core import get_unified_db_connection\n" + content
    content = re.sub(r'sqlite3\.connect\([^\)]+\)', 'get_unified_db_connection()', content)
    with open(router_path, "w") as f: f.write(content)
    print("[-] Swarm Router wired to unified core connection.")

print("[✓] Core Wiring Complete. The engine is now connected to the transmission.")
