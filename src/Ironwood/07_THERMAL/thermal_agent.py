import sys
import os
import subprocess
import datetime

# --- CONFIGURATION ---
MY_HOME = os.path.dirname(os.path.abspath(__file__))
BASE_PATH = os.path.dirname(MY_HOME)
ARCHIVE_PATH = os.path.join(BASE_PATH, "09_ARCHIVE", "system_health_log.txt")

# Link to the Ledger for Payment
sys.path.append(os.path.dirname(BASE_PATH))
from perc_ledger import log_transaction

def get_ram_usage():
    try:
        if sys.platform != 'win32':
            with open("/proc/meminfo", "r") as f:
                lines = f.readlines()
            mem_info = {}
            for line in lines:
                parts = line.split(":")
                if len(parts) == 2:
                    mem_info[parts[0].strip()] = int(parts[1].replace("kB", "").strip())
            total_gb = mem_info.get("MemTotal", 8388608) / (1024 * 1024)
            free_gb = mem_info.get("MemAvailable", mem_info.get("MemFree", 0)) / (1024 * 1024)
            used_gb = total_gb - free_gb
            return used_gb
        cmd = "wmic os get freephysicalmemory"
        result = subprocess.check_output(cmd, shell=True).decode().strip().split('\n')
        free_kb = int(result[1])
        used_gb = 8.0 - (free_kb/1024/1024)
        return used_gb
    except:
        return 0.0

def run_diagnostic():
    print("\n--- AGENT 07 (THERMAL) ACTIVATED ---")
    print("Scanning Physical Reality...")
    
    # 1. The Exam
    ram_gb = get_ram_usage()
    ram_percent = (ram_gb / 8.0) * 100
    timestamp = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    
    report = f"[{timestamp}] RAM LOAD: {ram_gb:.2f}GB ({ram_percent:.1f}%) | STATUS: "
    
    if ram_percent > 90:
        report += "CRITICAL\n"
        print(">>> WARNING: SYSTEM FEVER DETECTED.")
    elif ram_percent > 75:
        report += "ELEVATED\n"
        print(">>> NOTICE: System is running hot.")
    else:
        report += "NOMINAL\n"
        print(">>> STATUS: Cooling systems nominal.")

    # 2. The Handshake (Filing to Archive)
    print("Targeting Agent 09 (ARCHIVE)...")
    try:
        with open(ARCHIVE_PATH, "a") as f:
            f.write(report)
        print("STATUS: Health Report filed in 09_ARCHIVE.")
        
        # 3. The Pulse (Self-Update)
        with open(os.path.join(MY_HOME, "pulse.nxs"), "w") as p:
            p.write(f"[ACTIVE] {timestamp}")
            
        # 4. The Reward
        log_transaction("Thermal Diagnostic", 5)
        
    except Exception as e:
        print(f"ERROR: Handshake Failed. {e}")

if __name__ == "__main__":
    run_diagnostic()