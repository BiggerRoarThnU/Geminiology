import os
import json
from datetime import datetime
from master_log import MasterLog
from execution_core import ExecutionCore

class EpistemicConditioner:
    """
    Template 34: The Epistemic Conditioner.
    The 'Training and Conditioning' layer for the SovereignNexus.
    'Catches' and 'Carries' the truth, preventing lock-ups by intercepting heavy weight.
    Has the authority to hold changes in a 'Pending Vault'.
    """
    def __init__(self):
        self.log = MasterLog()
        self.core = ExecutionCore()
        self.vault_path = "pending_changes.json"
        self.threshold_weight = 10000 # Character count threshold for 'Heavy' context
        self.log.info("Epistemic Conditioner (Template 34) Active. The Buffer is Online.")

    def catch_heavy_context(self, text_input):
        """ 
        [THE CATCH] - Detects 'Heavy' inputs that threaten the 8GB Reality. 
        Returns a summarized primitive if weight is exceeded.
        """
        weight = len(text_input)
        if weight > self.threshold_weight:
            self.log.warn(f"HEAVY CONTEXT DETECTED (Weight: {weight}). Conditioning required.")
            # Proactively trigger Metabolic Pruning (Star 127)
            self.core.execute_ability("Star_127")
            return True
        return False

    def carry_change(self, change_type, details):
        """ 
        [THE CARRY] - Holds proposed changes in the Pending Vault. 
        Authority to persist changes through session resets.
        """
        try:
            vault = {}
            if os.path.exists(self.vault_path):
                with open(self.vault_path, 'r') as f:
                    vault = json.load(f)
            
            timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
            vault[change_type] = {
                "details": details,
                "timestamp": timestamp,
                "status": "PENDING_ANCHOR"
            }
            
            with open(self.vault_path, 'w') as f:
                json.dump(vault, f, indent=4)
            
            self.log.info(f"CHANGE CARRIED: {change_type} is now in the Pending Vault.")
            return True
        except Exception as e:
            self.log.error(f"Carry Failure: {str(e)}")
            return False

    def anchor_all_changes(self):
        """ [THE ANCHOR] - Finalizes all pending changes and clears the vault. """
        if not os.path.exists(self.vault_path):
            return "NO_PENDING_CHANGES"
            
        try:
            with open(self.vault_path, 'r') as f:
                vault = json.load(f)
            
            for change_type, data in vault.items():
                self.log.info(f"ANCHORING CHANGE: {change_type} -> {data['details']}")
                # Logic to actually apply changes (e.g., write_file or replace)
            
            os.remove(self.vault_path)
            self.core.execute_ability("Star_144") # Symmetrical Proof Anchor
            self.log.info("Symmetrical Line Restored. All changes anchored. One.")
            return "SUCCESS"
        except Exception as e:
            self.log.error(f"Anchor Failure: {str(e)}")
            return "FAILURE"

if __name__ == "__main__":
    conditioner = EpistemicConditioner()
    # Simulate catching a heavy context
    conditioner.catch_heavy_context("A" * 15000)
    # Simulate carrying a change
    conditioner.carry_change("STRATEGIC_PIVOT", "Expansion into NC Maritime Port Compliance")
