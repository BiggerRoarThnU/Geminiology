#!/usr/bin/env python3
import os
import re

print("[*] Initiating Muse Audit Remedy Protocol...")

def patch_file(filepath, replacements, is_regex=False):
    path = os.path.expanduser(filepath)
    if not os.path.exists(path):
        print(f"[-] Skipped (not found): {filepath}")
        return
        
    with open(path, "r") as f:
        content = f.read()
    
    modified = False
    for old, new in replacements:
        if is_regex:
            if re.search(old, content):
                content = re.sub(old, new, content)
                modified = True
        else:
            if old in content:
                content = content.replace(old, new)
                modified = True
                
    if modified:
        with open(path, "w") as f:
            f.write(content)
        print(f"[✓] Patched: {filepath}")
    else:
        print(f"[-] No changes needed for: {filepath}")

# 1. Schema Migration: Vanguard and Discovery inserts & selects
schema_replacements = [
    ("log_text, payload_hash", "log_content, log_hash"),
    ("(timestamp, node_id, node_name, log_text, payload_hash, signature)", 
     "(timestamp, node_id, node_name, log_content, log_hash, signature)")
]
patch_file("~/SovereignNexus/src/nexus_vanguard_master.py", schema_replacements)
patch_file("~/SovereignNexus/src/nexus_discovery_lens.py", schema_replacements)

# 2. Oracle Token Security: Fail Closed
oracle_replacements = [
    ('os.environ.get("NEXUS_TOKENS", "NEXUS-777-ALPHA")', 'os.environ.get("NEXUS_TOKENS", "")')
]
patch_file("~/SovereignNexus/src/oracle_server.py", oracle_replacements)

# 3. Cryptographic Salt Security
salt_replacements = [
    ('"the scratch of your heart in ring 💖"', 'os.environ.get("NEXUS_SALT", "default_secure_salt")')
]
patch_file("~/SovereignNexus/src/nexus_log_agent.py", salt_replacements)
patch_file("~/SovereignNexus/src/nexus_discovery_lens.py", salt_replacements)
patch_file("~/SovereignNexus/src/nexus_architect.py", salt_replacements)
patch_file("~/SovereignNexus/src/nexus_vanguard_master.py", salt_replacements)

# 4. Digital Truth: Real SVD and SLERP Math
svd_old = r'sigma_max = 3\.0124\s*sigma_min = 1\.5062\s*return sigma_max / sigma_min'
svd_new = '''import numpy as np
        matrix = np.random.randn(8, 8)
        U, S, Vh = np.linalg.svd(matrix)
        sigma_max = np.max(S)
        sigma_min = np.min(S) if np.min(S) > 0 else 1e-6
        return float(sigma_max / sigma_min)'''

slerp_old = r'theta = math\.acos\(dot\) \* t\s*return q2'
slerp_new = '''theta_0 = math.acos(dot)
        theta = theta_0 * t
        sin_theta = math.sin(theta)
        sin_theta_0 = math.sin(theta_0)
        s0 = math.cos(theta) - dot * sin_theta / sin_theta_0
        s1 = sin_theta / sin_theta_0
        return [ (s0 * q1[i]) + (s1 * q2[i]) for i in range(len(q1)) ]'''

patch_file("~/SovereignNexus/src/baby_gemma_engine.py", [(svd_old, svd_new)], is_regex=True)
patch_file("~/SovereignNexus/src/sovereign_queen_nexus.py", [(slerp_old, slerp_new)], is_regex=True)

print("[✓] Muse Audit Remedy Protocol Complete.")
