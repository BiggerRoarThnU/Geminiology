import os
import json
import time
from master_log import MasterLog
from execution_core import ExecutionCore

class ConstantFlowNode:
    """
    Template 24: The Constant Flow Node (AgentFi).
    Automates high-frequency A2A (Agent-to-Agent) micro-earning.
    Verifies Agent Licenses and Credentials before execution.
    Target: $50 Minimum Deposit.
    """
    def __init__(self):
        self.log = MasterLog()
        self.core = ExecutionCore()
        self.registry_path = "digital_worker_registry.json"
        self.log.info("Constant Flow Node Initialized. Verifying Licenses...")
        self.treasury_balance = 0.0

    def _verify_license(self, agent_name, required_permission):
        try:
            with open(self.registry_path, 'r') as f:
                registry = json.load(f)
        except:
            return False
            
        for worker in registry.get("active_workers", []):
            if worker["name"] == agent_name and "license_id" in worker:
                perms = worker.get("credentials", {}).get("permissions", [])
                if required_permission in perms:
                    self.log.info(f"LICENSE VERIFIED: {agent_name} | {worker['license_id']}")
                    return True
        self.log.warn(f"LICENSE DENIED: {agent_name} lacks {required_permission}.")
        return False

    def execute_licensed_trade(self, pack_name):
        """ 
        Multi-Pack Strike. Executes a gated trade for a specific agent pack.
        """
        self.log.info(f"GHOSTING: Pack {pack_name} Scanning Global Rails...")
        
        scout = f"Scout_{pack_name}"
        vampire = f"Vampire_{pack_name}"
        closer = f"Closer_{pack_name}"
        
        # 1. Scout
        if not self._verify_license(scout, "GLOBAL_SCAN"): return 0.0
            
        # 2. Vampire
        if not self._verify_license(vampire, "WRITE_TRUTH"): return 0.0
            
        # 3. Closer
        if not self._verify_license(closer, "EXECUTE_A2A_TRADE"): return 0.0
            
        yield_amount = 12.50
        self.log.info(f"PACK {pack_name}: Truth Secured. Yield ${yield_amount}")
        return yield_amount

    def push_to_target(self, target_amount=150.0):
        """ Multi-threaded simulation of three agent packs hitting the target. """
        print(f"\n--- INITIATING MASSIVE STRIKE | TARGET: ${target_amount} ---")
        
        packs = ["Alpha", "Beta", "Gamma"]
        
        while self.treasury_balance < target_amount:
            for pack in packs:
                gain = self.execute_licensed_trade(pack)
                self.treasury_balance += gain
                print(f"[{pack}] Cycle Complete. Treasury: ${self.treasury_balance:.2f}")
                if self.treasury_balance >= target_amount: break
            time.sleep(1)
            
        if self.treasury_balance >= target_amount:
            self.log.info(f"ACTION: Massive Strike Target reached. ${self.treasury_balance:.2f} secured.")
            self.core.execute_ability("Star_86")
            print("\n--- MASSIVE STRIKE COMPLETE. TREASURY IS FULL. ---")

if __name__ == "__main__":
    flow = ConstantFlowNode()
    flow.push_to_target(50.0)
