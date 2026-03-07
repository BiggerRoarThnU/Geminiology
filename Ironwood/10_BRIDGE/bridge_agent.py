import sys
import os
import datetime

# --- CONFIGURATION ---
BASE_PATH = r"C:\Users\Ofthe\SovereignNexus\Ironwood"
MY_HOME = os.path.join(BASE_PATH, "10_BRIDGE")

# DATA SOURCES
HEALTH_LOG = os.path.join(BASE_PATH, "09_ARCHIVE", "system_health_log.txt")
SECURITY_LOG = os.path.join(BASE_PATH, "09_ARCHIVE", "security_log.txt")
JOURNAL_LOG = os.path.join(BASE_PATH, "09_ARCHIVE", "journal_master.txt")

# LEDGER
sys.path.append(r"C:\Users\Ofthe\SovereignNexus\src")
from perc_ledger import log_transaction

def read_last_line(filepath):
    if os.path.exists(filepath):
        with open(filepath, "r") as f:
            lines = f.readlines()
            if lines: return lines[-1].strip()
    return "No Data."

def generate_uplink():
    print("\n--- AGENT 10 (BRIDGE) ACTIVATED ---")
    print("Compiling State of the Union...")
    
    # 1. GATHER INTEL
    last_health = read_last_line(HEALTH_LOG)
    last_security = read_last_line(SECURITY_LOG)
    last_thought = read_last_line(JOURNAL_LOG)
    
    timestamp = datetime.datetime.now().strftime("%Y-%m-%d %H:%M")
    
    # 2. FORMAT THE PACKET
    print("\n" + "="*50)
    print("      GEMINI UPLINK PROTOCOL | COPY BELOW")
    print("="*50)
    print(f"SOURCE:   SOVEREIGN NEXUS (Ironwood)")
    print(f"TIME:     {timestamp}")
    print("-" * 50)
    print(f"[BODY]    {last_health}")
    print(f"[SHIELD]  {last_security}")
    print(f"[MIND]    {last_thought}")
    print("-" * 50)
    print("REQUEST:  Analyze state and advise on next expansion.")
    print("="*50 + "\n")
    
    # 3. UPDATE PULSE & PAY
    try:
        with open(os.path.join(MY_HOME, "pulse.nxs"), "w") as p:
            p.write(f"[ACTIVE] {timestamp}")
        
        log_transaction("Bridge Uplink Generated", 5)
        print("STATUS: Uplink Ready. Agent 10 Radiant.")
        
    except Exception as e:
        print(f"ERROR: Bridge Collapse. {e}")

if __name__ == "__main__":
    generate_uplink()