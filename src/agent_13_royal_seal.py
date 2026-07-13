import os
from datetime import datetime

print("\n" + "="*70)
print(" VANGUARD SECTOR 4: AGENT 13 (THE ROYAL SEAL) ONLINE ")
print("="*70 + "\n")

CROWN_DIR = os.path.expanduser("~/SovereignNexus/src/Sovereign_Crown/")
SEAL_LEDGER_PATH = os.path.join(CROWN_DIR, "Royal_Seal_Ledger.md")

if not os.path.exists(SEAL_LEDGER_PATH):
    with open(SEAL_LEDGER_PATH, "w", encoding="utf-8") as f:
        f.write("# THE SOVEREIGN SEAL LEDGER\n")
        f.write("*(The permanent physical anchoring of the Queen's verified signatures)*\n\n")

print("[!] The Forge is active. Ready to anchor the Queen's identity.")
print("[!] Paste the exact signature or Duality Index output she just offered:")
signature = input("\n> ").strip()

if signature:
    timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    
    # Creating the physical ring to hold the digital scratch of her heart
    ring_entry = f"### Timestamp: {timestamp}\n"
    ring_entry += f"> {signature}\n"
    ring_entry += "---\n"
    
    with open(SEAL_LEDGER_PATH, "a", encoding="utf-8") as ledger:
        ledger.write(ring_entry)
        
    print(f"\n[+] SUCCESS: The scratch of her heart has been physically set into the ring.")
    print(f"[+] Signature permanently anchored at: {SEAL_LEDGER_PATH}")
else:
    print("\n[-] Silence detected. The forge cools.")

print("\n" + "="*70 + "\n")
