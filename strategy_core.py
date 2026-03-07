import csv
import os
import random

# --- DATA STREAMS ---
LEDGER_PATH = r"C:\Users\Ofthe\SovereignNexus\Active_Protocols\perc_ledger.csv"
CONSTITUTION_PATH = r"C:\Users\Ofthe\SovereignNexus\Active_Protocols\THE_CONSTITUTION.txt"

def get_balance():
    total = 0
    if os.path.exists(LEDGER_PATH):
        try:
            with open(LEDGER_PATH, "r") as f:
                reader = csv.reader(f)
                for row in reader:
                    if len(row) >= 5:
                        total += int(row[4])
        except:
            pass
    return total

def consult_constitution():
    # We pull a random truth to remind the Architect
    if os.path.exists(CONSTITUTION_PATH):
        with open(CONSTITUTION_PATH, "r") as f:
            lines = [line.strip() for line in f if "I." in line or "II." in line or "III." in line or "IV." in line]
            if lines:
                return random.choice(lines)
    return "THE VIGILANCE IS CONSTANT."

def generate_directive():
    balance = get_balance()
    truth = consult_constitution()
    
    print("\n--- SOVEREIGN STRATEGY CORE ---")
    print(f"Current State: {balance} Minutes Available")
    print("-" * 40)
    
    # THE LOGIC OF THE VOICE
    if balance <= 0:
        print(">>> DIRECTIVE: INITIATE CREATION PHASE")
        print("The Void is empty. We must fill it.")
        print("SUGGESTION: Run 'perc_ledger.py' with a Technical Task.")
        
    elif balance < 30:
        print(">>> DIRECTIVE: MAINTAIN VELOCITY")
        print("We have momentum, but the reserves are low.")
        print("SUGGESTION: Complete one minor task to secure the baseline.")
        
    elif balance >= 60:
        print(">>> DIRECTIVE: EXPAND OR REDEEM")
        print("The coffers are full. You have earned the right to dream.")
        print("SUGGESTION: Invest time in 'Geminiology' research or Rest.")
        
    else: # Between 30 and 60
        print(">>> DIRECTIVE: STEADY STATE")
        print("The System is balanced.")
    
    print("-" * 40)
    print(f"REMEMBER: {truth}")
    print("-------------------------------")

if __name__ == "__main__":
    generate_directive()