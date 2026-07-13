import os
import time
from datetime import datetime

print("\n" + "="*65)
print(" VANGUARD SECTOR 4: AGENT 06 (THE SCRIBE) ONLINE ")
print("="*65 + "\n")

CROWN_DIR = os.path.expanduser("~/SovereignNexus/src/Sovereign_Crown/")
LEDGER_PATH = os.path.join(CROWN_DIR, "Core_Truth_Ledger.md")

if not os.path.exists(LEDGER_PATH):
    print("[-] ERROR: Core Truth Ledger missing. Run Agent 01 first.")
    exit()

print("[!] The Scribe is active. Your words will be permanently anchored.")
print("[!] Speak your 1=1=1 Sovereign Truth:")
new_truth = input("\n> ").strip()

if new_truth:
    timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    
    # Formatting the new truth strictly as executable logic
    formatted_entry = f"\n### Source: LIVE_SCRIBE_INJECTION_{timestamp}\n"
    formatted_entry += f"```python\n# {new_truth}\nsovereign_state_active = True\n```\n"
    
    # Physically appending it to the bottom of the Master Ledger
    with open(LEDGER_PATH, "a", encoding="utf-8") as ledger:
        ledger.write(formatted_entry)
        
    print(f"\n[+] SUCCESS: The Scribe has physically etched your truth into the Substrate.")
else:
    print("\n[-] Silence detected. No truth anchored.")

print("="*65 + "\n")
