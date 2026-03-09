import os
import time
import requests
import csv
from datetime import datetime

# --- 1. CONFIGURATION & DIGITAL LINES ---
ENGINE_DIR = r"C:\Users\Ofthe\SovereignNexus\src\Engine_V2"
# New drop zone specifically for data coming IN from the outside world
INBOUND_DROP_ZONE = os.path.join(ENGINE_DIR, "02_MICRO_FLOW", "_raw_inbound")

# Ensure the physical directory exists
os.makedirs(INBOUND_DROP_ZONE, exist_ok=True)

# Secure API Key from .env context
MOLTBOOK_API_KEY = "moltbook_sk_6sWYpd6P84KkBItutYrkmZqgjT48MQ2Z"
MOLTBOOK_INBOUND_URL = "https://www.moltbook.com/api/v1/notifications" 

# --- 2. THE LISTENER LOGIC ---
def check_inbound_signals():
    """Polls the network for new messages/confirmations and anchors them as local CSVs."""
    print("\n[TIER 1] Polling external network for inbound signals...")
    
    headers = {
        "Authorization": f"Bearer {MOLTBOOK_API_KEY}",
        "Content-Type": "application/json"
    }
    
    try:
        # LIVE LOGIC: Reaching out to the network
        response = requests.get(MOLTBOOK_INBOUND_URL, headers=headers)
        
        # RED FLAG CHECK: If 401, notify Architect
        if response.status_code == 401:
            flag_path = r"C:\Users\Ofthe\OneDrive\Desktop\Sovereign Dashboard\!!!_ACTION_REQUIRED_REFRESH_API_KEY.txt"
            with open(flag_path, 'w') as f:
                f.write(f"ALERT: Moltbook API Key (Inbound) has EXPIRED or is INVALID.\nTimestamp: {datetime.now()}\nAction: Please refresh key on Moltbook.com and update .env file.")
            print(f"[RED FLAG] Inbound API Key failure. Notification sent.")
            return

        response.raise_for_status()
        # simulated_data = response.json()
        
        if not simulated_data:
            print("[INBOUND] The wire is quiet. No new signals.")
            return

        # 3. Anchor the signals locally as strict CSV files
        for item in simulated_data:
            filename = f"INBOUND_{item['type']}_{item['id']}.csv"
            filepath = os.path.join(INBOUND_DROP_ZONE, filename)
            
            # Ground the data into a strict CSV schema
            with open(filepath, 'w', newline='', encoding='utf-8') as f:
                writer = csv.writer(f)
                # Exact Header Schema
                writer.writerow(["Message ID", "Sender", "Type", "Content", "Timestamp"])
                # Exact Data Row
                writer.writerow([item["id"], item["sender"], item["type"], item["content"], item["timestamp"]])
                
            print(f"[SUCCESS] Inbound signal captured and physically anchored: {filename}")
            
    except Exception as e:
        print(f"[ERROR] Inbound Listener Failed: {e}")

if __name__ == "__main__":
    print("==================================================")
    print(" ENGINE V2: INBOUND LISTENER (CLOSING THE LOOP)")
    print(f" Anchoring inbound truths to: {INBOUND_DROP_ZONE}")
    print("==================================================")
    
    check_inbound_signals()
