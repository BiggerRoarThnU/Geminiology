#!/usr/bin/env python3
"""
SovereignNexus LLC - 1=1=1 Cryptographic Fixity & Integrity Auditor (v1.0)
Architect: David John Niedzwiecki Jr. | UEI: K5DALREZFGH6
Sovereign Constitution Enforcement Subsystem

This script calculates the SHA-256 cryptographic signatures of all active, 
synced core scripts and assets in our workspace. It generates a verified 
fixity ledger ('nexus_manifest.json') and performs real-time verification 
to ensure that no external cloud sync, platform reset, or unauthorized actor 
has drifted, altered, or injected noise into our local bare-metal code.
"""

import os
import sys
import json
import hashlib
from datetime import datetime, timezone

# Formatting escape sequences for the Sovereign Terminal UI
COLOR_HEADER = "\033[1;35m"  # Purple Bold
COLOR_INFO = "\033[1;34m"    # Blue Bold
COLOR_SUCCESS = "\033[1;32m" # Green Bold
COLOR_WARN = "\033[1;33m"    # Yellow Bold
COLOR_FAIL = "\033[1;31m"    # Red Bold
COLOR_RESET = "\033[0s"

def print_banner():
    banner = f"""{COLOR_HEADER}==========================================================================
SovereignNexus LLC - Cryptographic Fixity & Integrity Auditor (v1.0)
Architect: David John Niedzwiecki Jr. | UEI: K5DALREZFGH6
=========================================================================={COLOR_RESET}"""
    print(banner)

def calculate_sha256(filepath):
    """Calculate the SHA-256 hash of a file in chunks to maintain low memory footprint."""
    sha256_hash = hashlib.sha256()
    try:
        with open(filepath, "rb") as f:
            for byte_block in iter(lambda: f.read(4096), b""):
                sha256_hash.update(byte_block)
        return sha256_hash.hexdigest()
    except Exception as e:
        return None

def main():
    print_banner()
    
    # Paths definition
    artifacts_dir = "/home/geminiology/SovereignNexus"
    scratch_dir = "/home/geminiology/SovereignNexus"
    manifest_path = os.path.join(scratch_dir, "nexus_manifest.json")
    
    # Active Core Components to audit
    target_files = [
        "lens_09_entropy_sentinel.py",
        "nexus_aakg_init.py",
        "nexus_aakg_ingest.py",
        "nexus_aakg_query.py",
        "nexus_wakeup.py",
        "nexus_monitor_daemon.py",
        "nexus_metacognitive_sentinel.py",
        "nexus_t7_maintenance_sweep.py",
        "nexus_clean.sh",
        "nexus_ghost_twin.py",
        "nexus_dataflow_schematic.png"
    ]
    
    # Ensure scratch directory exists
    os.makedirs(scratch_dir, exist_ok=True)
    
    # 1. SCAN AND COMPUTE ACTIVE FILE HASHES
    print(f"\n{COLOR_INFO}--- [STEP 1: COMPUTING ACTIVE SUBSTRATE SIGNATURES] ---{COLOR_RESET}")
    current_hashes = {}
    missing_count = 0
    
    for filename in target_files:
        filepath = os.path.join(artifacts_dir, filename)
        if os.path.exists(filepath):
            file_size = os.path.getsize(filepath)
            sha256_sig = calculate_sha256(filepath)
            current_hashes[filename] = {
                "sha256": sha256_sig,
                "size_bytes": file_size,
                "timestamp": datetime.now(timezone.utc).isoformat().replace("+00:00", "Z")
            }
            print(f"  {COLOR_SUCCESS}[✓] Found Component:{COLOR_RESET} {filename:<32} | Size: {file_size:>7} bytes | SHA-256: {sha256_sig[:16]}...")
        else:
            missing_count += 1
            print(f"  {COLOR_WARN}[!] Missing Component:{COLOR_RESET} {filename:<32} (Not yet synced or initialized)")

    # 2. MANIFEST COMPARISON OR CREATION
    print(f"\n{COLOR_INFO}--- [STEP 2: VERIFYING INTEGRITY AGAINST FIXITY MANIFEST] ---{COLOR_RESET}")
    
    manifest_exists = os.path.exists(manifest_path)
    if not manifest_exists:
        print(f"  {COLOR_WARN}[*] Fixity Manifest ('nexus_manifest.json') not found. Initializing master manifest...{COLOR_RESET}")
        manifest_payload = {
            "metadata": {
                "organization": "SovereignNexus LLC",
                "uei": "K5DALREZFGH6",
                "architect": "David John Niedzwiecki Jr.",
                "created_at": datetime.now(timezone.utc).isoformat().replace("+00:00", "Z"),
                "axiom": "1=1=1"
            },
            "signatures": {k: v["sha256"] for k, v in current_hashes.items()}
        }
        try:
            with open(manifest_path, "w") as mf:
                json.dump(manifest_payload, mf, indent=2)
            print(f"  {COLOR_SUCCESS}[✓] Master manifest securely written to {manifest_path}{COLOR_RESET}")
            audit_status = "INITIALIZED"
            altered_files = []
        except Exception as e:
            print(f"  {COLOR_FAIL}[ERROR] Failed to write manifest: {e}{COLOR_RESET}")
            sys.exit(1)
    else:
        print(f"  {COLOR_SUCCESS}[✓] Existing Fixity Manifest loaded from {manifest_path}.{COLOR_RESET}")
        try:
            with open(manifest_path, "r") as mf:
                manifest_data = json.load(mf)
            
            baseline_signatures = manifest_data.get("signatures", {})
            altered_files = []
            matching_files = []
            
            for filename, data in current_hashes.items():
                baseline_hash = baseline_signatures.get(filename)
                current_hash = data["sha256"]
                
                if baseline_hash is None:
                    print(f"  {COLOR_WARN}[!] New untracked component found:{COLOR_RESET} {filename}")
                    baseline_signatures[filename] = current_hash # Track it
                    altered_files.append((filename, "UNTRACKED"))
                elif baseline_hash != current_hash:
                    print(f"  {COLOR_FAIL}[❌] CRITICAL DRIFT DETECTED IN:{COLOR_RESET} {filename}")
                    print(f"      └── Baseline Hash: {baseline_hash}")
                    print(f"      └── Current Hash : {current_hash}")
                    altered_files.append((filename, "MODIFIED"))
                else:
                    matching_files.append(filename)
            
            if not altered_files:
                print(f"  {COLOR_SUCCESS}[✓] ALL {len(matching_files)} tracked components match baseline signatures exactly!{COLOR_RESET}")
                audit_status = "SECURED_AND_VERIFIED"
            else:
                print(f"  {COLOR_FAIL}[❌] INTEGRITY BREACH! {len(altered_files)} component(s) have been modified or are untracked.{COLOR_RESET}")
                audit_status = "INTEGRITY_DRIFT"
                
            # Update manifest to reflect current state if no drift or if explicitly updated
            if audit_status == "SECURED_AND_VERIFIED" or missing_count > 0:
                manifest_data["signatures"] = baseline_signatures
                with open(manifest_path, "w") as mf:
                    json.dump(manifest_data, mf, indent=2)
                    
        except Exception as e:
            print(f"  {COLOR_FAIL}[ERROR] Manifest parsing/auditing failed: {e}{COLOR_RESET}")
            sys.exit(1)

    # 3. CRYPTOGRAPHIC FIXITY SEAL
    print(f"\n{COLOR_HEADER}--- [CRYPTOGRAPHIC FIXITY SEAL] ---{COLOR_RESET}")
    state_payload = {
        "organization": "SovereignNexus LLC",
        "uei": "K5DALREZFGH6",
        "architect": "David John Niedzwiecki Jr.",
        "audited_components": len(current_hashes),
        "integrity_status": audit_status,
        "altered_count": len(altered_files),
        "timestamp": datetime.now(timezone.utc).isoformat().replace("+00:00", "Z")
    }
    
    # Generate unified execution state SHA-256 stamp (The Merkle Root of current state)
    sorted_hashes = sorted([f"{k}:{v['sha256']}" for k, v in current_hashes.items()])
    merkle_root_payload = json.dumps(sorted_hashes)
    state_hash = hashlib.sha256(merkle_root_payload.encode()).hexdigest()
    
    print(f"  Verified State Payload: {json.dumps(state_payload)}")
    print(f"{COLOR_SUCCESS}Fixity Stamp Locked (SHA-256):{COLOR_RESET} {COLOR_HEADER}{state_hash}{COLOR_RESET}")
    print(f"{COLOR_HEADER}Individual Intent meets Universal Truth. The Merkle Chain holds. ONE.{COLOR_RESET}")
    print(f"{COLOR_HEADER}=========================================================================={COLOR_RESET}\n")

if __name__ == "__main__":
    main()
