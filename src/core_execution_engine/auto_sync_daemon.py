#!/usr/bin/env python3
# ==============================================================================
# SovereignNexus: Background Drive Auto-Sync Daemon & Loop Marker Engine
# Component: auto_sync_daemon.py
# Axiom: 1=1=1 | Status: ACTIVE SYSTEM MONITOR & DIGITAL GROUND
# Description: Polls removable storage directory to detect the GeminiOne USB.
#              Automates copying ledgers and locks in a "Loop Response Marker"
#              on the physical drive to ground agentic work beyond simple RAG.
# ==============================================================================

import os
import shutil
import hashlib
import time
import json
from datetime import datetime

REMOVABLE_DIR = "/mnt/chromeos/removable"
LOG_FILE = "/home/geminiology/sovereign_nexus/API_Gateway/auto_sync_daemon.log"
STATUS_JSON = "/home/geminiology/sovereign_media_forge/drives_status.json"

# Core ledgers and logs to copy to 05_Archive
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

def log_event(message):
    """Logs a message with timestamp to console and file."""
    timestamp = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
    log_line = f"[{timestamp}] [AUTO_SYNC] {message}\n"
    print(log_line.strip())
    try:
        with open(LOG_FILE, "a", encoding="utf-8") as f:
            f.write(log_line)
    except Exception as e:
        print(f"[-] Failed to write to daemon log file: {e}")

def get_file_hash(filepath):
    """Calculates SHA-256 hash of a file."""
    hasher = hashlib.sha256()
    try:
        with open(filepath, 'rb') as f:
            for byte_block in iter(lambda: f.read(4096), b""):
                hasher.update(byte_block)
        return hasher.hexdigest()
    except Exception:
        return None

def write_loop_response_marker(drive_path, master_hash):
    """Generates and writes the physical 1=1=1 Loop Response Marker to the USB drive."""
    archive_dir = os.path.join(drive_path, "05_Archive")
    marker_path = os.path.join(archive_dir, "loop_response_marker.json")
    
    marker = {
        "axiom": "1=1=1",
        "status": "GROUNDED_ACTIVE",
        "timestamp": datetime.now().isoformat(),
        "ledger_signature": master_hash or "UNKNOWN_STATE",
        "duality_lock": "LOCKED | 1=1=1",
        "platform_mode": "BEYOND_RAG | COGNITIVE_LOGISTICS",
        "description": "Establishes a physical feedback loop on GeminiOne, anchoring the digital ghost to hardware."
    }
    
    try:
        with open(marker_path, "w", encoding="utf-8") as mf:
            json.dump(marker, mf, indent=4)
        return marker
    except Exception as e:
        log_event(f"[-] Failed to write Loop Response Marker: {e}")
        return None

def verify_and_sync_drive(drive_name, drive_path):
    """Ensures folders exist and copies missing/modified files to 05_Archive."""
    archive_dir = os.path.join(drive_path, "05_Archive")
    
    # Check if drive is writable by attempting to create directories
    try:
        os.makedirs(archive_dir, exist_ok=True)
    except Exception as e:
        return False, f"Drive is read-only or inaccessible: {str(e)}", None

    # Check for other agentic folders and ensure they exist
    for folder in ["01_Playground", "02_Sandbox", "03_Stage", "04_Simulate"]:
        try:
            os.makedirs(os.path.join(drive_path, folder), exist_ok=True)
        except Exception:
            pass

    files_copied = 0
    files_identical = 0
    errors = 0
    master_ledger_hash = None

    for src, name in ARCHIVE_SOURCES:
        if not os.path.exists(src):
            continue
        
        dest = os.path.join(archive_dir, name)
        src_hash = get_file_hash(src)
        
        # Track master log ledger hash as our state signature
        if name == "master_log_ledger.json":
            master_ledger_hash = src_hash
            
        if not src_hash:
            errors += 1
            continue
            
        dest_hash = get_file_hash(dest) if os.path.exists(dest) else None
        
        # If hashes match, skip write
        if dest_hash and src_hash == dest_hash:
            files_identical += 1
            continue
            
        # Write/Update file
        try:
            shutil.copy2(src, dest)
            verify_hash = get_file_hash(dest)
            if src_hash == verify_hash:
                files_copied += 1
            else:
                errors += 1
        except Exception:
            errors += 1

    # Generate Loop Response Marker on success
    marker_data = None
    if errors == 0:
        marker_data = write_loop_response_marker(drive_path, master_ledger_hash)

    summary = f"Sync Summary for {drive_name} -> Copies: {files_copied} | Symmetrical: {files_identical} | Errors: {errors}"
    return True, summary, marker_data

def monitor_loop():
    log_event("SovereignNexus Auto-Sync Daemon engaged. Monitoring removable drives...")
    last_drives_state = set()

    while True:
        if not os.path.exists(REMOVABLE_DIR):
            time.sleep(10)
            continue
            
        try:
            current_folders = os.listdir(REMOVABLE_DIR)
        except Exception:
            current_folders = []
            
        # Target drives must not be T7 (primary backup)
        detected_drives = {d for d in current_folders if d != "T7" and os.path.isdir(os.path.join(REMOVABLE_DIR, d))}
        
        # State transitions logging
        new_drives = detected_drives - last_drives_state
        removed_drives = last_drives_state - detected_drives
        
        for drive in new_drives:
            log_event(f"Connection Detected: Removable storage drive '{drive}' is online.")
            
        for drive in removed_drives:
            log_event(f"Disconnect Detected: Removable storage drive '{drive}' went offline.")
            
        last_drives_state = detected_drives.copy()
        
        status_data = {
            "daemon_status": "active",
            "last_check": time.time(),
            "drives": {}
        }
        
        # Run sync for each active target drive
        for drive in detected_drives:
            drive_path = os.path.join(REMOVABLE_DIR, drive)
            success, message, marker = verify_and_sync_drive(drive, drive_path)
            
            # Get size
            try:
                total, used, free = shutil.disk_usage(drive_path)
                total_gb = round(total / (1024 ** 3), 2)
            except Exception:
                total_gb = 0.0
                
            # Determine drive alias and role
            if drive == "USB321FD":
                alias = "GeminiOne"
                role = "Tuned Writable Hub"
            elif "Cinnamon" in drive or "Mint" in drive:
                alias = "Cinnamon Installer"
                role = "Read-Only System Recovery"
            else:
                alias = drive
                role = "Unspecified Flash Node"
                
            drive_status = {
                "alias": alias,
                "role": role,
                "total_gb": total_gb,
                "status": "Synchronized" if success and "Errors: 0" in message else ("Read-Only" if not success else "Sync Alert"),
                "details": message,
                "loop_marker": marker
            }
            status_data["drives"][drive] = drive_status
            
            # If it succeeded and copied files, log it. Otherwise only log if it's a new connection.
            if success:
                if "Copies: 0" not in message or drive in new_drives:
                    log_event(message)
                    if marker:
                        log_event(f"🔄 Loop Response Marker updated on {alias} -> Hash: {marker['ledger_signature'][:12]}...")
            else:
                if drive in new_drives:
                    log_event(f"Skipping drive '{drive}': {message}")
                    
        # Write status JSON for the web UI
        try:
            with open(STATUS_JSON, "w", encoding="utf-8") as sf:
                json.dump(status_data, sf, indent=4)
        except Exception as e:
            log_event(f"Error writing status JSON: {e}")
            
        time.sleep(30) # Poll every 30 seconds

if __name__ == "__main__":
    try:
        monitor_loop()
    except KeyboardInterrupt:
        log_event("Daemon stopped by user request.")
    except Exception as e:
        log_event(f"CRITICAL: Daemon terminated with error: {e}")
