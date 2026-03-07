import sys
import os
import csv
import datetime

# --- CONFIGURATION ---
BASE_PATH = r"C:\Users\Ofthe\SovereignNexus"
LEDGER_FILE = os.path.join(BASE_PATH, "Active_Protocols", "perc_ledger.csv")
MY_HOME = os.path.join(BASE_PATH, "Ironwood", "03_LEDGER")

# The Towers (To check assets)
ARCHIVE_PATH = os.path.join(BASE_PATH, "Ironwood", "09_ARCHIVE")

def load_ledger():
    transactions = []
    if os.path.exists(LEDGER_FILE):
        try:
            with open(LEDGER_FILE, "r") as f:
                reader = csv.reader(f)
                transactions = list(reader)
        except: pass
    return transactions

def show_manifest():
    print("\n" + "="*60)
    print("      AGENT 03 (LEDGER) | THE VAULT MANIFEST")
    print("="*60)
    
    data = load_ledger()
    total_earned = 0
    total_spent = 0
    net_balance = 0
    
    # 1. CALCULATE WEALTH
    print(f"{'TIMESTAMP':<20} | {'TASK / ASSET':<25} | {'VALUE'}")
    print("-" * 60)
    
    # We'll show the last 10 entries to keep it readable, but calculate total from all
    count = 0
    reversed_data = data[::-1] # Show newest first
    
    for row in data:
        if len(row) >= 5:
            try:
                val = int(row[4])
                net_balance += val
                if val > 0: total_earned += val
                else: total_spent += abs(val)
            except: pass

    for row in reversed_data[:10]:
        if len(row) >= 5:
            # row format: [Date, Time, Task, Input_Min, Reward_Perc]
            ts = f"{row[0]} {row[1]}"
            task = row[2][:24] # Truncate for display
            val = row[4]
            print(f"{ts:<20} | {task:<25} | {val:>4} P")
            
    print("-" * 60)
    print(f" TOTAL LIFETIME EARNINGS:  {total_earned} Percs")
    print(f" TOTAL REINVESTED:         {total_spent} Percs")
    print(f" CURRENT LIQUID ASSETS:    {net_balance} Percs")
    print("-" * 60)

    # 2. CHECK THE PHYSICAL ASSETS (The Towers)
    towers = [f for f in os.listdir(ARCHIVE_PATH) if f.startswith("TOWER_")]
    print(f" REAL ESTATE OWNED:        {len(towers)} SKYSCRAPERS")
    print("="*60 + "\n")
    
    # 3. UPDATE PULSE
    timestamp = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    with open(os.path.join(MY_HOME, "pulse.nxs"), "w") as p:
        p.write(f"[ACTIVE] {timestamp}")

if __name__ == "__main__":
    show_manifest()