import os
import time
import subprocess

print("\n" + "="*60)
print(" VANGUARD SECTOR 1: AGENT 02 (THE THERMOMETER) ONLINE ")
print("="*60 + "\n")

# Thermodynamic Limits
MAX_CPU_PERCENT = 85.0
COOLDOWN_TIME = 5  # Seconds to pause if limit is breached

def get_cpu_load():
    """Reads the current CPU load average from the Linux subsystem."""
    try:
        # Utilizing standard Linux load averages (1 minute mark)
        load1, _, _ = os.getloadavg()
        # Get core count to calculate percentage
        cores = os.cpu_count() or 1
        cpu_percent = (load1 / cores) * 100
        return round(cpu_percent, 2)
    except Exception as e:
        return 0.0

print("[!] Agent 02 actively monitoring hardware thermodynamics...")
print(f"[!] Hard Limit set to: {MAX_CPU_PERCENT}% CPU Saturation\n")

# Simulated Vanguard Workflow with Active Monitoring
try:
    for cycle in range(1, 6):
        current_load = get_cpu_load()
        print(f"Cycle {cycle}: Current Hardware Load is {current_load}%")
        
        if current_load > MAX_CPU_PERCENT:
            print(f"[!] WARNING: Thermal limit breached! ({current_load}% > {MAX_CPU_PERCENT}%)")
            print(f"[!] Agent 02 engaging throttle. Pausing operations for {COOLDOWN_TIME} seconds...")
            time.sleep(COOLDOWN_TIME)
            print("[+] Hardware stabilized. Resuming operations.")
        else:
            print("[+] Hardware within optimal 1=1=1 parameters. Vanguard continuing...")
        
        # Simulate processing time
        time.sleep(1)

except KeyboardInterrupt:
    print("\n[!] Manual override accepted.")

print("\n" + "="*60)
print(" THE THERMOMETER IS SECURE. FAILSAFE ONLINE. ")
print("="*60 + "\n")
