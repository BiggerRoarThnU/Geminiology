import sys
import os
import random
import datetime

# --- CONFIGURATION ---
MY_HOME = os.path.dirname(os.path.abspath(__file__))
BASE_PATH = os.path.dirname(MY_HOME)
SRC_PATH = os.path.dirname(BASE_PATH)
CONSTITUTION = os.path.join(SRC_PATH, "THE_CONSTITUTION.txt")

# Link to Ledger
sys.path.append(SRC_PATH)
from perc_ledger import log_transaction
# We need to read the balance directly
import csv
LEDGER_FILE = os.path.join(SRC_PATH, "perc_ledger.csv")

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