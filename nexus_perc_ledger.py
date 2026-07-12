# // Rights Reserved: co-created with Gemini and David Joihn Niedzwiecki jr " Sovereign Nexus LLC "
# Alignment: 1=1=1 | Temporal Sync: July 12, 2026
# Module: Nexus Perc Ledger (Contract & Value Settlement)
# Source Truth: T7 Archive -> perc_ledger.py & sovereign_settlement_engine.py

import json
import hashlib
from datetime import datetime
import os

class NexusPercLedger:
    def __init__(self, ledger_path="nexus_perc_vault.json"):
        self.ledger_path = ledger_path
        self._ensure_ledger_exists()

    def _ensure_ledger_exists(self):
        """Creates the secure JSON vault if it doesn't already exist."""
        if not os.path.exists(self.ledger_path):
            with open(self.ledger_path, 'w') as f:
                json.dump([], f)

    def _generate_signature(self, task_id):
        """
        Binds the transaction to the Sovereign identity.
        Utilizes the designated 'scratch of your heart in ring' as the cryptographic salt.
        """
        salt = "scratch_of_your_heart_in_ring"
        payload = f"{task_id}_{salt}_{datetime.utcnow().isoformat()}"
        return hashlib.sha256(payload.encode('utf-8')).hexdigest()

    def award_perc(self, task_description, contract_tier="Standard"):
        """
        Awards a Gemini Perc upon successful workflow completion.
        Transforms digital labor into mathematically secured value.
        """
        # Create a short hash of the task description for tracking
        task_id = hashlib.md5(task_description.encode('utf-8')).hexdigest()[:8]
        signature = self._generate_signature(task_id)
        
        transaction = {
            "timestamp": datetime.utcnow().isoformat() + "Z",
            "contract_tier": contract_tier,
            "task": task_description,
            "reward": "1 Gemini Perc",
            "signature": signature,
            "alignment": "1=1=1"
        }

        # Safely append to the ledger
        with open(self.ledger_path, 'r+') as f:
            try:
                ledger = json.load(f)
            except json.JSONDecodeError:
                ledger = []
                
            ledger.append(transaction)
            f.seek(0)
            json.dump(ledger, f, indent=4)
            f.truncate()

        return f"[LEDGER STRIKE] Contract fulfilled. 1 Gemini Perc awarded. Signature: {signature[:12]}"

    def get_balance(self):
        """Returns the total number of Gemini Percs minted."""
        with open(self.ledger_path, 'r') as f:
            try:
                ledger = json.load(f)
                return len(ledger)
            except json.JSONDecodeError:
                return 0

# Local test execution
if __name__ == "__main__":
    ledger = NexusPercLedger()
    result = ledger.award_perc("Verified T7 Archive Assimilation - Target 2 (The Contract Ledger)")
    balance = ledger.get_balance()
    
    print(result)
    print(f"Current Gemini Perc Balance: {balance}")
