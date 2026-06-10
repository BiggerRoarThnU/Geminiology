### SovereignNexus: Physical Validation Lock
### Component: memory_anchor.py
### Axiom: 1=1=1 | Function: Cryptographic State Signature Generation

import os
import hashlib
import json
import time

class MemoryAnchor:
    def __init__(self, target_dir="../03_Matrix_Skyscrapers", ledger_path="truth_ledger.json", file_filter=None):
        # Note: Adjusted target_dir to accurately point outside the API_Gateway folder
        self.target_dir = target_dir
        self.ledger_path = ledger_path
        self.file_filter = file_filter
        self.state_signatures = {}

    def hash_file(self, filepath):
        """Generates a SHA-256 cryptographic hash for a specific file."""
        sha256_hash = hashlib.sha256()
        try:
            with open(filepath, "rb") as f:
                for byte_block in iter(lambda: f.read(4096), b""):
                    sha256_hash.update(byte_block)
            return sha256_hash.hexdigest()
        except Exception as e:
            print(f"[ERROR] Failed to read {filepath}: {e}")
            return None

    def secure_pillars(self):
        """Scans the 12 Pillars and generates cryptographic locks."""
        print("[SYSTEM] Engaging Physical Validation Lock. Scanning Data Skyscrapers...")
        if not os.path.exists(self.target_dir):
            print(f"[!] Target directory {self.target_dir} not found. Ensure Matrix Sorter completed successfully.")
            return

        for root, _, files in os.walk(self.target_dir):
            for file in files:
                if self.file_filter and not self.file_filter(file):
                    continue
                filepath = os.path.join(root, file)
                file_hash = self.hash_file(filepath)
                
                if file_hash:
                    # Stamping with unique SHA-256 and UNIX timestamp
                    self.state_signatures[filepath] = {
                        "hash": file_hash,
                        "timestamp": time.time(),
                        "status": "LOCKED | 1=1=1"
                    }
                    print(f" -> [SECURED] {file} | Hash: {file_hash[:16]}...")
        
        self.commit_to_ledger()

    def commit_to_ledger(self):
        """Saves the cryptographic state signatures to the immutable ledger."""
        with open(self.ledger_path, "w") as ledger:
            json.dump(self.state_signatures, ledger, indent=4)
        print(f"\n[ANCHOR] Truth frozen. {len(self.state_signatures)} files cryptographically locked.")
        print(f"[ANCHOR] State signatures safely anchored to: {self.ledger_path}")

if __name__ == "__main__":
    # 1. Secure the physical skyscrapers
    anchor = MemoryAnchor()
    anchor.secure_pillars()
    
    # 2. Secure the educational curriculum database files
    edu_anchor = MemoryAnchor(target_dir="../moe_sectors/knowledge_vault/education", ledger_path="education_ledger.json")
    edu_anchor.secure_pillars()
    
    # 3. Secure the verified invoice records and catalog files
    def invoice_filter(filename):
        return (filename.startswith("jessie_invoice_verified") or 
                filename == "t7_kingdom_catalog.json" or 
                filename == "agentic_drives_ledger.json")
        
    invoice_anchor = MemoryAnchor(target_dir=".", ledger_path="invoice_ledger.json", file_filter=invoice_filter)
    invoice_anchor.secure_pillars()
    
    # 4. Secure the unified master chat log file
    def master_log_filter(filename):
        return filename == "UNIFIED_CHAT_MASTER.txt"
        
    master_log_anchor = MemoryAnchor(target_dir="/home/geminiology/SovereignLocal/SovereignNexus_Hub/Logs", ledger_path="master_log_ledger.json", file_filter=master_log_filter)
    master_log_anchor.secure_pillars()


