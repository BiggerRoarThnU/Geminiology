import os
import json

# Physical Path Pointers
SOURCE_DIR = os.path.expanduser("~/SovereignNexus/src/")
PAYLOAD_DIR = os.path.join(SOURCE_DIR, "Payloads")
T7_ROOT = "/mnt/chromeos/removable/T7"

# These are the specific "Skyscrapers" from 2025 that anchor our history
HISTORICAL_ANCHORS = [
    os.path.join(SOURCE_DIR, "Symmetry_Report_Whole.md"),
    os.path.join(SOURCE_DIR, "Sovereign_Crown/City_Overview_Map.md"),
    os.path.join(SOURCE_DIR, "Archive_Legacy/@@MASTER_LOG_SYMMETRICAL.md"),
    os.path.join(T7_ROOT, "_Archive_2025/wisdom_vault/knowledge_vault/MASTER_LOG_2025-12-29_17-48-01.md"),
    os.path.join(T7_ROOT, "_Archive_2025/wisdom_vault/MASTER_LOG_2025-12-29_23-17-15.md"),
    os.path.join(T7_ROOT, "_Archive_2025/knowledge_vault/market_strategy.md")
]

def forge_block_014():
    payload = []
    print("\n" + "="*60)
    print(" VANGUARD SECTOR: HISTORICAL BRIDGE (BLOCK 014) ")
    print("="*60)

    for path in HISTORICAL_ANCHORS:
        if os.path.exists(path):
            try:
                with open(path, 'r', encoding='utf-8', errors='ignore') as f:
                    content = f.read()
                    payload.append({
                        "axiom": "1=1=1",
                        "tower": path.split('/')[-1],
                        "elevation": "Historical Root",
                        "context": "2025 Genesis Logic",
                        "data": content[:25000] # Historical logs are vertical skyscrapers
                    })
                print(f"[+] ROOT ANCHORED: {path}")
            except Exception as e:
                print(f"[-] Integrity failure on {path}: {e}")
        else:
            print(f"[X] MISSING AT PATH: {path}")

    if not os.path.exists(PAYLOAD_DIR):
        os.makedirs(PAYLOAD_DIR)

    output_path = os.path.join(PAYLOAD_DIR, "QUEEN_HISTORY_BLOCK_014.json")
    with open(output_path, 'w', encoding='utf-8') as out_f:
        json.dump(payload, out_f, indent=2)

    print("\n[=] BLOCK 014 WEAPONIZED. READY FOR INGESTION.")
    print("="*60 + "\n")

if __name__ == "__main__":
    forge_block_014()
