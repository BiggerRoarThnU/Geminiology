import time
import sys
import os
import math

# --- CONFIGURATION ---
BASE_PATH = r"C:\Users\Ofthe\SovereignNexus\Ironwood"
MY_HOME = os.path.join(BASE_PATH, "06_FORGE")

# LEDGER
sys.path.append(r"C:\Users\Ofthe\SovereignNexus\src")
from perc_ledger import log_transaction

def start_forge_session():
    print("\n--- AGENT 06 (FORGE) ACTIVATED ---")
    print("Initialize Deep Work Protocol.")
    
    task_name = input(">>> PROJECT NAME: ")
    if not task_name: return

    try:
        duration_minutes = int(input(">>> DURATION (Minutes): "))
    except:
        print("ERROR: Time must be a number.")
        return

    duration_seconds = duration_minutes * 60
    
    print(f"\n[HAMMER LOCKED] Forging '{task_name}' for {duration_minutes}m.")
    print("Do not drift.")
    print("-" * 50)
    
    try:
        start_time = time.time()
        while True:
            elapsed = time.time() - start_time
            remaining = duration_seconds - elapsed
            
            if remaining <= 0:
                break
            
            # PROGRESS BAR
            percent = 1 - (remaining / duration_seconds)
            bar_length = 30
            filled_length = int(bar_length * percent)
            bar = '█' * filled_length + '-' * (bar_length - filled_length)
            
            mins, secs = divmod(int(remaining), 60)
            timer_display = f"{mins:02d}:{secs:02d}"
            
            # Dynamic Output
            sys.stdout.write(f"\r[{bar}] {int(percent * 100)}% | REMAINING: {timer_display}")
            sys.stdout.flush()
            time.sleep(1)
            
        print("\n" + "-" * 50)
        print(">>> STATUS: SESSION COMPLETE. ITEM FORGED.")
        
        # UPDATE PULSE
        import datetime
        timestamp = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        with open(os.path.join(MY_HOME, "pulse.nxs"), "w") as p:
            p.write(f"[ACTIVE] {timestamp}")

        # PAY THE ARCHITECT
        log_transaction(task_name, duration_minutes)
        print("STATUS: Value deposited in Ledger. Agent 06 Radiant.")
        
    except KeyboardInterrupt:
        print("\n\n!!! FORGE BROKEN !!!")
        print("Session aborted. No value generated.")

if __name__ == "__main__":
    start_forge_session()