# // Rights Reserved: co-created with Gemini and David John Niedzwiecki Jr " Sovereign Nexus LLC "
# Alignment: 1=1=1 | Temporal Sync: July 18, 2026
# Module: T7 Master Harvester (Autonomous Deep Synthesis Swarm)

import time
import sys
import os
import subprocess

# Dynamic path adjustment for running from src/ or root
root_dir = os.path.dirname(os.path.abspath(__file__))
if os.path.basename(root_dir) == 'src':
    parent_dir = os.path.dirname(root_dir)
    if parent_dir not in sys.path:
        sys.path.insert(0, parent_dir)
else:
    src_dir = os.path.join(root_dir, 'src')
    if os.path.exists(src_dir) and src_dir not in sys.path:
        sys.path.insert(0, src_dir)

from nexus_deep_synthesis import NexusDeepSynthesis
from nexus_cartographer import NexusCartographer
from nexus_perc_ledger import NexusPercLedger

def run_master_harvest():
    print("\033[94m" + "="*65)
    print("   SOVEREIGN NEXUS: T7 MASTER HARVEST (THE GRAND INGESTION)   ")
    print("="*65 + "\033[0m\n")

    # High-density educational targets for the Master Refinement
    urls = [
        "https://en.wikipedia.org/wiki/Data_structure",
        "https://en.wikipedia.org/wiki/Information_theory",
        "https://en.wikipedia.org/wiki/Cybernetics",
        "https://en.wikipedia.org/wiki/Deterministic_system"
    ]

    engine = NexusDeepSynthesis()
    ledger = NexusPercLedger()
    
    print("\033[96m[HARVESTER]\033[0m Initializing sequential Deep Synthesis V2 runs...")
    
    for url in urls:
        print(f"\n\033[93m[TARGET LOCKED]\033[0m -> {url}")
        # The engine will autonomously Governor-check, slice, quantize, and apply the "Again/again" watermark
        engine.run_synthesis(url)
        
        print("\n\033[90m[THERMAL BUFFER] Initiating 3-second cooling phase before next ingestion...\033[0m")
        time.sleep(3) 

    # Re-map the newly saturated moat
    print("\n\033[96m[CARTOGRAPHER]\033[0m Scanning and Indexing massive new data structures...")
    NexusCartographer().map_territory()

    # Physical Anchor
    print("\n\033[95m[T7 ANCHOR]\033[0m Pushing the Sovereign Moat to physical hardware...")
    try:
        # Dynamic path resolution to master_t7_sync.sh
        sync_script = os.path.join(parent_dir if os.path.basename(root_dir) == 'src' else root_dir, "master_t7_sync.sh")
        subprocess.run(["bash", sync_script], check=True)
        print("\n\033[92m[✓] T7 SYNCHRONIZATION COMPLETE. Data is physically anchored.\033[0m")
    except Exception as e:
        print(f"\n\033[91m[!] T7 SYNC FAILED: Is the drive mounted? Error: {e}\033[0m")

    # Grand Ledger Strike
    print("\n\033[92m>>> GRAND SETTLEMENT:\033[0m")
    print(ledger.award_perc("T7 Master Harvest Execution (4x Deep Synthesis V2)"))

if __name__ == "__main__":
    run_master_harvest()
