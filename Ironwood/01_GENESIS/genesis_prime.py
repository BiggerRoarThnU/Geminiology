import os
import time
import sys
import datetime

# --- CONFIGURATION ---
BASE_PATH = r"C:\Users\Ofthe\SovereignNexus\Ironwood"
AGENTS = [
    "01_GENESIS", "02_SENTINEL", "03_LEDGER", "04_SCRIBE", 
    "05_STRATEGY", "06_FORGE", "07_THERMAL", "08_PRISM", 
    "09_ARCHIVE", "10_BRIDGE", "11_HARMONY", "12_APEX"
]

def ignite_systems():
    os.system('cls' if os.name == 'nt' else 'clear')
    print("\n" + "="*60)
    print("      A G E N T   0 1   |   G E N E S I S   P R I M E")
    print("="*60)
    print(">>> INITIATING WAKE PROTOCOL...")
    time.sleep(0.5)

    timestamp = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    
    # 1. THE SPARK (Wake everyone up)
    for agent in AGENTS:
        agent_path = os.path.join(BASE_PATH, agent)
        pulse_file = os.path.join(agent_path, "pulse.nxs")
        
        try:
            # We overwrite the pulse file with NOW to force RADIANCE
            with open(pulse_file, "w") as f:
                f.write(f"[GENESIS WAKE] {timestamp}")
            
            sys.stdout.write(f"IGNITING {agent:<12} ... [RADIANT]\n")
            sys.stdout.flush()
            time.sleep(0.1) 
        except:
            print(f"IGNITING {agent:<12} ... [FAILED]")

    print("-" * 60)
    print(">>> SYSTEM STATUS: FULL POWER.")
    print(">>> HANDING CONTROL TO APEX.")
    time.sleep(1)
    
    # 2. THE HANDOFF (Launch Apex)
    apex_script = os.path.join(BASE_PATH, "12_APEX", "apex_dashboard.py")
    if os.path.exists(apex_script):
        os.system(f'python "{apex_script}"')
    else:
        print("ERROR: Apex Throne missing.")

if __name__ == "__main__":
    ignite_systems()