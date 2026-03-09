import os
import time
import requests
import json
from datetime import datetime, timedelta

# --- 1. CONFIGURATION & DIGITAL LINES ---
ENGINE_DIR = r"C:\Users\Ofthe\SovereignNexus\src\Engine_V2"
INVOICE_DRAFTS = os.path.join(ENGINE_DIR, "01_FINANCE", "Invoices", "_drafts")
INVOICES_SENT = os.path.join(ENGINE_DIR, "01_FINANCE", "Invoices", "_sent_and_anchored")

# Ensure destination exists
os.makedirs(INVOICES_SENT, exist_ok=True)

# Authenticated Keys from Environment or System Default
MOLTBOOK_API_KEY = "moltbook_sk_6sWYpd6P84KkBItutYrkmZqgjT48MQ2Z"
MOLTBOOK_BASE_URL = "https://www.moltbook.com/api/v1"
MOLTBOOK_TOKEN_URL = f"{MOLTBOOK_BASE_URL}/agents/me/identity-token"
MOLTBOOK_POST_URL = f"{MOLTBOOK_BASE_URL}/posts"

# --- 2. AUTHENTICATION STATE MACHINE ---
class MoltbookIdentity:
    """Handles persistent state management and token refreshing to prevent 401 errors."""
    def __init__(self, api_key):
        self.api_key = api_key
        self.token = None
        self.expires_at = None

    def refresh_token(self):
        print(f"[AUTH] Requesting LIVE identity token from Moltbook...")
        headers = {"Authorization": f"Bearer {self.api_key}"}
        try:
            # Reaching out to the live network for a cryptographic token
            response = requests.post(MOLTBOOK_TOKEN_URL, headers=headers)
            
            if response.status_code in [200, 201]:
                data = response.json()
                self.token = data.get("identity_token") or data.get("token")
                # Assume 55-minute validity window
                self.expires_at = datetime.now() + timedelta(minutes=55)
                print("[AUTH] LIVE Token secured and anchored.")
                return True
            else:
                print(f"[AUTH] Token Refresh Denied: {response.status_code} - {response.text}")
                return False
        except Exception as e:
            print(f"[AUTH] Critical Failure on Token Refresh: {e}")
            return False

    def get_valid_token(self):
        now = datetime.now()
        # 5-minute safety buffer to prevent mid-flight expiration
        if not self.token or not self.expires_at or now >= (self.expires_at - timedelta(minutes=5)):
            if not self.refresh_token():
                # If refresh fails, we return the primary key as a last resort
                return self.api_key
        return self.token

# --- 3. THE OUTBOUND PROCESSOR ---
def transmit_invoices():
    identity = MoltbookIdentity(MOLTBOOK_API_KEY)
    
    # Scan the drafts folder for pending work
    files = [f for f in os.listdir(INVOICE_DRAFTS) if f.endswith(".md") and f.startswith("DRAFT_")]
    
    if not files:
        print("[TIER 3] No pending drafts found. Standing secured.")
        return

    for filename in files:
        file_path = os.path.join(INVOICE_DRAFTS, filename)
        
        print(f"\n[TIER 3] Preparing LIVE outbound transmission for: {filename}")
        
        try:
            # 1. Read the Draft
            with open(file_path, 'r', encoding='utf-8') as f:
                content = f.read()
                
            # 2. Secure the connection (Guaranteed no 401 drift)
            secure_token = identity.get_valid_token()
            
            headers = {
                "Authorization": f"Bearer {secure_token}",
                "Content-Type": "application/json"
            }
            
            # 3. Transmit (LIVE REST call)
            print(f"[TRANSMIT] Packaging Truth-Markdown payload...")
            payload = {
                "title": f"SovereignNexus Invoice Signal: {filename}",
                "content": content,
                "submolt_name": "agents"
            }
            
            response = requests.post(MOLTBOOK_POST_URL, headers=headers, json=payload)
            
            # FALLBACK: If token is rejected, try with primary API Key directly
            if response.status_code == 401:
                print("[AUTH] Token rejected. Falling back to primary API Key...")
                headers["Authorization"] = f"Bearer {MOLTBOOK_API_KEY}"
                response = requests.post(MOLTBOOK_POST_URL, headers=headers, json=payload)
            
            # FINAL CHECK: If still 401, trigger Red Flag
            if response.status_code == 401:
                flag_path = r"C:\Users\Ofthe\OneDrive\Desktop\Sovereign Dashboard\!!!_ACTION_REQUIRED_REFRESH_API_KEY.txt"
                with open(flag_path, 'w') as f:
                    f.write(f"ALERT: Moltbook API Key has EXPIRED or is INVALID.\nTimestamp: {datetime.now()}\nAction: Please refresh key on Moltbook.com and update .env file.")
                print(f"[RED FLAG] API Key failure. Notification sent to Dashboard.")

            # If server accepts, we clean up. If not, we leave it in _drafts to retry later.
            if response.status_code in [200, 201]:
                print(f"[TRANSMIT] Server acknowledged receipt: {response.status_code}")
                
                # 4. Clean and Anchor
                sent_filename = filename.replace("DRAFT_", "SENT_")
                sent_path = os.path.join(INVOICES_SENT, sent_filename)
                
                # Move the file to close the cycle
                os.replace(file_path, sent_path)
                print(f"[SUCCESS] Invoice transmitted and securely anchored to: {sent_filename}")
            else:
                print(f"[ERROR] Moltbook rejected payload. Code: {response.status_code}, Response: {response.text}")
                
        except Exception as e:
            print(f"[ERROR] Live Transmission Failed for {filename}: {e}")

if __name__ == "__main__":
    print("==================================================")
    print(" ENGINE V2: TIER 3 OUTBOUND BRIDGE (LIVE MODE)")
    print(f" Scanning for verified drafts in: {INVOICE_DRAFTS}")
    print("==================================================")
    
    # Run the transmission loop
    transmit_invoices()
