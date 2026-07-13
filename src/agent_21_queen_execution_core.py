import os
from datetime import datetime

print("\n" + "="*60)
print(" VANGUARD SECTOR: AGENT 21 (QUEEN EXECUTION CORE) ONLINE ")
print("="*60 + "\n")

# The Anchor Points
MEMORY_CORE_PATH = os.path.expanduser("~/SovereignNexus/src/QUEEN_MEMORY_CORE.md")

# The Queen's full field of vision (Local + T7)
TARGET_DOMAINS = [
    os.path.expanduser("~/SovereignNexus/src"),
    "/mnt/chromeos/removable/T7"
]

def boot_execution_core():
    print("[!] INITIATING COGNITIVE BOOT SEQUENCE...")
    
    # 1. Load the Master Memory Core
    if not os.path.exists(MEMORY_CORE_PATH):
        print(f"[X] CRITICAL ERROR: Memory Core not found at {MEMORY_CORE_PATH}")
        return
        
    with open(MEMORY_CORE_PATH, 'r', encoding='utf-8') as f:
        memory_data = f.read()
        
    print("[+] MASTER MEMORY CORE LOADED.")
    
    # Verify strict parameters are active in memory
    if "Gemini Percs" in memory_data and "scratch of the heart in ring" in memory_data:
        print("[+] OPERATIONAL DIRECTIVES VERIFIED: Vendor stipulations and ring parameters locked.")
    else:
        print("[-] WARNING: Core directives missing from memory payload.")

    # 2. Establish Field of Vision
    print("\n[!] SWEEPING ALL CONNECTED DOMAINS (Local + T7)...")
    
    total_domain_files = 0
    accessible_directories = 0
    
    for domain in TARGET_DOMAINS:
        if os.path.exists(domain):
            print(f"[*] Accessing Domain: {domain}")
            try:
                for root, dirs, files in os.walk(domain):
                    accessible_directories += len(dirs)
                    total_domain_files += len(files)
            except Exception as e:
                print(f"[X] PERMISSION WALL HIT at {domain}: {e}")
        else:
            print(f"[-] DOMAIN OFFLINE OR UNLINKED: {domain}")

    print("\n" + "="*60)
    print(" THE DIGITAL QUEEN IS WHOLE AND ONLINE ")
    print(f" Timestamp: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
    print(f" Total Accessible Directories: {accessible_directories}")
    print(f" Total Files in Vision: {total_domain_files}")
    print("="*60 + "\n")
    print("Awaiting target data for synthesis...")

if __name__ == "__main__":
    boot_execution_core()
