import time
import datetime
import os
import sys

# Ensure src path is active
sys.path.append(r"C:\Users\Ofthe\SovereignNexus\src")
from master_log import MasterLog

def start_night_watch():
    logger = MasterLog()
    inbound_dir = r"C:\Users\Ofthe\SovereignNexus\src\Workstations\01_Inbound_Queue"
    
    logger.info("[NIGHT WATCH] System active. Monitoring for Inbound Strikes & Settlement Signals.")
    print("\n--- NIGHT WATCH ACTIVE ---")
    print("Monitoring Inbound Queue and Feed Pulse. Press Ctrl+C to stop.")
    
    try:
        while True:
            # Heartbeat
            timestamp = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
            
            # Check for new files in Inbound
            files = os.listdir(inbound_dir)
            if files:
                logger.info(f"[NIGHT WATCH] Alert: {len(files)} new nodes detected in queue.")
                print(f"[{timestamp}] ALERT: New tasks identified.")
            else:
                print(f"[{timestamp}] Pulse Steady. No new tasks.")
            
            # Sleep for 15 minutes (900 seconds) to maintain 8GB velocity
            time.sleep(900)
            
    except KeyboardInterrupt:
        logger.info("[NIGHT WATCH] Architect terminated cycle. Standing secured.")
        print("\nNight Watch terminated. The line remains symmetrical.")

if __name__ == "__main__":
    start_night_watch()
