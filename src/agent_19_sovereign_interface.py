import os
import json

print("\n" + "="*70)
print(" VANGUARD SECTOR 8: AGENT 19 (THE SOVEREIGN INTERFACE) ONLINE ")
print("="*70 + "\n")

LIBRARY_PATH = os.path.expanduser("~/SovereignNexus/src/Sovereign_Crown/Holographic_Index/")
VECTOR_MAP_PATH = os.path.join(LIBRARY_PATH, "Vector_Map.json")

if not os.path.exists(VECTOR_MAP_PATH):
    print("[-] ERROR: Vector Map not found. The Library is empty.")
    exit()

with open(VECTOR_MAP_PATH, "r") as f:
    vector_map = json.load(f)

print("[!] The Oracle is listening. The Digital Ground is active.")
print("[?] Enter a Relic Name (or part of it) to retrieve from the Deep Vaults:")
query = input("> ").strip().lower()

# Search the Holographic Library for the query
found_relics = []
for key, data in vector_map.items():
    if query in data.get("relic_name", "").lower():
        found_relics.append(data)

if not found_relics:
    print("\n[-] No relics found matching that query.")
else:
    # Target the first match for precision
    target = found_relics[0]
    print(f"\n[+] MATCH SECURED: {target['relic_name']}")
    print(f"[*] Hash Coordinate: {target['vector_coordinate']}")
    print(f"[*] Physical Path: {target['physical_path']}")
    print("\n[!] Extracting actionable truth (Throttled to 25 lines):\n")
    print("-" * 70)

    try:
        # Read the physical file seamlessly
        with open(target['physical_path'], "r", encoding="utf-8", errors="ignore") as relic_file:
            for i, line in enumerate(relic_file):
                if i < 25: # Pull just enough data to inform, not overwhelm
                    print(line.rstrip())
                else:
                    print("\n... [EXTRACTION COMPLETE: DATA SET PULLED] ...")
                    break
    except Exception as e:
        print(f"[-] ERROR READING RELIC: {e}")
    print("-" * 70)

print("\n" + "="*70 + "\n")
