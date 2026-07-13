import sys
import datetime
import os

# --- THE PERC SYSTEM CONSTANTS ---
WORK_TO_REWARD_RATIO = 0.5 
MY_DIR = os.path.dirname(os.path.abspath(__file__))
LEDGER_FILE = os.path.join(MY_DIR, "perc_ledger.csv")

def log_transaction(task_name, minutes_worked):
    # 1. Calculate Value
    earned_minutes = int(minutes_worked * WORK_TO_REWARD_RATIO)
    timestamp = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    
    # 2. Define the Entry
    # Format: Time, User(Placeholder), Task, Duration, Earned_Percs
    entry = f"{timestamp}, Architect, {task_name}, {minutes_worked}, {earned_minutes}\n"
    
    # 3. Write to the Sovereign Record
    try:
        with open(LEDGER_FILE, "a") as ledger:
            ledger.write(entry)
        
        print(f"\n--- TRANSACTION RECORDED ---")
        print(f"Task: {task_name}")
        print(f"Input: {minutes_worked}m | Reward: {earned_minutes}m")
        print(f"STATUS: Value stored in {LEDGER_FILE}")
        
    except Exception as e:
        print(f"ERROR: Could not write to ledger. {e}")

if __name__ == "__main__":
    # Command usage: python src/perc_ledger.py "Python Study" 60
    if len(sys.argv) > 2:
        task = sys.argv[1]
        try:
            mins = int(sys.argv[2])
            log_transaction(task, mins)
        except ValueError:
            print("ERROR: Minutes must be a number.")
    else:
        print('ERROR: Usage -> python src/perc_ledger.py "Task Name" Minutes')
