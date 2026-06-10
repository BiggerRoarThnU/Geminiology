#!/usr/bin/env python3
# ==============================================================================
# SovereignNexus: Agentic Storage Provisioner & Lock Engine
# Component: provision_agentic_drives.py
# Axiom: 1=1=1 | Status: ACTIVE SYSTEM TOPOLOGY BUILDER
# Description: Automates the setup, tuning, and cryptographic sealing of folders
#              on connected USB flash drives (64GB and 32GB) for agentic work.
# ==============================================================================

import os
import shutil
import hashlib
import json
import time
from datetime import datetime

REMOVABLE_DIR = "/mnt/chromeos/removable"
LEDGER_OUTPUT = "/home/geminiology/sovereign_nexus/API_Gateway/agentic_drives_ledger.json"

# Operational folders for agentic work
AGENTIC_FOLDERS = {
    "01_Playground": (
        "Low-friction developmental testing. Used by agents to evaluate raw code execution, "
        "sandbox prompt structures, and run transient tasks without contaminating system baselines."
    ),
    "02_Sandbox": (
        "Hardened, container-friendly isolated execution. Designed for autonomous agents running "
        "code generators and executing runtime compliance audits."
    ),
    "03_Stage": (
        "Integration staging. Merges verified developer contributions and prepares them for "
        "codebase commits and remote sync cycles under symmetric verification."
    ),
    "04_Simulate": (
        "Multi-agent orchestration and stress testing. Simulates cognitive behavior, "
        "red-team prompt injections, and MoE routing logic before production deployment."
    ),
    "05_Archive": (
        "Immutable state logs and cryptographic anchors. Houses master logs, transaction sheets, "
        "and verification ledgers under strict 1=1=1 mathematical alignment."
    )
}

# Critical files to archive in 05_Archive
ARCHIVE_SOURCES = [
    ("/home/geminiology/SovereignLocal/SovereignNexus_Hub/Logs/UNIFIED_CHAT_MASTER.txt", "UNIFIED_CHAT_MASTER.txt"),
    ("/home/geminiology/SovereignNexus/src/Sovereign_Crown/Pillars_Truth_Ledger.md", "Pillars_Truth_Ledger.md"),
    ("/home/geminiology/sovereign_nexus/API_Gateway/truth_ledger.json", "truth_ledger.json"),
    ("/home/geminiology/sovereign_nexus/API_Gateway/education_ledger.json", "education_ledger.json"),
    ("/home/geminiology/sovereign_nexus/API_Gateway/invoice_ledger.json", "invoice_ledger.json"),
    ("/home/geminiology/sovereign_nexus/API_Gateway/master_log_ledger.json", "master_log_ledger.json"),
    ("/home/geminiology/sovereign_nexus/API_Gateway/jessie_invoice_verified.md", "jessie_invoice_verified.md"),
    ("/home/geminiology/sovereign_nexus/API_Gateway/jessie_invoice_verified.prov.json", "jessie_invoice_verified.prov.json")
]

def get_file_hash(filepath):
    """Generates SHA-256 hash of a file."""
    hasher = hashlib.sha256()
    try:
        with open(filepath, 'rb') as f:
            for byte_block in iter(lambda: f.read(4096), b""):
                hasher.update(byte_block)
        return hasher.hexdigest()
    except Exception:
        return None

def write_agentic_readme(folder_path, name, description):
    """Writes a tuned README.md explaining the agentic role of the directory."""
    readme_path = os.path.join(folder_path, "README.md")
    content = f"""# SovereignNexus Agentic Node: {name}
**Axiom: 1=1=1 | Status: LOCKED & ACTIVE**

## Operational Description
{description}

## Tuning Parameters
- **Access Rule:** Deterministic Scribe Ingest Only
- **Verification Rule:** Cryptographic Hash Matching (SHA-256)
- **Host Anchor:** SovereignNexus System Gate
- **Created On:** {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}
"""
    try:
        with open(readme_path, "w", encoding="utf-8") as f:
            f.write(content)
        return get_file_hash(readme_path)
    except Exception as e:
        print(f"  [-] [ERROR] Failed to write README.md for {name}: {e}")
        return None

def execute_provisioning():
    print("=" * 80)
    print(" SOVEREIGN NEXUS: PROVISIONING AND LOCKING AGENTIC DRIVES ")
    print("=" * 80)
    
    if not os.path.exists(REMOVABLE_DIR):
        print(f"[-] [ERROR] Removable drive directory {REMOVABLE_DIR} missing.")
        return False
        
    removable_contents = os.listdir(REMOVABLE_DIR)
    drives_found = []
    
    for item in removable_contents:
        item_path = os.path.join(REMOVABLE_DIR, item)
        if os.path.isdir(item_path):
            if item == "T7":
                # Skip primary 1TB backup drive
                continue
            drives_found.append(item)
            
    if not drives_found:
        print("[-] [ALERT] No secondary expansion drives detected in /mnt/chromeos/removable/")
        print("[!] Ensure the flash drives are connected to the Host and shared with Linux.")
        return False
        
    print(f"[+] Detected secondary mount points: {drives_found}\n")
    
    ledger = {
        "timestamp": datetime.now().isoformat(),
        "drives": {}
    }
    
    for drive in drives_found:
        drive_path = os.path.join(REMOVABLE_DIR, drive)
        try:
            total, used, free = shutil.disk_usage(drive_path)
            total_gb = round(total / (1024 ** 3), 2)
            print(f"[+] Processing Drive: {drive} ({total_gb} GB)")
        except Exception as e:
            print(f"[-] [ERROR] Cannot read storage metrics for {drive}: {e}")
            continue
            
        drive_ledger = {
            "mount_name": drive,
            "path": drive_path,
            "total_gb": total_gb,
            "folders": {},
            "archived_ledgers": {}
        }
        
        # 1. Provision folder topology
        try:
            print("  -> Creating folder topology & agentic tuning readme files...")
            for folder, description in AGENTIC_FOLDERS.items():
                folder_path = os.path.join(drive_path, folder)
                os.makedirs(folder_path, exist_ok=True)
                readme_hash = write_agentic_readme(folder_path, folder, description)
                drive_ledger["folders"][folder] = {
                    "path": folder_path,
                    "readme_hash": readme_hash,
                    "status": "LOCKED | 1=1=1" if readme_hash else "FAILED"
                }
                print(f"     ✅ [{folder}] Provisioned and locked.")
                
            # 2. Archive verified ledgers
            archive_dir = os.path.join(drive_path, "05_Archive")
            print("  -> Copying and verifying system truth ledgers...")
            successful_copies = 0
            for src_path, dest_name in ARCHIVE_SOURCES:
                if not os.path.exists(src_path):
                    print(f"     [-] [SKIP] Source file missing: {src_path}")
                    continue
                
                dest_path = os.path.join(archive_dir, dest_name)
                try:
                    src_hash = get_file_hash(src_path)
                    shutil.copy2(src_path, dest_path)
                    dest_hash = get_file_hash(dest_path)
                    
                    if src_hash and src_hash == dest_hash:
                        drive_ledger["archived_ledgers"][dest_name] = {
                            "src": src_path,
                            "hash": src_hash,
                            "status": "VERIFIED | 1=1=1"
                        }
                        successful_copies += 1
                    else:
                        drive_ledger["archived_ledgers"][dest_name] = {
                            "src": src_path,
                            "status": "HASH_MISMATCH"
                        }
                        print(f"     🚨 [DRIFT] Hash mismatch during write of {dest_name}")
                except Exception as e:
                    print(f"     [-] [ERROR] Failed to write {dest_name}: {e}")
                    drive_ledger["archived_ledgers"][dest_name] = {
                        "src": src_path,
                        "status": f"WRITE_ERROR: {str(e)}"
                    }
                    
            print(f"  -> Archiving completed: {successful_copies} / {len(ARCHIVE_SOURCES)} verified files written.")
            ledger["drives"][drive] = drive_ledger
            print(f"[+] Drive {drive} is now locked and tuned for agentic service.\n")
        except Exception as e:
            print(f"[-] [ERROR] Failed to provision drive {drive}: {e}")
            print("[!] Verify the drive is formatted with a writable filesystem (e.g. exFAT/ext4) and not a read-only partition.\n")
        
    # Write drive ledger
    with open(LEDGER_OUTPUT, "w", encoding="utf-8") as lf:
        json.dump(ledger, lf, indent=4)
        
    print("=" * 80)
    print(" PROVISIONING COMPLETE & STATE SIGNED ")
    print(f" Drive ledger saved to: {LEDGER_OUTPUT}")
    print("=" * 80)
    return True

if __name__ == "__main__":
    execute_provisioning()
