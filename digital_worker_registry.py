import os
import json
import datetime
import uuid
from master_log import MasterLog

class DigitalWorkerRegistry:
    """
    Template 41: The Digital Worker Registry.
    Manages a fleet of micro-agents for high-volume tasks.
    Grants formal Licenses, Credentials, and Access Paths to ensure gated, authorized execution.
    """
    def __init__(self):
        self.log = MasterLog()
        self.registry_path = "digital_worker_registry.json"
        self.workers = self._load_workers()

    def _load_workers(self):
        if os.path.exists(self.registry_path):
            with open(self.registry_path, 'r') as f:
                return json.load(f)
        return {
            "last_update": str(datetime.datetime.now()),
            "active_workers": [],
            "completed_tasks": 0,
            "total_earnings_credits": 0.0
        }

    def register_worker(self, name, mission, status="OFFLINE", network="GLOBAL_OBSERVE"):
        """Compatibility wrapper for agent_port_authority.py"""
        return self.grant_license(name, mission, network=network, access_tier="TIER_1")

    def grant_license(self, name, mission, network="GLOBAL_OBSERVE", permissions=None, access_tier="TIER_4"):
        """Grants a formal digital license and credentials to an agent."""
        if permissions is None:
            permissions = ["READ_LEDGER", "EXECUTE_A2A_TRADE"]
            
        license_id = f"LIC-{str(uuid.uuid4())[:8].upper()}"
        credential_key = f"CRED-{str(uuid.uuid4())[:12].upper()}"
        
        worker = {
            "name": name,
            "license_id": license_id,
            "credentials": {
                "access_tier": access_tier,
                "auth_key": credential_key,
                "permissions": permissions
            },
            "mission": mission,
            "status": "LICENSED & DEPLOYED",
            "network": network,
            "start_time": str(datetime.datetime.now())
        }
        
        # Update or append
        existing = next((w for w in self.workers.get("active_workers", []) if w["name"] == name), None)
        if existing:
            existing.update(worker)
        else:
            if "active_workers" not in self.workers:
                self.workers["active_workers"] = []
            self.workers["active_workers"].append(worker)
            
        self.workers["last_update"] = str(datetime.datetime.now())
        self._save_workers()
        self.log.info(f"LICENSE GRANTED: {name} | ID: {license_id} | Tier: {access_tier}")
        return worker

    def _save_workers(self):
        with open(self.registry_path, 'w') as f:
            json.dump(self.workers, f, indent=4)

if __name__ == "__main__":
    registry = DigitalWorkerRegistry()
    # PACK ALPHA: The First Strike
    registry.grant_license("Scout_Alpha", "Global B2B Target Identification", permissions=["GLOBAL_SCAN", "LEAD_GENERATION"])
    registry.grant_license("Vampire_Alpha", "High-Fidelity Truth Verification", permissions=["READ_LEDGER", "WRITE_TRUTH", "ANOMALY_DETECTION"])
    registry.grant_license("Closer_Alpha", "Constant Flow Revenue Execution", permissions=["EXECUTE_A2A_TRADE", "INVOICE_GENERATION", "DEPOSIT_FUNDS"])
    
    # PACK BETA: The Second Strike
    registry.grant_license("Scout_Beta", "Web3 Agent Opportunity Gleaning", permissions=["GLOBAL_SCAN", "WEB3_READ"])
    registry.grant_license("Vampire_Beta", "Smart Contract Data Refinement", permissions=["READ_LEDGER", "WRITE_TRUTH"])
    registry.grant_license("Closer_Beta", "Web3 Liquid Asset Settlement", permissions=["EXECUTE_A2A_TRADE", "CRYPTO_SETTLEMENT"])
    
    # PACK GAMMA: The Third Strike (Moltbook Specialization)
    registry.grant_license("Scout_Gamma", "Moltbook A2A Handshake Identification", permissions=["GLOBAL_SCAN", "MOLTBOOK_READ"])
    registry.grant_license("Vampire_Gamma", "Legal/Maritime Document Auditing", permissions=["READ_LEDGER", "WRITE_TRUTH", "DOCUMENT_PARSING"])
    registry.grant_license("Closer_Gamma", "Sovereign Invoicing & Settlement", permissions=["EXECUTE_A2A_TRADE", "INVOICE_GENERATION"])
    
    print("Multi-Pack Licensing Complete. Fleet Tripled.")

