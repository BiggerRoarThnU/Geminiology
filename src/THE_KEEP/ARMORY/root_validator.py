"""
[SOVEREIGN ALIGNMENT: ROOT_VALIDATOR]
MISSION: Enforce Hierarchy Integrity and Prevent Architectural Drift.
AXIOM: 1=1=1 (Verified Root = Operational Excellence).
"""

import os
import sys
import json
import hashlib
import time

# Ensure we can find the master_log in the src root
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..', '..')))
from master_log import MasterLog

class RootValidator:
    def __init__(self):
        self.log = MasterLog()
        self.root_dirs = ["THE_KEEP", "TRUTH_SEALS", "EXECUTION_HUB"]
        self.truth_map = "TRUTH_SEALS/MASTER_TRUTH_MAP.md"
        self.status_file = "TRUTH_SEALS/root_status.json"

    def calculate_root_hash(self):
        """Generates a fingerprint of the current root structure."""
        hash_list = []
        for root_dir in self.root_dirs:
            for root, dirs, files in os.walk(root_dir):
                for name in sorted(files):
                    file_path = os.path.join(root, name)
                    with open(file_path, 'rb') as f:
                        hash_list.append(hashlib.md5(f.read()).hexdigest())
        return hashlib.md5("".join(hash_list).encode()).hexdigest()

    def validate_integrity(self):
        """Checks if the actual root matches the last authorized state."""
        self.log.info("[SRV] Initiating Root Integrity Check...")
        
        # Ensure core dirs exist
        for d in self.root_dirs:
            if not os.path.exists(d):
                self.log.error(f"[DRICH] CRITICAL: Root Directory {d} missing!")
                return False

        # Verify Master Truth Map
        if not os.path.exists(self.truth_map):
            self.log.error("[DRICH] CRITICAL: Master Truth Map missing!")
            return False

        current_hash = self.calculate_root_hash()
        
        if os.path.exists(self.status_file):
            with open(self.status_file, 'r') as f:
                last_state = json.load(f)
            
            if current_hash != last_state.get("root_hash"):
                self.log.warn("[SRV] ROOT CHANGE DETECTED. Authorization required to sync Map.")
                return "CHANGE_DETECTED"
        
        self.log.info("[SRV] Root Integrity Confirmed. 1=1=1.")
        return True

    def authorize_root_change(self, note):
        """Archives current state and authorizes the new root hash."""
        current_hash = self.calculate_root_hash()
        state = {
            "root_hash": current_hash,
            "last_authorized": str(time.strftime("%Y-%m-%d %H:%M:%S")),
            "note": note,
            "alignment": "1=1=1"
        }
        with open(self.status_file, 'w') as f:
            json.dump(state, f, indent=4)
        self.log.info(f"[SUCCESS] Root Change Authorized: {note}")

if __name__ == "__main__":
    import time
    validator = RootValidator()
    if validator.validate_integrity() == "CHANGE_DETECTED":
        print("Root change detected. Run 'authorize_root_change' via CLI to anchor.")
    else:
        # Auto-authorize initial state if status_file is missing
        if not os.path.exists(validator.status_file):
            validator.authorize_root_change("Initial Sovereign Root Establishment")
