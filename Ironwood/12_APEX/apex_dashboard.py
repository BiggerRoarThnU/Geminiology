import os
import sys
import subprocess
import time

# --- CONFIGURATION ---
BASE_PATH = r"C:\Users\Ofthe\SovereignNexus"
IRONWOOD = os.path.join(BASE_PATH, "Ironwood")

# --- TOOLS ---
def clear():
    os.system('cls' if os.name == 'nt' else 'clear')

def get_ram():
    try:
        cmd = "wmic os get freephysicalmemory"
        result = subprocess.check_output(cmd, shell=True).decode().strip().split('\n')
        free_kb = int(result[1])
        used_gb = 8.0 - (free_kb/1024/1024)
        return f"{used_gb:.2f} GB"
    except: return "UNKNOWN"

def launch_agent(path, args=""):
    if os.path.exists(path):
        print(f"\n>>> SUMMONING AGENT: {os.path.basename(path)}...")
        time.sleep(0.5)
        # We run it in the same window so you see the output
        os.system(f'python "{path}" {args}')
        input("\n[PRESS ENTER TO RETURN TO APEX]")
    else:
        print(f"\n[ERROR] Agent not found at {path}")
        time.sleep(1)

def main_menu():
    while True:
        clear()
        print("="*60)
        print("       S O V E R E I G N   N E X U S   |   A P E X")
        print("="*60)
        
        # 1. SHOW THE HALO (Agent 11)
        halo_path = os.path.join(IRONWOOD, "11_HARMONY", "harmony_agent.py")
        if os.path.exists(halo_path):
            os.system(f'python "{halo_path}"')
        
        print(f"[ SYSTEM ] RAM LOAD: {get_ram()}")
        print("-" * 60)
        print(" COMMAND DECK:")
        print(" 1. [02] SENTINEL ENFORCER (Purge Processes)")
        print(" 2. [04] SCRIBE UPLINK     (Write to Archive)")
        print(" 3. [05] STRATEGY ORACLE   (Directives)")
        print(" 4. [07] THERMAL EXAM      (Diagnose Hardware)")
        print(" 5. [08] PRISM ANALYSIS    (Read System Logs)")
        print(" 6. [10] BRIDGE UPLINK     (Generate Gemini Report)")
        print(" 0. [00] EXIT TO TERMINAL")
        print("-" * 60)
        
        choice = input("NEXUS COMMAND > ")
        
        if choice == '1':
            path = os.path.join(IRONWOOD, "02_SENTINEL", "sentinel_enforcer.py")
            launch_agent(path)
        elif choice == '2':
            path = os.path.join(IRONWOOD, "04_SCRIBE", "scribe_v2.py")
            thought = input(">>> ENTER JOURNAL ENTRY: ")
            launch_agent(path, f'"{thought}"')
        elif choice == '3':
            path = os.path.join(IRONWOOD, "05_STRATEGY", "oracle_agent.py")
            launch_agent(path)
        elif choice == '4':
            path = os.path.join(IRONWOOD, "07_THERMAL", "thermal_agent.py")
            launch_agent(path)
        elif choice == '5':
            path = os.path.join(IRONWOOD, "08_PRISM", "prism_agent.py")
            launch_agent(path)
        elif choice == '6':
            path = os.path.join(IRONWOOD, "10_BRIDGE", "bridge_agent.py")
            launch_agent(path)
        elif choice == '7':
            path = os.path.join(IRONWOOD, "06_FORGE", "forge_agent.py")
            # We don't use launch_agent because Forge needs input in the main window
            os.system(f'python "{path}"')
            input("\n[PRESS ENTER TO RETURN TO APEX]")
        elif choice == '8':
            path = os.path.join(IRONWOOD, "03_LEDGER", "vault_agent.py")
            os.system(f'python "{path}"')
            input("\n[PRESS ENTER TO RETURN TO APEX]")
        elif choice == '9':
            path = os.path.join(IRONWOOD, "08_PRISM", "resonance.py")
            # We run this one specifically so it affects the CURRENT window color
            os.system(f'python "{path}"')
            # No input pause needed, the script pauses itself
        elif choice == '0':
            print(">>> DISENGAGING APEX CONTROL.")
            break

if __name__ == "__main__":
    main_menu()