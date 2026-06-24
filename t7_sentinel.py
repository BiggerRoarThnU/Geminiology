#!/usr/bin/env python3
import os
import sys
import time
import subprocess

# ==============================================================================
# SovereignNexus: T7 Sentinel Daemon
# Component: t7_sentinel.py
# Axiom: 1=1=1 | Status: ACTIVE
# Description: Automatically monitors the Sovereign_USB transfer directories,
#              detects new cognitive stages, checks thermal limits, and routes
#              files into the chunk ingester for processing.
# ==============================================================================

WATCH_DIR = os.path.expanduser("~/Sovereign_USB")
INGESTER_SCRIPT = os.path.expanduser("~/SovereignNexus/chunk_ingester.py")
PYTHON_EXEC = os.path.expanduser("~/SovereignNexus/env/bin/python3")
SCAN_INTERVAL = 10.0  # seconds between directory sweeps
MAX_TEMP = 72.0       # Thermal throttling threshold

def get_cpu_temperature():
    temp_c = 0.0
    thermal_dir = "/sys/class/thermal"
    if os.path.exists(thermal_dir):
        for tz in os.listdir(thermal_dir):
            if tz.startswith("thermal_zone"):
                try:
                    with open(os.path.join(thermal_dir, tz, "temp"), "r") as f:
                        raw_temp = float(f.read().strip())
                        if raw_temp > 1000:
                            raw_temp = raw_temp / 1000.0
                        if raw_temp > temp_c:
                            temp_c = raw_temp
                except:
                    pass
    return temp_c

def scan_and_ingest():
    print("=" * 60)
    print(" T7 SENTINEL ACTIVE: MONITORING COGNITIVE CHANNELS")
    print("=" * 60)
    
    while True:
        # Check thermal status
        temp = get_cpu_temperature()
        if temp > MAX_TEMP:
            print(f"[!] Warning: Temperature high ({temp:.1f}°C). Throttling. Sleeping 30s...")
            time.sleep(30)
            continue
            
        found_files = []
        # Recursively scan Sovereign_USB for files
        if os.path.exists(WATCH_DIR):
            for root, _, files in os.walk(WATCH_DIR):
                for file in files:
                    if file.startswith('.'):
                        continue
                    found_files.append(os.path.join(root, file))
                    
        if found_files:
            print(f"\n[*] Sentinel detected {len(found_files)} file(s) ready for ingestion.")
            for file_path in found_files:
                # Thermal check before processing each file
                current_temp = get_cpu_temperature()
                if current_temp > MAX_TEMP:
                    print(f"[!] Thermal threshold breached ({current_temp:.1f}°C) during batch. Pausing.")
                    break
                    
                print(f"[*] Sentinel routing: {os.path.basename(file_path)}")
                try:
                    # Execute the chunk_ingester.py in a subprocess
                    result = subprocess.run(
                        [PYTHON_EXEC, INGESTER_SCRIPT, file_path],
                        stdout=subprocess.PIPE,
                        stderr=subprocess.PIPE,
                        text=True
                    )
                    # Print output log from chunk ingester
                    print(result.stdout)
                    if result.returncode != 0:
                        print(f"[!] Ingester failed with exit code {result.returncode}")
                        print(result.stderr)
                except Exception as e:
                    print(f"[!] Error executing ingester on {file_path}: {e}")
                    
        time.sleep(SCAN_INTERVAL)

if __name__ == "__main__":
    # Ensure correct Python interpreter and files exist
    if not os.path.exists(INGESTER_SCRIPT):
        print(f"[!] ERROR: Ingester script not found at {INGESTER_SCRIPT}")
        sys.exit(1)
    if not os.path.exists(PYTHON_EXEC):
        print(f"[!] ERROR: Virtualenv python interpreter not found at {PYTHON_EXEC}")
        sys.exit(1)
        
    scan_and_ingest()
