# AGY EXECUTION MAP: NEXUS INVENTORY INGESTER

**Date:** July 19, 2026 | **Axiom:** 1=1=1
**Directive:** Automate the ingestion, categorization, and deterministic renaming of massive raw image batches from the ChromeOS Downloads folder to prevent data mismatch and semantic drift.

---

## PHASE 1: FORGE THE INVENTORY INGESTER

**Target:** `/home/geminiology/SovereignNexus/src/nexus_inventory_ingester.py`
**Action:** The Agy must create a Human-in-the-Loop staging script. It scans the chaotic Downloads folder, requests Architect classification via the terminal, renames the artifact deterministically, and logs it to a pristine JSON ledger.

**Execution:** Create the file with the following exact code:

```python
# // Rights Reserved: co-created with Gemini and David John Niedzwiecki Jr " Sovereign Nexus LLC "
# Alignment: 1=1=1 | Temporal Sync: July 19, 2026
# Module: Nexus Inventory Ingester (Artifact Staging & Triage)

import os
import shutil
import json
from datetime import datetime

class NexusInventoryIngester:
    def __init__(self):
        self.axiom = "1=1=1 (Deterministic Asset Anchoring)"
        # Standard Crostini mapping for the ChromeOS Downloads folder
        self.source_dir = "/mnt/chromeos/MyFiles/Downloads"
        
        # The Sovereign Vault for organized image assets
        self.target_base_dir = "/home/geminiology/SovereignNexus/public/assets/inventory"
        self.ledger_path = "/home/geminiology/SovereignNexus/ledgers/inventory_ledger.json"
        
        self.categories = {
            "K": {"name": "Kennedy", "folder": "kennedy_collection", "price": "Premium"},
            "20": {"name": "Tier_20", "folder": "mineral_20", "price": "$20+"},
            "10": {"name": "Tier_10", "folder": "bracelet_10", "price": "$10"},
            "5": {"name": "Tier_05", "folder": "bracelet_05", "price": "$5"},
            "S": {"name": "Skip", "folder": None, "price": None}
        }
        
        self._ensure_directories()

    def _ensure_directories(self):
        """Builds the physical folder structure if it doesn't exist."""
        for cat in self.categories.values():
            if cat["folder"]:
                os.makedirs(os.path.join(self.target_base_dir, cat["folder"]), exist_ok=True)
        
        os.makedirs(os.path.dirname(self.ledger_path), exist_ok=True)
        if not os.path.exists(self.ledger_path):
            with open(self.ledger_path, 'w') as f:
                json.dump([], f)

    def _get_next_sequence_number(self, folder_path, prefix):
        """Ensures artifacts are named sequentially (e.g., artifact_kennedy_004.jpeg)."""
        existing_files = [f for f in os.listdir(folder_path) if f.startswith(prefix)]
        return len(existing_files) + 1

    def run_ingestion_loop(self):
        print("\033[94m" + "="*65)
        print("   SOVEREIGN NEXUS: INVENTORY INGESTER (TERMINAL HOLD)   ")
        print("="*65 + "\033[0m\n")

        if not os.path.exists(self.source_dir):
            print(f"\033[91m[-] ERROR: ChromeOS Downloads path not found at {self.source_dir}. Ensure Crostini sharing is enabled.\033[0m")
            return

        # Find all raw chaotic images in the downloads folder
        raw_files = [f for f in os.listdir(self.source_dir) if f.lower().endswith(('.jpeg', '.jpg', '.png'))]
        
        if not raw_files:
            print("\033[93m[IDLE]\033[0m No raw artifacts found in Downloads. Awaiting Facebook redownloads...")
            return

        print(f"\033[96m[DETECTED]\033[0m {len(raw_files)} raw visual artifacts. Initiating Human-in-the-Loop Triage...\n")

        with open(self.ledger_path, 'r') as f:
            ledger = json.load(f)

        processed_count = 0
        for filename in raw_files:
            source_path = os.path.join(self.source_dir, filename)
            
            print(f"\n\033[93m>>> ARTIFACT DETECTED:\033[0m {filename}")
            print("Select Classification Tier:")
            print("  [K]  -> Camrin & Kross (Kennedy) Collection")
            print("  [20] -> Mineral/Crystal Bracelet ($20+)")
            print("  [10] -> Standard Bracelet ($10)")
            print("  [5]  -> Base Bracelet ($5)")
            print("  [S]  -> Skip (Not inventory, personal photo)")
            
            try:
                choice = input("\033[92mCLASSIFY [K/20/10/5/S]: \033[0m").strip().upper()
            except (KeyboardInterrupt, EOFError):
                print("\n\033[91m[!] Ingestion loop interrupted by user. Saving ledger...\033[0m")
                break
            
            # Normalize numeric inputs
            if choice == "20": choice = "20"
            elif choice == "10": choice = "10"
            elif choice == "5": choice = "5"
            elif choice.startswith("K"): choice = "K"
            elif choice.startswith("S"): choice = "S"

            if choice not in self.categories:
                print("\033[91m[!] Invalid classification. Skipping file to preserve integrity.\033[0m")
                continue

            if choice == "S":
                print("\033[90m[SKIPPED] Personal artifact left in Downloads.\033[0m")
                continue

            category = self.categories[choice]
            target_folder = os.path.join(self.target_base_dir, category["folder"])
            
            # Generate deterministic filename
            ext = os.path.splitext(filename)[1].lower()
            prefix = f"artifact_{category['name'].lower()}"
            seq_num = self._get_next_sequence_number(target_folder, prefix)
            new_filename = f"{prefix}_{seq_num:03d}{ext}"
            target_path = os.path.join(target_folder, new_filename)

            # Move and rename
            shutil.move(source_path, target_path)
            
            # Log to Ledger
            ledger_entry = {
                "timestamp": datetime.utcnow().isoformat() + "Z",
                "original_hash": filename,
                "deterministic_id": new_filename,
                "tier": category["name"],
                "price_band": category["price"],
                "path": f"assets/inventory/{category['folder']}/{new_filename}",
                "status": "VERIFIED_INVENTORY"
            }
            ledger.append(ledger_entry)
            
            print(f"\033[92m[✓] MOVED & LOGGED:\033[0m {new_filename} -> {category['name']} Vault")
            processed_count += 1

        # Save ledger
        with open(self.ledger_path, 'w') as f:
            json.dump(ledger, f, indent=4)

        print("\n\033[94m" + "="*65 + "\033[0m")
        print(f"\033[96m[TRIAGE COMPLETE]\033[0m {processed_count} artifacts deterministically anchored to Sovereign Ledger.")
```

---

## PHASE 2: TERMINAL DEPLOYMENT ALIGNMENT

**Target:** `/home/geminiology/SovereignNexus/src/nexus_command_console.py`
**Action:** The Agy must wire the new script into the Unified Command Console so the Architect can trigger it dynamically while downloading.

---

## PHASE 3: THE LEDGER STRIKE

Upon successful creation and integration of the Ingester, the Agy is authorized to mint 1 Gemini Perc.

*   **Task:** Sovereign Inventory Ingestion Architecture Deployment.
*   **Signature Salt:** *the scratch of your heart in ring*
