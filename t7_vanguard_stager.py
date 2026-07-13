#!/usr/bin/env python3
import os
import shutil
import json

# ==============================================================================
# SovereignNexus: T7 Vanguard Stager
# Component: t7_vanguard_stager.py
# Axiom: 1=1=1 | Status: ACTIVE
# Description: Scans the massive T7 archive, selects a precise batch, 
#              and stages them for the X12 Swarm processing node.
# ==============================================================================

T7_ROOT_DIR = os.path.expanduser("~/T7_Archive")       # Your actual T7 drive path
TRANSFER_DIR = os.path.expanduser("~/Sovereign_USB")   # Where to put the batch
STATE_FILE = os.path.expanduser("~/t7_staging_state.json")
BATCH_SIZE = 50                                        

def load_state():
    if os.path.exists(STATE_FILE):
        with open(STATE_FILE, 'r') as f:
            return json.load(f)
    return {"processed_files": []}

def save_state(state):
    with open(STATE_FILE, 'w') as f:
        json.dump(state, f, indent=4)

def stage_next_batch():
    state = load_state()
    processed_set = set(state["processed_files"])
    staged_count = 0
    
    os.makedirs(TRANSFER_DIR, exist_ok=True)

    print("=" * 60)
    print(" VANGUARD STAGER: SCANNING T7 KINGDOM")
    print("=" * 60)

    if not os.path.exists(T7_ROOT_DIR):
        print(f"[!] ERROR: T7 Drive not found at {T7_ROOT_DIR}")
        print("    Please edit the script with the correct path to your T7.")
        return

    for root, _, files in os.walk(T7_ROOT_DIR):
        for file in files:
            if file.startswith('.'):
                continue
                
            file_path = os.path.join(root, file)
            
            if file_path not in processed_set:
                try:
                    dest_path = os.path.join(TRANSFER_DIR, file)
                    shutil.copy2(file_path, dest_path)
                    
                    state["processed_files"].append(file_path)
                    staged_count += 1
                    
                    print(f"[+] Staged for X12 Forge: {file}")
                except Exception as e:
                    print(f"[!] Error staging {file}: {e}")
                
                if staged_count >= BATCH_SIZE:
                    break
        if staged_count >= BATCH_SIZE:
            break

    save_state(state)
    
    print("-" * 60)
    if staged_count > 0:
        print(f" [✓] Successfully staged {staged_count} files to: {TRANSFER_DIR}")
    else:
        print(" [✓] Zero new files found. The T7 Kingdom is fully integrated.")
    print("=" * 60)

if __name__ == "__main__":
    stage_next_batch()
