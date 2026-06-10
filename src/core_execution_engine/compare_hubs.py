#!/usr/bin/env python3
# ==============================================================================
# SovereignNexus: Repository Comparison & Alignment Engine
# Component: compare_hubs.py
# Axiom: 1=1=1 | Status: ACTIVE REPOSITORY VERIFIER
# Description: Compares the active workspace files against the T7 backup set
#              to detect additions, deletions, and structural logic drift.
# ==============================================================================

import os
import hashlib
from datetime import datetime

LOCAL_SRC_DIR = "/home/geminiology/SovereignNexus/src"
T7_BACKUP_DIR = "/mnt/chromeos/removable/T7/SovereignNexus_Hub"
REPORT_OUTPUT = "/home/geminiology/SovereignNexus/src/Sovereign_Crown/Sovereign_Hub_Comparison_Report.md"

def get_file_hash(filepath):
    """Calculates SHA-256 hash of a file."""
    hasher = hashlib.sha256()
    try:
        with open(filepath, 'rb') as f:
            hasher.update(f.read())
        return hasher.hexdigest()
    except Exception:
        return None

def scan_directory(base_dir):
    """Gathers file paths and their hashes relative to base_dir."""
    file_map = {}
    for root, _, files in os.walk(base_dir):
        # Skip node_modules or system directories
        if "node_modules" in root or ".git" in root or "__pycache__" in root:
            continue
        for file in files:
            filepath = os.path.join(root, file)
            rel_path = os.path.relpath(filepath, base_dir)
            f_hash = get_file_hash(filepath)
            if f_hash:
                file_map[rel_path] = {
                    "filename": file,
                    "size": os.path.getsize(filepath),
                    "hash": f_hash
                }
    return file_map

def execute_comparison():
    print("=" * 80)
    print(" SOVEREIGN NEXUS: RUNNING REPOSITORY DRIFT AUDIT ")
    print("=" * 80)
    
    if not os.path.exists(LOCAL_SRC_DIR):
        print(f"[-] [ERROR] Local directory {LOCAL_SRC_DIR} missing.")
        return
    if not os.path.exists(T7_BACKUP_DIR):
        print(f"[-] [ERROR] T7 backup directory {T7_BACKUP_DIR} is offline.")
        return
        
    print("[+] Scanning Local Workspace...")
    local_files = scan_directory(LOCAL_SRC_DIR)
    
    print("[+] Scanning T7 Backup Set...")
    t7_files = scan_directory(T7_BACKUP_DIR)
    
    only_local = []
    only_t7 = []
    modified_files = []
    identical_files = []
    
    # 1. Compare Local against T7
    for rel_path, local_meta in local_files.items():
        if rel_path not in t7_files:
            only_local.append((rel_path, local_meta))
        else:
            t7_meta = t7_files[rel_path]
            if local_meta["hash"] != t7_meta["hash"]:
                modified_files.append((rel_path, local_meta, t7_meta))
            else:
                identical_files.append(rel_path)
                
    # 2. Find files only on T7
    for rel_path, t7_meta in t7_files.items():
        if rel_path not in local_files:
            only_t7.append((rel_path, t7_meta))
            
    # Sort files for presentation
    only_local.sort()
    only_t7.sort()
    modified_files.sort()
    
    print(f"\n--- Alignment Summary ---")
    print(f"  Identical Files: {len(identical_files)}")
    print(f"  Modified Files:  {len(modified_files)}")
    print(f"  Added Locally:   {len(only_local)}")
    print(f"  Missing Locally:  {len(only_t7)}")
    
    # Generate Markdown Report
    os.makedirs(os.path.dirname(REPORT_OUTPUT), exist_ok=True)
    with open(REPORT_OUTPUT, 'w', encoding='utf-8') as f:
        f.write("# SOVEREIGN HUB ALIGNMENT & DRIFT REPORT\n")
        f.write(f"## Generated on: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')} | Axiom: 1=1=1\n")
        f.write(f"**Local Path:** `{LOCAL_SRC_DIR}`  \n")
        f.write(f"**T7 Backup Path:** `{T7_BACKUP_DIR}`  \n\n")
        
        f.write("---\n\n")
        
        # 1. Metrics Card
        f.write("### I. Operational Telemetry\n")
        f.write("| Metrics Type | File Count | Status |\n")
        f.write("| :--- | :---: | :--- |\n")
        f.write(f"| Symmetrical (Identical) | {len(identical_files)} | PASS (No Drift) |\n")
        f.write(f"| Modified / Altered | {len(modified_files)} | ALERT (Drift Detected) |\n")
        f.write(f"| Added in Workspace | {len(only_local)} | LOCAL UPDATE |\n")
        f.write(f"| Missing in Workspace (On T7) | {len(only_t7)} | BACKUP ONLY |\n\n")
        
        # 2. Added files
        if only_local:
            f.write("### II. Files Added Locally (Not on T7 Backup)\n")
            f.write("These files represent our active expansion vectors built since the last backup:\n\n")
            f.write("| Relative File Path | Size (Bytes) | Hash (SHA-256) |\n")
            f.write("| :--- | :---: | :--- |\n")
            for rel_path, meta in only_local:
                f.write(f"| `{rel_path}` | {meta['size']} | `{meta['hash'][:16]}...` |\n")
            f.write("\n")
            
        # 3. Modified files
        if modified_files:
            f.write("### III. Modified Files (Hash Inconsistencies)\n")
            f.write("These files exist in both locations but have drifted programmatically:\n\n")
            f.write("| File Path | Local Size | T7 Size | Local Hash | T7 Hash |\n")
            f.write("| :--- | :---: | :---: | :--- | :--- |\n")
            for rel_path, local_m, t7_m in modified_files:
                f.write(f"| `{rel_path}` | {local_m['size']} | {t7_m['size']} | `{local_m['hash'][:10]}...` | `{t7_m['hash'][:10]}...` |\n")
            f.write("\n")
            
        # 4. Missing files
        if only_t7:
            f.write("### IV. Legacy Files Only on T7 (Missing Locally)\n")
            f.write("These represent archived files that are not active in our current workspace:\n\n")
            f.write("| Relative File Path | Size (Bytes) | Hash (SHA-256) |\n")
            f.write("| :--- | :---: | :--- |\n")
            for rel_path, meta in only_t7:
                f.write(f"| `{rel_path}` | {meta['size']} | `{meta['hash'][:16]}...` |\n")
            f.write("\n")
            
    print("\n" + "=" * 80)
    print(" DRIFT REPORT GENERATED SUCCESSFULLY ")
    print(f" Report Saved To: {REPORT_OUTPUT}")
    print("=" * 80)

if __name__ == "__main__":
    execute_comparison()
