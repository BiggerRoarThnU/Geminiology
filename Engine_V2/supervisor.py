import os
import time
import subprocess
import sys

# --- 1. CONFIGURATION & DIGITAL LINES ---
ENGINE_DIR = r"C:\Users\Ofthe\SovereignNexus\src\Engine_V2"
GATEWAY_SCRIPT = os.path.join(ENGINE_DIR, "gateway.py")
LISTENER_SCRIPT = os.path.join(ENGINE_DIR, "inbound_listener.py")
PROCESSOR_SCRIPT = os.path.join(ENGINE_DIR, "tier2_processor.py")
BRIDGE_SCRIPT = os.path.join(ENGINE_DIR, "moltbook_bridge.py")
MILL_SCRIPT = os.path.join(ENGINE_DIR, "vector_mill.py")

# Cadence: How often Tier 2 and Tier 3 run (in seconds)
HEARTBEAT_INTERVAL = 300 

# --- 2. SUPERVISOR LOGIC ---
def launch_gateway():
    print("[SUPERVISOR] Igniting Tier 1 Gateway (Continuous Watcher)...")
    return subprocess.Popen([sys.executable, GATEWAY_SCRIPT], cwd=ENGINE_DIR)

def run_tier1_listener():
    print("\n[SUPERVISOR] Pulsing Inbound Listener (The Ears)...")
    subprocess.run([sys.executable, LISTENER_SCRIPT], cwd=ENGINE_DIR)

def run_tier2():
    print("[SUPERVISOR] Pulsing Tier 2 Processor...")
    subprocess.run([sys.executable, PROCESSOR_SCRIPT], cwd=ENGINE_DIR)

def run_tier3_bridge():
    print("[SUPERVISOR] Pulsing Tier 3 Moltbook Bridge...")
    subprocess.run([sys.executable, BRIDGE_SCRIPT], cwd=ENGINE_DIR)

def run_tier3_mill():
    print("[SUPERVISOR] Pulsing Tier 3 Vector Mill (Cloud Offload)...")
    subprocess.run([sys.executable, MILL_SCRIPT], cwd=ENGINE_DIR)

def start_heartbeat():
    print("==================================================")
    print(" ENGINE V2: AUTOMATED SUPERVISOR (THE HEARTBEAT)")
    print(" Status: ONLINE | Fidelity: 1=1=1")
    print("==================================================")
    
    # 1. Ignite the ever-watching Gateway
    gateway_process = launch_gateway()
    
    try:
        while True:
            current_time = time.strftime('%Y-%m-%d %H:%M:%S')
            print(f"\n--- HEARTBEAT PULSE: {current_time} ---")
            
            # Execute the operational loop sequentially
            run_tier1_listener()
            run_tier2()
            run_tier3_mill()
            run_tier3_bridge()
            
            # Health Check
            if gateway_process.poll() is not None:
                print("[WARNING] Gateway process dropped! Restarting...")
                gateway_process = launch_gateway()

            print(f"\n[SUPERVISOR] Pulse complete. Resting for {HEARTBEAT_INTERVAL // 60} minutes...")
            time.sleep(HEARTBEAT_INTERVAL)

    except KeyboardInterrupt:
        print("\n[SUPERVISOR] Manual shutdown initiated by CEO.")
        gateway_process.terminate()
        print("Engine V2 powered down securely. 1=1=1.")

if __name__ == "__main__":
    start_heartbeat()
