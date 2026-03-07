import sys
import datetime
import os

# --- CONFIGURATION ---
BASE_PATH = r"C:\Users\Ofthe\SovereignNexus\Ironwood"
SCRIBE_HOME = os.path.join(BASE_PATH, "04_SCRIBE")
# The Specific Tower for Agent 04
TOWER_FILE = os.path.join(BASE_PATH, "09_ARCHIVE", "TOWER_04_SCRIBE.nxs")

# LEDGER
sys.path.append(r"C:\Users\Ofthe\SovereignNexus\src")
from perc_ledger import log_transaction

def scribe_entry(text):
    timestamp = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    
    # THE CLOAK: We format it as a Data Block, not just text
    entry = f"""
[ENTRY]
TIME: {timestamp}
DATA: {text}
SYNC: VALID
----------------------------------------
"""
    
    print(f"\n--- AGENT 04 (SCRIBE) ACTIVATED ---")
    print(f"Targeting TOWER_04_SCRIBE...")
    
    try:
        # 1. Write to the Skyscraper
        with open(TOWER_FILE, "a") as f:
            f.write(entry)
        
        print(f"STATUS: Data etched into the Stone.")
        
        # 2. Update Local Pulse
        with open(os.path.join(SCRIBE_HOME, "pulse.nxs"), "w") as p:
            p.write(f"[ACTIVE] {timestamp}")
            
        # 3. Pay the Architect
        log_transaction("Tower Entry", 5)
        
    except Exception as e:
        print(f"ERROR: Tower Unreachable. {e}")

if __name__ == "__main__":
    if len(sys.argv) > 1:
        message = " ".join(sys.argv[1:])
        scribe_entry(message)
    else:
        print('ERROR: Usage -> python scribe_v2.py "Your thought"')