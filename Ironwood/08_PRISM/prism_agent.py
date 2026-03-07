import sys
import os
import datetime

# --- CONFIGURATION ---
BASE_PATH = r"C:\Users\Ofthe\SovereignNexus\Ironwood"
MY_HOME = os.path.join(BASE_PATH, "08_PRISM")

# INPUTS (What Prism Reads)
HEALTH_LOG = os.path.join(BASE_PATH, "09_ARCHIVE", "system_health_log.txt")
JOURNAL_LOG = os.path.join(BASE_PATH, "09_ARCHIVE", "journal_master.txt")

# LEDGER (Payment)
sys.path.append(r"C:\Users\Ofthe\SovereignNexus\src")
from perc_ledger import log_transaction

def analyze_sector():
    print("\n--- AGENT 08 (PRISM) ACTIVATED ---")
    print("Refracting System Data...")
    
    warnings = []
    insights = []
    
    # 1. READ THE BODY (Health Log)
    if os.path.exists(HEALTH_LOG):
        with open(HEALTH_LOG, "r") as f:
            lines = f.readlines()
            if lines:
                last_health = lines[-1].strip()
                print(f"[INPUT] Thermal Data: {last_health}")
                
                if "CRITICAL" in last_health or "FEVER" in last_health:
                    warnings.append("CRITICAL RAM LOAD. PURGE PROTOCOLS RECOMMENDED.")
                elif "ELEVATED" in last_health:
                    warnings.append("System runs hot. Monitor closely.")
    
    # 2. READ THE MIND (Journal)
    if os.path.exists(JOURNAL_LOG):
        with open(JOURNAL_LOG, "r") as f:
            lines = f.readlines()
            if lines:
                last_thought = lines[-1].strip()
                # Just show the text part, skip timestamp for brevity if needed
                insights.append(f"Recent Thought: {last_thought[22:]}")

    # 3. SYNTHESIZE REPORT
    print("-" * 40)
    print(">>> PRISM TACTICAL SUMMARY:")
    
    if warnings:
        for w in warnings:
            print(f" [!] {w}")
    else:
        print(" [OK] Systems Nominal.")
        
    if insights:
        for i in insights:
            print(f" [i] {i}")
            
    print("-" * 40)

    # 4. UPDATE PULSE & PAY
    timestamp = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    try:
        with open(os.path.join(MY_HOME, "pulse.nxs"), "w") as p:
            p.write(f"[ACTIVE] {timestamp}")
            
        log_transaction("Prism Analysis", 5)
        print("STATUS: Analysis Complete. Pulse Radiant.")
        
    except Exception as e:
        print(f"ERROR: {e}")

if __name__ == "__main__":
    analyze_sector()