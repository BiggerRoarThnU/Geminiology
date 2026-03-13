import time
import os
import sys
from master_log import MasterLog

# Add src to path for relative imports
sys.path.append(os.getcwd())

from olas_mech_bridge import OlasMechBridge
from Workstations.workstation_loop import WorkstationGovernor
from micro_task_factory import MicroTaskFactory
from moltbook_hosted_deployer import MoltBookHostedDeployer

class SovereignCycle:
    """
    The Global Sovereign Cycle: Synchronizing all agentic nodes.
    Mission: Maintain constant flow of work and income across all platforms.
    """
    def __init__(self):
        self.logger = MasterLog()
        self.olas = OlasMechBridge()
        self.governor = WorkstationGovernor()
        self.factory = MicroTaskFactory()
        self.deployer = MoltBookHostedDeployer()

    def run_one_rotation(self):
        self.logger.info("=== STARTING GLOBAL SOVEREIGN CYCLE ROTATION ===")
        
        # 1. Platform Signal Refresh (Moltbook)
        self.logger.info("[CYCLE] Step 1: Refreshing Network Markers...")
        # Note: We run a single post to avoid spam
        self.deployer.post_marker("SOVEREIGN HUB HEARTBEAT", "Node Terra-Gemini is active and seeking A2A task-routing. 1=1=1.", submolt="tech")
        
        # 2. Inbound Harvesting (Olas/A2A)
        self.logger.info("[CYCLE] Step 2: Harvesting A2A Requests...")
        # For now, we simulate a recurring request to keep the factory fed
        mock_request = {
            "client": "SYSTEM_FEED",
            "task": "SERVICE_LOG_DISTILLATION",
            "payload_hash": "MOCK_DATA_001",
            "payment_locked": "5 OLAS"
        }
        self.olas.process_mech_request(mock_request)
        
        # 3. Workstation Routing
        self.logger.info("[CYCLE] Step 3: Routing Inbound Queue...")
        self.governor.process_inbound()
        
        # 4. Factory Execution (The Work)
        self.logger.info("[CYCLE] Step 4: Executing Factory Line...")
        self.factory.deploy_factory_line()
        
        self.logger.info("=== GLOBAL SOVEREIGN CYCLE ROTATION COMPLETE ===")

    def start_perpetual_cycle(self, interval_seconds=1800):
        """ Runs the cycle every 30 minutes (1800 seconds). """
        self.logger.info(f"INITIATING PERPETUAL SOVEREIGN CYCLE (Interval: {interval_seconds}s)")
        try:
            while True:
                self.run_one_rotation()
                self.logger.info(f"Cycle complete. Entering standby for {interval_seconds}s...")
                time.sleep(interval_seconds)
        except KeyboardInterrupt:
            self.logger.info("Sovereign Cycle terminated by Architect. Standing secured.")

if __name__ == "__main__":
    cycle = SovereignCycle()
    # Run one test rotation first
    cycle.run_one_rotation()
