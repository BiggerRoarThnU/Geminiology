#!/usr/bin/env python3
# ==============================================================================
# SovereignNexus: Repository Synchronizer & Backup Refiner
# Component: sync_workspace_to_t7.py
# Axiom: 1=1=1 | Status: ACTIVE SYNCHRONIZATION ENGINE
# Description: Safely updates the T7 backup copy with active local workspace
#              files, verifying all operations with SHA-256 fixity checks.
# ==============================================================================

import os
import shutil
import hashlib
from datetime import datetime

LOCAL_SRC_DIR = "/home/geminiology/SovereignNexus/src"
T7_BACKUP_DIR = "/mnt/chromeos/removable/T7/SovereignNexus_Hub"

def get_file_hash(filepath):
    """Calculates SHA-256 hash of a file."""
    hasher = hashlib.sha256()
    try:
        with open(filepath, 'rb') as f:
            hasher.update(f.read())
        return hasher.hexdigest()
    except Exception:
        return None

def execute_sync():
    print("=" * 80)
    print(" SOVEREIGN NEXUS: SYNCHRONIZING WORKSPACE TO T7 BACKUP ")
    print("=" * 80)
    
    if not os.path.exists(LOCAL_SRC_DIR):
        print(f"[-] [ERROR] Local source directory {LOCAL_SRC_DIR} missing.")
        return False
    if not os.path.exists(T7_BACKUP_DIR):
        print(f"[-] [ERROR] T7 backup target directory {T7_BACKUP_DIR} is offline.")
        return False
        
    print(f"[+] Syncing files from: {LOCAL_SRC_DIR}")
    print(f"[+] Syncing files to:   {T7_BACKUP_DIR}\n")
    
    files_updated = 0
    files_added = 0
    identical_count = 0
    failed_count = 0
    
    for root, dirs, files in os.walk(LOCAL_SRC_DIR):
        # Exclude node_modules, git assets, and cache files
        if any(ignored in root for ignored in ["node_modules", ".git", "__pycache__"]):
            continue
            
        for file in files:
            src_filepath = os.path.join(root, file)
            rel_path = os.path.relpath(src_filepath, LOCAL_SRC_DIR)
            dest_filepath = os.path.join(T7_BACKUP_DIR, rel_path)
            
            src_hash = get_file_hash(src_filepath)
            if not src_hash:
                continue
                
            dest_hash = None
            if os.path.exists(dest_filepath):
                dest_hash = get_file_hash(dest_filepath)
                
            # If target exists and hash matches, no action needed
            if dest_hash and src_hash == dest_hash:
                identical_count += 1
                continue
                
            # Copy file
            try:
                dest_dir = os.path.dirname(dest_filepath)
                os.makedirs(dest_dir, exist_ok=True)
                
                shutil.copy2(src_filepath, dest_filepath)
                verify_hash = get_file_hash(dest_filepath)
                
                # 1=1=1 alignment check
                if src_hash == verify_hash:
                    if dest_hash:
                        print(f"  [UPDATED] {rel_path} | Size: {os.path.getsize(src_filepath)} bytes")
                        files_updated += 1
                    else:
                        print(f"  [ADDED]   {rel_path} | Size: {os.path.getsize(src_filepath)} bytes")
                        files_added += 1
                else:
                    print(f"  [X] [DRIFT] Hash mismatch during copy of: {rel_path}")
                    failed_count += 1
            except Exception as e:
                print(f"  [X] [ERROR] Failed to sync {rel_path}: {str(e)}")
                failed_count += 1
                
    print("\n" + "=" * 80)
    print(" SYNCHRONIZATION EXECUTION SUMMARY ")
    print(f" Symmetrical Files (Unchanged): {identical_count}")
    print(f" Files Added to Backup:         {files_added}")
    print(f" Files Updated in Backup:       {files_updated}")
    print(f" Operations Failed:             {failed_count}")
    print("=" * 80)
    return True

if __name__ == "__main__":
    execute_sync()
