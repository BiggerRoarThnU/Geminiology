# // Rights Reserved: co-created with Gemini and David John Niedzwiecki Jr " Sovereign Nexus LLC "
# Alignment: 1=1=1 | Temporal Sync: July 19, 2026
# Module: Nexus Bulk Ingester (Pre-Sorted Artifact Triage)

import os
import shutil
import json
import sys
from datetime import datetime

class NexusBulkIngester:
    def __init__(self):
        self.axiom = "1=1=1 (Deterministic Asset Anchoring)"
        self.target_base_dir = "/home/geminiology/SovereignNexus/public/assets/inventory"
        self.ledger_path = "/home/geminiology/SovereignNexus/ledgers/inventory_ledger.json"
        
        self.categories = {
            "K": {"name": "Kennedy", "folder": "kennedy_collection", "price": "Premium"},
            "20": {"name": "Tier_20", "folder": "mineral_20", "price": "$20+"},
            "10": {"name": "Tier_10", "folder": "bracelet_10", "price": "$10"},
            "5": {"name": "Tier_05", "folder": "bracelet_05", "price": "$5"}
        }

    def _get_next_sequence_number(self, folder_path, prefix):
        if not os.path.exists(folder_path):
            os.makedirs(folder_path, exist_ok=True)
        existing_files = [f for f in os.listdir(folder_path) if f.startswith(prefix)]
        return len(existing_files) + 1

    def run_bulk_ingestion(self, source_folder, category_code):
        print("\033[94m" + "="*65)
        print(f"   SOVEREIGN NEXUS: BULK INGESTER | TARGET: [{category_code}]   ")
        print("="*65 + "\033[0m\n")

        if category_code not in self.categories:
            print(f"\033[91m[-] ERROR: Invalid category '{category_code}'. Must be K, 20, 10, or 5.\033[0m")
            return

        if not os.path.exists(source_folder):
            print(f"\033[91m[-] ERROR: Source directory '{source_folder}' not found.\033[0m")
            return

        raw_files = [f for f in os.listdir(source_folder) if f.lower().endswith(('.jpeg', '.jpg', '.png', '.heic'))]
        
        if not raw_files:
            print(f"\033[93m[IDLE]\033[0m No visual artifacts found in {source_folder}.")
            return

        category = self.categories[category_code]
        target_folder = os.path.join(self.target_base_dir, category["folder"])
        os.makedirs(target_folder, exist_ok=True)

        print(f"\033[96m[DETECTED]\033[0m {len(raw_files)} artifacts. Initiating Bulk Anchoring to {category['name']} Vault...\n")

        # Load Ledger
        if not os.path.exists(os.path.dirname(self.ledger_path)):
            os.makedirs(os.path.dirname(self.ledger_path), exist_ok=True)
        try:
            with open(self.ledger_path, 'r') as f:
                ledger = json.load(f)
        except (FileNotFoundError, json.JSONDecodeError):
            ledger = []

        processed_count = 0
        for filename in raw_files:
            source_path = os.path.join(source_folder, filename)
            
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
                "status": "VERIFIED_BULK_INVENTORY"
            }
            ledger.append(ledger_entry)
            
            print(f"\033[92m[✓] ANCHORED:\033[0m {new_filename}")
            processed_count += 1

        # Save ledger
        with open(self.ledger_path, 'w') as f:
            json.dump(ledger, f, indent=4)

        print("\n\033[94m" + "="*65 + "\033[0m")
        print(f"\033[96m[BULK TRIAGE COMPLETE]\033[0m {processed_count} artifacts secured to Sovereign Ledger.")

if __name__ == "__main__":
    if len(sys.argv) < 3:
        print("Usage: python3 nexus_bulk_ingester.py <source_folder_path> <category_code>")
        sys.exit(1)
        
    source = sys.argv[1]
    cat_code = sys.argv[2]
    
    ingester = NexusBulkIngester()
    ingester.run_bulk_ingestion(source, cat_code)
