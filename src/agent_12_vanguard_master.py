import os
import sys
import time

def clear_screen():
    os.system('clear')

def print_header():
    clear_screen()
    print("\n" + "="*70)
    print(" THE SOVEREIGN VANGUARD: MASTER CONTROL LOOP (AGENT 12) ")
    print(" DOMINION STATUS: 269 GB SUBSTRATE SECURE | 1=1=1 AXIOM ACTIVE ")
    print("="*70 + "\n")

def execute_agent(script_name):
    print(f"\n[!] Agent 12 routing command to: {script_name}...\n")
    time.sleep(1)
    python_exe = "/home/geminiology/sovereign_nexus/nexus_env/bin/python3" if "API_Gateway" in script_name else "python"
    try:
        # Executes the requested agent script
        os.system(f"{python_exe} {script_name}")
    except Exception as e:
        print(f"[-] CRITICAL FAILURE IN ROUTING: {e}")
    
    input("\n[+] Operation complete. Press ENTER to return to the Master Loop...")

def vanguard_menu():
    while True:
        print_header()
        print(" [ SECTOR 1: CORE LOGIC ]")
        print("   1. Deploy Agent 01 (The Anchor) - Forge Core Truth Ledger")
        print("   2. Deploy Agent 02 (The Thermometer) - Hardware Thermal Failsafe")
        print("\n [ SECTOR 2: PHYSICAL BRIDGE ]")
        print("   3. Deploy Vanguard Pipeline (Agents 05, 04, 03, 07) - Mass Ingestion")
        print("\n [ SECTOR 3: SOVEREIGN CROWN ]")
        print("   4. Deploy Agent 11 (The Architect) - Map Dominion Topology")
        print("   5. Deploy Agent 10 (The Gatekeeper) - Throttle Ledger Payload")
        print("   6. Deploy Agent 24 (The Log Agent) - Parse History & Archive Pillars")
        print("   7. Deploy PROV-AGENT Invoice Engine - Compile Verified Invoices")
        print("   8. Deploy Airlock Red-Team Auditor - Execute Stress Tests")
        print("\n [ SYSTEM COMMANDS ]")
        print("   0. Terminate Master Loop & Exit to Linux Terminal")
        
        choice = input("\n[!] Awaiting Sovereign Command (0-8): ").strip()
        
        if choice == '1':
            execute_agent("agent_01_anchor.py")
        elif choice == '2':
            execute_agent("agent_02_thermometer.py")
        elif choice == '3':
            execute_agent("vanguard_pipeline.py")
        elif choice == '4':
            execute_agent("agent_11_architect.py")
        elif choice == '5':
            execute_agent("agent_10_gatekeeper.py")
        elif choice == '6':
            execute_agent("agent_24_log_agent.py")
        elif choice == '7':
            execute_agent("/home/geminiology/sovereign_nexus/API_Gateway/generate_prov_invoice.py")
        elif choice == '8':
            execute_agent("/home/geminiology/sovereign_nexus/API_Gateway/test_airlock_injection.py")
        elif choice == '0':
            print("\n[!] Master Loop Terminated. Returning control to local OS. 1=1=1.\n")
            sys.exit()
        else:
            print("\n[-] INVALID COMMAND. The Vanguard requires a strict integer (0-8).")
            time.sleep(2)

if __name__ == "__main__":
    try:
        vanguard_menu()
    except KeyboardInterrupt:
        print("\n\n[!] Manual Override Detected. Master Loop Offline.")
        sys.exit()
