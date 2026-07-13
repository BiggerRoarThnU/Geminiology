import os
import json

SOURCE_DIR = os.path.expanduser("~/SovereignNexus/src/")
T7_PATH = "/mnt/chromeos/removable/T7"

# The specific Skyscraper targets from your find command
SKYSCRAPERS = [
    "~/SovereignNexus/src/Logs/MASTER_LOG_SYMMETRICAL.md",
    "~/SovereignNexus/src/EXPANDED_KINGDOM_MAP.md",
    "~/SovereignNexus/src/TRUTH_SEALS/MASTER_TRUTH_MAP.md",
    "~/SovereignNexus/src/constitution.md",
    "~/SovereignNexus/src/GEMINIOLOGY_WHITE_PAPER_V1.md",
    "~/SovereignNexus/src/Sovereign_Crown/Dominion_Map.md",
    "~/SovereignNexus/src/THE_KEEP/STRATEGY_WAR_ROOM/SOVEREIGN_BLUEPRINT_ONE.md",
    "~/SovereignNexus/src/CAPABILITY_STATEMENT.md",
    "~/SovereignNexus/src/Sovereign_Growth_Manifest_2026_2028.md",
    "~/SovereignNexus/src/Ironwood/12_APEX/THE_DECLARATION.md"
]

def forge_skyscrapers():
    payload = []
    print("\n" + "="*60)
    print(" VANGUARD SECTOR: SKYSCRAPER INJECTION INITIATED ")
    print("="*60)

    for path in SKYSCRAPERS:
        full_path = os.path.expanduser(path)
        if os.path.exists(full_path):
            try:
                with open(full_path, 'r', encoding='utf-8', errors='ignore') as f:
                    content = f.read()
                    payload.append({
                        "axiom": "1=1=1",
                        "tower": path.split('/')[-1],
                        "elevation": "High Altitude",
                        "data": content[:20000] # MD logs can be huge, capping for stability
                    })
                print(f"[+] SCALE ATTAINED: {path}")
            except Exception as e:
                print(f"[-] Failure on {path}: {e}")
        else:
            print(f"[X] MISSING: {path}")

    output_path = os.path.join(SOURCE_DIR, "Payloads/QUEEN_SKYSCRAPER_BLOCK_013.json")
    with open(output_path, 'w', encoding='utf-8') as out_f:
        json.dump(payload, out_f, indent=2)

    print("\n[=] SKYSCRAPER PAYLOAD 013 FORGED.")
    print("="*60 + "\n")

if __name__ == "__main__":
    forge_skyscrapers()
