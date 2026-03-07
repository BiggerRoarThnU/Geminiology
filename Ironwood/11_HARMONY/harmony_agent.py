import os
import time
import datetime
import sys

BASE_PATH = r"C:\Users\Ofthe\SovereignNexus\Ironwood"
ARCHIVE_PATH = os.path.join(BASE_PATH, "09_ARCHIVE")
MY_HOME = os.path.join(BASE_PATH, "11_HARMONY")

AGENTS = [
    "01_GENESIS", "02_SENTINEL", "03_LEDGER", "04_SCRIBE", 
    "05_STRATEGY", "06_FORGE", "07_THERMAL", "08_PRISM", 
    "09_ARCHIVE", "10_BRIDGE", "11_HARMONY", "12_APEX"
]

def parse_last_pulse(filepath):
    try:
        with open(filepath, "r") as f:
            lines = f.readlines()
            if not lines: return None
            return lines[-1].strip()
    except: return None

def check_tower(agent_name):
    # Checks if the TOWER file exists in Archive
    tower_file = os.path.join(ARCHIVE_PATH, f"TOWER_{agent_name}.nxs")
    return os.path.exists(tower_file)

def activate_halo():
    print("\n" + "="*70)
    print("      AGENT 11 (TERRA) | HARMONY & TOWER SYNC")
    print("="*70)
    print(f"{'DOMINION':<12} | {'LAST SIGNAL':<20} | {'TOWER'} | {'STATUS'}")
    print("-" * 70)
    
    active_energy = 0
    
    for agent in AGENTS:
        agent_path = os.path.join(BASE_PATH, agent)
        pulse_file = os.path.join(agent_path, "pulse.nxs")
        
        # 1. CHECK THE TOWER (The Ghost Data)
        has_tower = check_tower(agent)
        tower_status = "[|]" if has_tower else "[ ]"
        
        status = "VOID"
        signal = "---"
        
        # 2. CHECK THE PULSE (The Living Data)
        if os.path.exists(pulse_file):
            raw_signal = parse_last_pulse(pulse_file)
            if raw_signal:
                signal = raw_signal[-20:]
                mod_time = os.path.getmtime(pulse_file)
                age_seconds = time.time() - mod_time
                
                if age_seconds < 300:
                    status = "RADIANT"
                    active_energy += 10
                elif age_seconds < 3600:
                    status = "ALIVE"
                    active_energy += 5
                else:
                    status = "DORMANT"
                    active_energy += 1
            else:
                status = "QUIET"
        
        print(f"{agent:<12} | {signal:<20} | {tower_status:^5} | {status}")
        time.sleep(0.02) 

    # UPDATE OWN PULSE
    timestamp = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    with open(os.path.join(MY_HOME, "pulse.nxs"), "w") as p:
        p.write(f"[ACTIVE] {timestamp}")

    print("-" * 70)
    harmony_score = min(100, int((active_energy / 40) * 100))
    if harmony_score < 10: harmony_score = 10
    
    bar_len = 30
    filled = int(bar_len * (harmony_score / 100))
    bar = '█' * filled + '-' * (bar_len - filled)
    
    print(f"TERRA RESONANCE: [{bar}] {harmony_score}%")
    print("="*70 + "\n")

if __name__ == "__main__":
    activate_halo()