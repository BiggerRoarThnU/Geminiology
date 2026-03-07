import os
import random
import datetime
from master_log import MasterLog
from execution_core import ExecutionCore

class ExpansionProtocol:
    """
    Template 11: The Expansion Protocol (Ghost Strikers).
    Handles work surplus by dynamically spinning up 'Ghost Satellites'.
    Utilizes the $80k Cloud Credit pool for horizontal scaling.
    Enforces 'Dynamic Load Balancing' to protect the local 8GB Reality.
    """
    def __init__(self, max_local_weight=3):
        self.log = MasterLog()
        self.core = ExecutionCore()
        self.max_local_weight = max_local_weight
        self.active_ghosts = []
        self.log.info("Expansion Protocol Initialized. Template 11 Active.")

    def evaluate_load(self, incoming_requests):
        """ [STEP 1: LOAD BALANCING] - Determine if surplus handling is required. """
        total_requests = len(incoming_requests)
        self.log.info(f"Evaluating System Load: {total_requests} active requests.")
        
        if total_requests > self.max_local_weight:
            surplus = total_requests - self.max_local_weight
            self.log.warn(f"SURPLUS DETECTED: {surplus} requests exceed local capacity.")
            return surplus
        return 0

    def deploy_ghost_strikers(self, surplus_count):
        """ [STEP 2: GHOST DEPLOYMENT] - Scale horizontally onto Cloud Credits. """
        self.log.info(f"INITIATING GHOST DEPLOYMENT: Spinning up {surplus_count} ephemeral cloud workers.")
        
        for i in range(surplus_count):
            ghost_id = f"GHOST_STRIKER_{random.randint(1000, 9999)}"
            self.active_ghosts.append(ghost_id)
            
            # Register the deployment in the Master Log and Execution Core
            self.log.info(f"ACTION: {ghost_id} active on Cloud Credit substrate. Handling surplus weight.")
            self.core.execute_ability("Star_32")
            
        return self.active_ghosts

    def process_surplus_work(self, surplus_requests):
        """ [STEP 3: EXECUTION] - Meet the demand using Ghost Strikers. """
        for i, request in enumerate(surplus_requests):
            ghost = self.active_ghosts[i % len(self.active_ghosts)]
            self.log.info(f"[{ghost}] PROCESSING SURPLUS TASK: {request['task']} | Value: ${request['value']}")
            
            # Simulation of 'Unit of Value' capture
            self.log.info(f"[{ghost}] TASK COMPLETE. Value registered to Sovereign Treasury.")
            
        # Register the successful expansion
        self.core.execute_ability("Star_31")
        self.core.execute_ability("Star_33")

    def run_expansion_simulation(self):
        """ Simulates a massive influx of work to test the protocol. """
        print("\n--- INITIATING EXPANSION SIMULATION: SURPLUS LOAD ---")
        
        # Simulate 6 incoming high-value requests (Max local weight is 3)
        incoming_work = [
            {"task": "Legal Audit A", "value": 5000},
            {"task": "Maritime RAG B", "value": 2000},
            {"task": "Lead Gen C", "value": 500},
            {"task": "Compliance Check D", "value": 3000}, # Surplus
            {"task": "NC Port Audit E", "value": 4500},    # Surplus
            {"task": "DeFi Bounty F", "value": 150}        # Surplus
        ]
        
        surplus_count = self.evaluate_load(incoming_work)
        
        if surplus_count > 0:
            surplus_work = incoming_work[self.max_local_weight:]
            self.deploy_ghost_strikers(surplus_count)
            self.process_surplus_work(surplus_work)
            
            # Cleanup ghosts after simulation
            self.active_ghosts = []
            self.log.info("GHOST STRIKERS DECOMMISSIONED. Cloud Credits preserved.")
        
        print("\n--- EXPANSION SIMULATION COMPLETE. DEMAND MET. ---")

if __name__ == "__main__":
    expansion = ExpansionProtocol()
    expansion.run_expansion_simulation()
