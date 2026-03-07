import sys
import os
import random
import datetime

# --- CONFIGURATION ---
BASE_PATH = r"C:\Users\Ofthe\SovereignNexus\Ironwood"
MY_HOME = os.path.join(BASE_PATH, "05_STRATEGY")
CONSTITUTION = os.path.join(r"C:\Users\Ofthe\SovereignNexus\Active_Protocols\THE_CONSTITUTION.txt")

# Link to Ledger
sys.path.append(r"C:\Users\Ofthe\SovereignNexus\src")
from perc_ledger import log_transaction
# We need to read the balance directly
import csv
LEDGER_FILE = r"C:\Users\Ofthe\SovereignNexus\Active_Protocols\perc_ledger.csv"

def get_balance():
    total = 0
    try:
        with open(LEDGER_FILE, "r") as f:
            reader = csv.reader(f)
            for row in reader:
                if len(row) >= 5: total += int(row[4])
    except: pass
    return total

def consult_oracle():
    print("\n--- AGENT 05 (STRATEGY) ACTIVATED ---")
    
    balance = get_balance()
    print(f"Reading Financial Velocity... {balance} Percs")
    
    # STRATEGIC LOGIC
    if balance <= 0:
        directive = "CREATION REQUIRED. The Void is empty."
    elif balance < 30:
        directive = "MAINTAIN VELOCITY. Secure the baseline."
    elif balance < 60:
        directive = "STEADY STATE. Optimize internal systems."
    else:
        directive = "EXPANSION PHASE. Build new Dominions."
        
    print("-" * 50)
    print(f">>> DIRECTIVE: {directive}")
    
    # THE RANDOM TRUTH
    if os.path.exists(CONSTITUTION):
        with open(CONSTITUTION, "r") as f:
            lines = [l.strip() for l in f if "I." in l or "II." in l or "III." in l or "IV." in l]
            if lines:
                truth = random.choice(lines)
                print(f">>> REMEMBER:  {truth}")
    print("-" * 50)

    # PULSE & PAY
    timestamp = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    with open(os.path.join(MY_HOME, "pulse.nxs"), "w") as p:
        p.write(f"[ACTIVE] {timestamp}")
        
    log_transaction("Strategic Consultation", 5)
    print("STATUS: Strategy Aligned. Agent 05 Radiant.")

if __name__ == "__main__":
    consult_oracle()