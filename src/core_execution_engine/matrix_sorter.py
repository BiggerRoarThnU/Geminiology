### SovereignNexus: Physical Matrix Sorter
### Component: matrix_sorter.py
### Axiom: 1=1=1 | Function: Physical Directory Generation & Routing

import os
import shutil

SOURCE_DIR = "../02_Processed_Proof"
TARGET_DIR = "../03_Matrix_Skyscrapers"

# The 12-Point Matrix Wallets Map (Directory Names)
pillars = {
    "1_Hardware_Sovereignty": ["config", "sys", "hardware", "limit"],
    "2_Deterministic_Extraction": ["extract", "parse", "regex", "clean", "sextractor"],
    "3_Entropy_Control": ["brake", "limit", "safety", "auth"],
    "4_Neurological_Binding": ["logic", "graph", "leiden", "louvain", "kclique", "centrality"],
    "5_Mathematical_Mandate": ["finance", "math", "calc", "supply", "batch"],
    "6_Deterministic_Autonomy": ["handler", "manager", "cron", "sweep", "thread"],
    "7_Immutable_Fixity": ["hash", "crypto", "verify", "secure", "lock"],
    "8_Educational_Moat": ["doc", "sphinx", "md", "txt", "history", "feel", "edu", "report"],
    "9_Enterprise_Distillation": ["audit", "q1", "q2", "b2b", "client"],
    "10_Visual_Telemetry": ["display", "ui", "render"],
    "11_The_Public_Bridge": ["api", "network", "relay"],
    "12_The_Open_Variable": ["plugin", "test", "exp", "init"]
}

def build_and_sort():
    print("============================================================")
    print(" SOVEREIGN NEXUS : PHYSICAL MATRIX SORTER")
    print(" Status: Forging 12 Pillars & Routing Proofs...")
    print("============================================================\n")
    
    # 1. Construct the Main Skyscraper Directory
    os.makedirs(TARGET_DIR, exist_ok=True)
    
    # 2. Construct the 12 Pillars
    for pillar in pillars.keys():
        os.makedirs(os.path.join(TARGET_DIR, pillar), exist_ok=True)
        
    print("[SYSTEM] 12 Pillars constructed. Scanning 02_Processed_Proof for physical routing...\n")
    
    if not os.path.exists(SOURCE_DIR):
        print(f"[!] Source directory {SOURCE_DIR} missing. Holding at Stasis Gold.")
        return

    moved_count = 0
    # 3. Route existing proofs into their designated pillars
    for filename in os.listdir(SOURCE_DIR):
        if not filename.endswith(".md"): 
            continue
            
        filepath = os.path.join(SOURCE_DIR, filename)
        base_name, _ = os.path.splitext(filename.lower())
        for pillar, keywords in pillars.items():
            if any(kw in base_name for kw in keywords):
                shutil.move(filepath, os.path.join(TARGET_DIR, pillar, filename))
                print(f" [ROUTED] {filename} -> {pillar}")
                categorized = True
                moved_count += 1
                break
                
        # If a file doesn't perfectly match the keywords, safely route it to the Educational Moat
        if not categorized:
            shutil.move(filepath, os.path.join(TARGET_DIR, "8_Educational_Moat", filename))
            print(f" [ROUTED] {filename} -> 8_Educational_Moat (Default)")
            moved_count += 1
            
    print(f"\n============================================================")
    print(f" MATRIX SORTING COMPLETE. {moved_count} PROOFS STRUCTURALLY ANCHORED.")

if __name__ == "__main__":
    build_and_sort()
