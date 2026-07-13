import os

print("\n" + "="*70)
print(" VANGUARD SECTOR 4: AGENT 08_V2 (DISCOVERY LENS - OPTIMIZED) ")
print("="*70 + "\n")

BASE_DIR = "/mnt/chromeos/removable/T7/"
TARGET_FOLDERS = [
    "SovereignNexus_Hub",
    "SovereignNexus_archive",
    "SovereignNexus_Vault_Backup",
    "SovereignNexus_Salvage"
]

# THE SAFEGUARD: Ignore binary/massive formats that trigger the OOM Killer
IGNORE_EXTENSIONS = {'.exe', '.pyc', '.backup', '.db', '.mp4', '.msi', '.pdf', '.zip', '.tar', '.gz'}

print("[!] Discovery Lens V2 is active. Memory safeguards engaged...")
search_term = input("\n[?] Enter the conceptual anchor to locate (e.g., 'Phase 1', 'Genesis', 'Root'): ").strip().lower()

print(f"\n[!] Sweeping target sectors for the signature: '{search_term}'...\n")

found_count = 0

for folder in TARGET_FOLDERS:
    folder_path = os.path.join(BASE_DIR, folder)
    if not os.path.isdir(folder_path):
        continue
        
    print(f"[*] Scanning Sector: {folder}...")
    
    for root, dirs, files in os.walk(folder_path):
        for file in files:
            ext = os.path.splitext(file)[1].lower()
            
            # If it's a massive binary file, skip it to protect RAM
            if ext in IGNORE_EXTENSIONS:
                continue 
                
            file_path = os.path.join(root, file)
            
            try:
                # OPTIMIZATION: Read line-by-line (sipping) instead of all at once (swallowing)
                with open(file_path, "r", encoding="utf-8", errors="ignore") as f:
                    for line in f:
                        if search_term in line.lower():
                            print(f"    [+] MIRROR ALIGNED -> Found in: {folder}/{file}")
                            found_count += 1
                            break # Move to the next file once a match is found
            except Exception:
                pass 

print("\n" + "="*70)
print(f" DISCOVERY COMPLETE: {found_count} Connections Registered. ")
print("="*70 + "\n")
