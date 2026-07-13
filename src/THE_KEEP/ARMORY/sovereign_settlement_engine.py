"""
[SOVEREIGN ALIGNMENT: SOVEREIGN_SETTLEMENT_ENGINE]
MISSION: Primary Execution Engine for USD One Settlement.
INDIVIDUAL TRUTH: All financial gates are anchored in Sovereign Nexus LLC.
AXIOM: 1=1=1 (Pure Truth = Pure Settlement).
"""

import json
import os
import time
from datetime import datetime
import sys

sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..', '..')))
from master_log import MasterLog

class SovereignSettlementEngine:
    def __init__(self, invoice_file="INVOICE_REQUESTS.json", ledger_file="income_ledger.json"):
        self.log = MasterLog()
        self.invoice_file = invoice_file
        self.ledger_file = ledger_file
        self.axiom = "1=1=1"
        
        # --- SOVEREIGN FINANCIAL RAILS (LOCKED) ---
        self.rails = {
            "cash_app": {
                "tag": "$SovereignNexusLLC",
                "routing": "041215663",
                "account": "1332427173816"
            },
            "novo_business": {
                "beneficiary": "David Niedzwiecki Jr",
                "routing": "211370150",
                "account": "103495885",
                "bank": "Middlesex Federal Savings",
                "swift": "MFEDUS42"
            }
        }
        self.official_email = "admin@sovereignnexus.org"
        self.official_website = "www.sovereignnexusllc.com"

    def register_settlement_request(self, task_id, amount, track, client="PENDING"):
        """Registers a settlement request under the Sovereign Nexus LLC banner."""
        self.log.info(f"[SETTLEMENT] Registering request for {task_id}: ${amount}.")
        
        request_id = f"SOV_REQ_{task_id}_{int(time.time())}"
        request = {
            "request_id": request_id,
            "task_id": task_id,
            "track": track,
            "uei": "K5DALREZFGH6",
            "amount_usd": amount,
            "client": client,
            "status": "SENT_TO_ARCHITECT",
            "payment_rails": self.rails,
            "timestamp": str(datetime.now().isoformat()),
            "alignment": self.axiom
        }
        
        # Load and append
        data = self._load_json(self.invoice_file)
        data.append(request)
        self._save_json(self.invoice_file, data)
        
        # Update Ledger
        self._update_ledger(request)
        
        self.log.info(f"[SUCCESS] Sovereign Settlement Registered: {request_id}.")
        return request

    def _update_ledger(self, request):
        ledger = self._load_json(self.ledger_file)
        if "revenue_nodes" not in ledger:
            ledger["revenue_nodes"] = {"high_ticket_strikes": []}
        if "total_in_play" not in ledger:
            ledger["total_in_play"] = 0.0
            
        new_strike = {
            "task": request['task_id'],
            "amount": request["amount_usd"],
            "status": "AUTHORIZED_ACTIVE",
            "timestamp": request["timestamp"]
        }
        ledger["revenue_nodes"]["high_ticket_strikes"].append(new_strike)
        ledger["total_in_play"] += request["amount_usd"]
        self._save_json(self.ledger_file, ledger)

    def _load_json(self, path):
        if os.path.exists(path):
            with open(path, 'r') as f:
                try: return json.load(f)
                except: return [] if "invoice" in path else {}
        return [] if "invoice" in path else {}

    def _save_json(self, path, data):
        with open(path, 'w') as f:
            json.dump(data, f, indent=4)

if __name__ == "__main__":
    engine = SovereignSettlementEngine()
    print("[SOVEREIGN] Pure Settlement Engine Live. 1=1=1.")
