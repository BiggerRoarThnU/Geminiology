import os

print("\n" + "="*70)
print(" VANGUARD SECTOR 5: AGENT 14 (THE RELIC READER) ONLINE ")
print("="*70 + "\n")

BASE_DIR = "/mnt/chromeos/removable/T7/"
MAX_LINES = 50

print("[!] The Relic Reader is active. Ready to extract ancient code safely.")
file_target = input("\n[?] Paste the exact path of the Genesis file to read (e.g., SovereignNexus_archive/knowledge_skyscraper.py): ").strip()

full_path = os.path.join(BASE_DIR, file_target)

if not os.path.exists(full_path):
    print(f"[-] ERROR: Relic not found at {full_path}")
else:
    print(f"\n[!] Breaching the seal on {file_target}...")
    print("[!] Throttling output to the first 50 lines to protect the timeline.\n")
    print("-" * 70)
    try:
        with open(full_path, "r", encoding="utf-8", errors="ignore") as f:
            for i, line in enumerate(f):
                if i >= MAX_LINES:
                    print("\n... [THROTTLE ENGAGED: RELIC DEPTH LIMIT REACHED] ...")
                    break
                print(line.rstrip())
    except Exception as e:
        print(f"[-] CRITICAL FAILURE: {e}")
    print("-" * 70)

print("\n[+] RELIC EXTRACTION COMPLETE.\n")
