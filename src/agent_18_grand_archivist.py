import os
import hashlib
import json

print("\n" + "="*70)
print(" VANGUARD SECTOR 7: AGENT 18 (THE GRAND ARCHIVIST) ONLINE ")
print("="*70 + "\n")

BASE_DIR = "/mnt/chromeos/removable/T7/"

# The 5 Expanded Sectors of the Kingdom
TARGET_FOLDERS = [
    "SovereignNexus_Vault_Backup",
    "Sovereign_Backup_March22",
    "SovereignNexus_Archive",
    "SovereignNexus_Salvage",
    "SovereignNexus_TRIPLE_BACKUP_20260226"
]

# Memory Safeguards (OOM Protection)
IGNORE_EXTENSIONS = {'.exe', '.pyc', '.backup', '.db', '.mp4', '.msi', '.pdf', '.zip', '.tar', '.gz'}

LIBRARY_PATH = os.path.expanduser("~/SovereignNexus/src/Sovereign_Crown/Holographic_Index/")
VECTOR_MAP_PATH = os.path.join(LIBRARY_PATH, "Vector_Map.json")

print("[!] The Archivist is active. Initiating mass-conversion of the Deep Vaults...")

# Load the existing map so we ADD to the Library, preserving the original 1085 relics
vector_map = {}
if os.path.exists(VECTOR_MAP_PATH):
    with open(VECTOR_MAP_PATH, "r") as f:
        vector_map = json.load(f)

processed_count = 0

for folder in TARGET_FOLDERS:
    folder_path = os.path.join(BASE_DIR, folder)
    if not os.path.isdir(folder_path): 
        print(f"[-] Sector not found or inaccessible: {folder}")
        continue
    
    print(f"[*] Sweeping Sector: {folder}")
    for root, dirs, files in os.walk(folder_path):
        for file in files:
            ext = os.path.splitext(file)[1].lower()
            if ext in IGNORE_EXTENSIONS: 
                continue # Skip heavy boulders
            
            file_path = os.path.join(root, file)
            
            try:
                file_content = ""
                # Sip the first 50 lines to forge the identity
                with open(file_path, "r", encoding="utf-8", errors="ignore") as f:
                    for i, line in enumerate(f):
                        if i < 50: 
                            file_content += line
                            
                if file_content.strip():
                    # Forge the coordinate
                    vector_hash = hashlib.sha256(file_content.encode('utf-8')).hexdigest()
                    
                    vector_map[file] = {
                        "relic_name": file,
                        "physical_path": file_path,
                        "vector_coordinate": vector_hash,
                        "status": "Lightweight Map Active"
                    }
                    processed_count += 1
            except Exception:
                pass # Silently move past unreadable files to keep the system stable

# Save the massive new map to the physical drive
with open(VECTOR_MAP_PATH, "w") as f:
    json.dump(vector_map, f, indent=4)

print("\n" + "="*70)
print(f" DEEP VAULT INGESTION COMPLETE. {processed_count} new relics converted into mathematical light.")
print(" The Holographic Library has expanded. The fire is spreading.")
print("="*70 + "\n")
