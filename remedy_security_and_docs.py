#!/usr/bin/env python3
import os
import re

print("[*] Initiating Phase 2: Security Crumbs & README Honesty...")

def patch_file(filepath, replacements):
    path = os.path.expanduser(filepath)
    if not os.path.exists(path):
        print(f"[-] Skipped (not found): {filepath}")
        return
        
    with open(path, "r") as f:
        content = f.read()
    
    modified = False
    for old, new in replacements:
        if old in content:
            content = content.replace(old, new)
            modified = True
            
    if modified:
        with open(path, "w") as f:
            f.write(content)
        print(f"[✓] Patched: {filepath}")

# 1. Scrub Family Names & LAN IPs from Sentinel
sentinel_replacements = [
    ("Makai", "[REDACTED_FAMILY_M]"),
    ("Yariah", "[REDACTED_FAMILY_Y]"),
    ("Jessica", "[REDACTED_FAMILY_J]"),
    ("192.168.12.32", '127.0.0.1'),
    ("192.168.12.153", '127.0.0.1'),
    ("100.115.92.195", '127.0.0.1')
]
patch_file("~/SovereignNexus/src/nexus_metacognitive_sentinel.py", sentinel_replacements)

# 2. Remove burned token placeholder from Oracle Server HTML
oracle_replacements = [
    ('value="NEXUS-777-ALPHA"', 'value="" placeholder="ENTER_TOKEN"')
]
patch_file("~/SovereignNexus/src/oracle_server.py", oracle_replacements)

# 3. Secure the final missed salt in Baby Gemma
bg_replacements = [
    ('"the scratch of your heart in ring 💖"', 'os.environ.get("NEXUS_SALT", "default_secure_salt")')
]
patch_file("~/SovereignNexus/src/baby_gemma_engine.py", bg_replacements)

# 4. README Honesty Alignment
readme_replacements = [
    ("252k QPS", "[Benchmarking QPS TBD]"),
    ("zero dependencies", "minimal edge-optimized dependencies (see pyproject.toml)"),
    ("Proves that Beam", "Simulates Beam")
]
patch_file("~/SovereignNexus/README.md", readme_replacements)

print("[*] Phase 2 complete.")
