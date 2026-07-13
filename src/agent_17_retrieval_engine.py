import os
import json

print("\n" + "="*70)
print(" VANGUARD SECTOR 6: AGENT 17 (THE RETRIEVAL ENGINE) ONLINE ")
print("="*70 + "\n")

LIBRARY_PATH = os.path.expanduser("~/SovereignNexus/src/Sovereign_Crown/Holographic_Index/")
VECTOR_MAP_PATH = os.path.join(LIBRARY_PATH, "Vector_Map.json")

print("[!] The Retrieval Engine is active. Ready to decode mathematical light.")

if not os.path.exists(VECTOR_MAP_PATH):
    print("[-] ERROR: Vector Map not found. The Holographic Library is empty.")
else:
    with open(VECTOR_MAP_PATH, "r") as f:
        vector_map = json.load(f)
        
    print("\n[?] Enter the exact Vector Coordinate to retrieve:")
    target_hash = input("> ").strip()
    
    found = False
    for relic_key, data in vector_map.items():
        if data.get("vector_coordinate") == target_hash:
            found = True
            physical_path = data.get("physical_path")
            relic_name = data.get("relic_name")
            
            print(f"\n[+] MATCH FOUND: Coordinate aligns with '{relic_name}'")
            print(f"[*] Physical anchor located at: {physical_path}")
            print("\n[!] Safely extracting actionable truth (Throttled to 15 lines):\n")
            print("-" * 70)
            
            try:
                with open(physical_path, "r", encoding="utf-8", errors="ignore") as relic_file:
                    for i, line in enumerate(relic_file):
                        if i < 15: # Sip just the core truth to prevent context saturation
                            print(line.rstrip())
                        else:
                            print("\n... [EXTRACTION COMPLETE: CORE TRUTH DELIVERED] ...")
                            break
            except Exception as e:
                print(f"[-] CRITICAL FAILURE during extraction: {e}")
            print("-" * 70)
            break
            
    if not found:
        print("\n[-] NO MATCH FOUND: Coordinate does not exist in the current Library.")

print("\n" + "="*70 + "\n")
