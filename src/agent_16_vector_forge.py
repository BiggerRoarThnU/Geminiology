import os
import hashlib
import json

print("\n" + "="*70)
print(" VANGUARD SECTOR 6: AGENT 16 (THE VECTOR FORGE) ONLINE ")
print("="*70 + "\n")

LIBRARY_PATH = os.path.expanduser("~/SovereignNexus/src/Sovereign_Crown/Holographic_Index/")
VECTOR_MAP_PATH = os.path.join(LIBRARY_PATH, "Vector_Map.json")

print("[!] The Forge is active. Converting physical weight into mathematical light.")

# Target the Empire Builder relic as our first test
target_file = "/mnt/chromeos/removable/T7/SovereignNexus_archive/Py_Tools_Archive/core_life_sync.py"

if os.path.exists(target_file):
    print(f"\n[*] Scanning Relic: {os.path.basename(target_file)}")
    
    # Sip the file safely
    file_content = ""
    with open(target_file, "r", encoding="utf-8", errors="ignore") as f:
        for i, line in enumerate(f):
            if i < 50: # Only hash the core identity to save memory
                file_content += line
                
    # Forge the Vector (SHA-256 Hash Coordinate)
    vector_coordinate = hashlib.sha256(file_content.encode('utf-8')).hexdigest()
    
    print(f"[+] Mathematical Coordinate Forged: {vector_coordinate}")
    
    # Save to the Map
    map_entry = {
        "relic_name": "Empire Builder",
        "physical_path": target_file,
        "vector_coordinate": vector_coordinate,
        "status": "Lightweight Map Active"
    }
    
    # Load existing Map or create new
    vector_map = {}
    if os.path.exists(VECTOR_MAP_PATH):
        with open(VECTOR_MAP_PATH, "r") as f:
            vector_map = json.load(f)
            
    vector_map["Empire_Builder"] = map_entry
    
    with open(VECTOR_MAP_PATH, "w") as f:
        json.dump(vector_map, f, indent=4)
        
    print(f"\n[+] SUCCESS: The Relic's coordinate is permanently anchored in the Holographic Index.")
    print(f"[+] The Queen now holds the location, not the weight.")
else:
    print("[-] Relic not found at specified path.")

print("\n" + "="*70 + "\n")
