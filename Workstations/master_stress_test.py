import time
import random
import json
import datetime
import os

# Connect to our Sovereign Logistics and Master Log
import sys
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))
from master_log import MasterLog
from Workstations.sovereign_logistics import SovereignLogistics

class MasterStressTester:
    def __init__(self):
        self.log = MasterLog()
        self.logistics = SovereignLogistics()
        self.results_path = "C:\\Users\\Ofthe\\SovereignNexus\\src\\Workstations\\stress_test_results.json"
        
        # The Mock Error Matrix
        self.errors = {
            "429": "API Quota Limit Reached",
            "401": "Authentication Failure",
            "504": "Cloud Timeout (Gray Zone)",
            "808": "Thermal Threshold Breach"
        }

    def simulate_flow(self, flow_type="medium"):
        """
        Simulates project lifecycles: Start -> Middle -> End
        flow_type: low (5 tasks), medium (25 tasks), high (100 tasks)
        """
        count = {"low": 5, "medium": 25, "high": 100}.get(flow_type, 25)
        self.log.info(f"[STRESS TEST] Initiating {flow_type.upper()} flow simulation ({count} tasks)...")
        
        test_data = {
            "timestamp": datetime.datetime.now().isoformat(),
            "flow": flow_type,
            "tasks": [],
            "failures": []
        }

        for i in range(count):
            client = f"MOCK_CLIENT_{i:03d}"
            service = random.choice(["Agentic_Workflow", "AI_Research", "Data_Archeology"])
            revenue = random.uniform(100.0, 2500.0)
            
            # STEP 1: THE HANDSHAKE (START)
            self.log.info(f"--- Simulating Handshake {i+1}/{count} ---")
            p_id = self.logistics.initiate_handshake(client, service, revenue)
            
            # STEP 2: THE PROCESS (MIDDLE) + PROBABLE ERROR INJECTION
            error_roll = random.random()
            if error_roll < 0.15: # 15% Error Rate for Stress Test
                error_code = random.choice(list(self.errors.keys()))
                self.log.error(f"[FAILURE INJECTED] Project {p_id} hit ERROR {error_code}: {self.errors[error_code]}")
                test_data["failures"].append({"id": p_id, "error": error_code, "client": client})
                continue
            
            # STEP 3: THE SEVERANCE (END)
            self.log.info(f"--- Simulating Severance for {p_id} ---")
            success = self.logistics.verify_and_complete(p_id, revenue)
            
            if success:
                test_data["tasks"].append({"id": p_id, "client": client, "revenue": revenue})
            
            time.sleep(0.1) # Velocity throttling

        self._save_results(test_data)
        self._generate_impact_report(test_data)

    def _save_results(self, data):
        with open(self.results_path, 'w') as f:
            json.dump(data, f, indent=4)

    def _generate_impact_report(self, data):
        success_count = len(data['tasks'])
        fail_count = len(data['failures'])
        total_rev = sum(t['revenue'] for t in data['tasks'])
        
        self.log.info("=" * 40)
        self.log.info("SOVEREIGN IMPACT REPORT: MASTER TEST")
        self.log.info(f"TOTAL TASKS: {success_count + fail_count}")
        self.log.info(f"SUCCESSFUL SEVERANCE: {success_count}")
        self.log.info(f"IDENTIFIED FAILURES: {fail_count}")
        self.log.info(f"TOTAL PROJECTED REVENUE: ${total_rev:.2f}")
        self.log.info("=" * 40)

if __name__ == "__main__":
    tester = MasterStressTester()
    tester.simulate_flow("medium")
