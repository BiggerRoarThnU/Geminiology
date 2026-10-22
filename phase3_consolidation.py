#!/usr/bin/env python3
import os
import re

print("[*] Initiating Phase 3: Final Consolidation...")

def regex_patch(filepath, pattern, replacement):
    path = os.path.expanduser(filepath)
    if not os.path.exists(path): return
    with open(path, 'r') as f: content = f.read()
    new_content = re.sub(pattern, replacement, content, flags=re.DOTALL | re.IGNORECASE)
    if new_content != content:
        with open(path, 'w') as f: f.write(new_content)
        print(f"[✓] Patched: {filepath}")

# 1. Clean up Phase 2 Misses (Flexible Regex)
regex_patch("~/SovereignNexus/src/oracle_server.py", r'value=[\"\']NEXUS-777-ALPHA[\"\']', 'value="" placeholder="ENTER_TOKEN"')
regex_patch("~/SovereignNexus/README.md", r'252k QPS', '[Benchmarking QPS TBD]')
regex_patch("~/SovereignNexus/README.md", r'zero dependencies', 'minimal edge-optimized dependencies')
regex_patch("~/SovereignNexus/README.md", r'Proves that Beam', 'Simulates Beam')

# 2. Delete Legacy Swarm Router
legacy_router = os.path.expanduser("~/SovereignNexus/swarm_router.py")
if os.path.exists(legacy_router):
    os.remove(legacy_router)
    print("[✓] Legacy root swarm_router.py removed.")

# 3. Fix ru_maxrss metric in mmap module (Linux KB to MB)
regex_patch("~/SovereignNexus/src/nexus_mmap_page.py", r'ru_maxrss\s*/\s*\(1024\s*\*\s*1024\)', 'ru_maxrss / 1024')

# 4. Prune duplicated entropy function from Vanguard
regex_patch("~/SovereignNexus/src/nexus_vanguard_master.py", r'def calculate_shannon_entropy[^:]+:.*?return entropy\n', '')

# 5. Fix run_full_test_suite.sh
test_sh = os.path.expanduser("~/SovereignNexus/run_full_test_suite.sh")
with open(test_sh, 'w') as f:
    f.write("#!/bin/bash\nexport PYTHONPATH=src\npython3 -m unittest discover -s src\n")
os.chmod(test_sh, 0o755)
print("[✓] run_full_test_suite.sh rebuilt and configured.")

print("[*] Phase 3 Complete. The Sovereign Framework is fully aligned.")
