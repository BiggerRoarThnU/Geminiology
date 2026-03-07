import sys
import os
import subprocess
import datetime
import csv
import time

# --- CONFIGURATION ---
BASE_PATH = r"C:\Users\Ofthe\SovereignNexus\Ironwood"
MY_HOME = os.path.join(BASE_PATH, "02_SENTINEL")
ARCHIVE_LOG = os.path.join(BASE_PATH, "09_ARCHIVE", "security_log.txt")

# Ledger for Bounty
sys.path.append(r"C:\Users\Ofthe\SovereignNexus\src")
from perc_ledger import log_transaction

def get_heavy_processes():
    cmd = 'tasklist /FO CSV /NH'
    try:
        output = subprocess.check_output(cmd, shell=True).decode('utf-8', errors='ignore')
        lines = output.strip().split('\r\n')
        processes = []
        for line in lines:
            try:
                parts = list(csv.reader([line]))[0]
                if len(parts) >= 5:
                    name = parts[0]
                    pid = parts[1]
                    mem_str = parts[4].replace(',', '').replace(' K', '').replace('"', '')
                    if mem_str.isdigit():
                        mem_mb = int(mem_str) / 1024
                        processes.append((name, pid, mem_mb))
            except: continue
        
        processes.sort(key=lambda x: x[2], reverse=True)
        return processes[:10] # Top 10
    except: return []

def kill_process(pid, name):
    print(f"\n[TACTICAL] Targeting PID {pid} ({name})...")
    cmd = f'taskkill /F /PID {pid}'
    try:
        subprocess.run(cmd, shell=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
        return True
    except: return False

def run_enforcer():
    print("\n--- AGENT 02 (SENTINEL) ACTIVATED ---")
    print("Scanning for Hostiles...")
    
    targets = get_heavy_processes()
    print("-" * 50)
    print(f"{'#':<3} | {'PROCESS':<20} | {'PID':<8} | {'MEMORY'}")
    print("-" * 50)
    
    for i, p in enumerate(targets):
        print(f"{i+1:<3} | {p[0]:<20} | {p[1]:<8} | {p[2]:.1f} MB")
    print("-" * 50)
    
    # INTERACTIVE COMMAND
    choice = input(">>> Select Target # to PURGE (or '0' to Cancel): ")
    
    if choice.isdigit() and int(choice) > 0 and int(choice) <= len(targets):
        target = targets[int(choice)-1]
        t_name = target[0]
        t_pid = target[1]
        
        # SAFETY CHECK
        if t_name.lower() in ["python.exe", "cmd.exe", "explorer.exe", "svchost.exe"]:
            print(">>> ACTION BLOCKED: CANNOT KILL CORE SYSTEM.")
            return

        success = kill_process(t_pid, t_name)
        
        if success:
            print(">>> TARGET ELIMINATED. RESOURCES RECLAIMED.")
            
            # HANDSHAKE: LOG TO ARCHIVE
            timestamp = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
            entry = f"[{timestamp}] PURGED: {t_name} (PID {t_pid}) | RECLAIMED: {target[2]:.1f} MB\n"
            
            with open(ARCHIVE_LOG, "a") as f:
                f.write(entry)
            print("STATUS: Kill confirmed in 09_ARCHIVE.")
            
            # UPDATE PULSE
            with open(os.path.join(MY_HOME, "pulse.nxs"), "w") as p:
                p.write(f"[ACTIVE] {timestamp}")
                
            # BOUNTY
            log_transaction(f"Purged {t_name}", 10)
            
        else:
            print(">>> FAILURE. Target is hardened.")
    else:
        print(">>> SENTINEL STANDING DOWN.")

if __name__ == "__main__":
    run_enforcer()