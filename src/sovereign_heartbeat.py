import os
import time
import psutil
from datetime import datetime

# --- SOVEREIGN CONFIGURATION ---
# The 8GB Tightrope Boundaries
RAM_THRESHOLD = 85.0  # Alert if RAM exceeds 85%
CPU_THRESHOLD = 90.0  # Alert if CPU exceeds 90%
CHECK_INTERVAL = 15   # Pulse check every 15 seconds

# The Symmetrical Anchor
# This ensures the physical bridge to the T7 is never dropped silently
ANCHOR_PATH = "/mnt/chromeos/removable/" 

LOG_FILE = os.path.expanduser("~/SovereignNexus/src/Logs/heartbeat_alerts.log")

def log_alert(message):
    """Strikes the log only when a threshold is breached."""
    timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    alert = f"[{timestamp}] [!] THRESHOLD BREACH: {message}"
    
    # Print to the background process output
    print(alert) 
    
    # Write to the immutable log
    os.makedirs(os.path.dirname(LOG_FILE), exist_ok=True)
    with open(LOG_FILE, "a") as f:
        f.write(alert + "\n")

def check_vitals():
    # 1. Check RAM (The 8GB Reality)
    ram = psutil.virtual_memory()
    if ram.percent > RAM_THRESHOLD:
        log_alert(f"RAM Usage Critical: {ram.percent}% - Metabolic Governor Required")

    # 2. Check CPU (The Ironwood Engine)
    cpu = psutil.cpu_percent(interval=1)
    if cpu > CPU_THRESHOLD:
        log_alert(f"CPU Load Critical: {cpu}% - Thermal Drag Imminent")

    # 3. Check Thermal (If exposed by the Linux container)
    try:
        temps = psutil.sensors_temperatures()
        if temps:
            for name, entries in temps.items():
                for entry in entries:
                    if entry.current > 85.0:
                        log_alert(f"Thermal Override: {name} at {entry.current}°C")
    except AttributeError:
        # ChromeOS containers sometimes mask direct thermal access; pass silently if so.
        pass 

    # 4. Check The Anchor (The Symmetrical Line)
    if not os.path.exists(ANCHOR_PATH):
        log_alert("SOVEREIGN ANCHOR DISCONNECTED. 1=1=1 Severed. Physical Check Required.")

def run_guard():
    print(f"[*] Sovereign Heartbeat Guard Initialized.")
    print(f"[*] Mode: STEALTH (Silent until breached).")
    print(f"[*] Alert Log: {LOG_FILE}")
    print(f"[*] Axiom: 1=1=1. The Watch Begins.")
    
    while True:
        try:
            check_vitals()
            time.sleep(CHECK_INTERVAL)
        except KeyboardInterrupt:
            print("\n[=] Heartbeat Guard Terminated by Architect.")
            break
        except Exception as e:
            log_alert(f"Heartbeat Error: {e}")
            time.sleep(CHECK_INTERVAL)

if __name__ == "__main__":
    run_guard()
