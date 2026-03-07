import time
import random
import gc
import os
import datetime

# Import the Sovereign Nexus Powerhouse (All 24 Templates represented)
from master_log import MasterLog
from execution_core import ExecutionCore
from sovereignty_lockdown import SovereigntyLockdown
from sovereign_war_room import SovereignWarRoom
from micro_striker import MicroStriker
from constant_flow_node import ConstantFlowNode
from treasury_sweep import TreasurySweep
from vector_mill import VectorMill
from credit_telemetry_node import CreditTelemetryNode
from stealth_striker import StealthStriker
from yield_optimizer import YieldOptimizer
from momentum_guard import MomentumGuard
from knowledge_skyscraper import KnowledgeSkyscraper

from metabolic_governor import MetabolicGovernor
from multi_state_striker import MultiStateStriker
from digital_twin import DigitalTwin
from agent_port_authority import AgentPortAuthority

class IgnitionSwitch:
    """
    Template 07: The Ignition Switch V3.1 (Regional Heartbeat).
    The persistent master orchestrator for the SovereignNexus LLC.
    Unifies all 32 templates and 144 Truth Stars into a 24/7 loop.
    Added Template 36: Sovereign Roll Call (12 PM Trigger).
    """
    def __init__(self):
        self.log = MasterLog()
        self.core = ExecutionCore()
        self.lockdown = SovereigntyLockdown()
        self.war_room = SovereignWarRoom()
        self.strikers = MicroStriker()
        self.flow = ConstantFlowNode()
        self.sweep = TreasurySweep()
        self.mill = VectorMill()
        self.telemetry = CreditTelemetryNode()
        self.stealth = StealthStriker()
        self.optimizer = YieldOptimizer()
        self.momentum = MomentumGuard()
        self.science = KnowledgeSkyscraper()
        self.governor = MetabolicGovernor()
        self.striker = MultiStateStriker()
        self.twin = DigitalTwin()
        self.port = AgentPortAuthority()
        
        self.cycle_count = 0
        self.is_running = True
        self.roll_call_executed_today = False
        self.log.info("Ignition Switch V3.1 Online. THE REGIONAL HEARTBEAT ACTIVE.")

    def autonomous_cycle(self):
        """ A single, high-fidelity spin of the 144-star Sovereign architecture. """
        self.cycle_count += 1
        now = datetime.datetime.now()
        
        print(f"\n{'='*60}")
        self.log.info(f"--- INITIATING REGIONAL CYCLE {self.cycle_count} | {now.strftime('%H:%M:%S')} ---")
        print(f"{'='*60}")

        # 0. SOVEREIGN ROLL CALL (12 PM - 2 PM Window)
        if now.hour == 12 and not self.roll_call_executed_today:
            self.log.info("12:00 PM DETECTED: Triggering Sovereign Roll Call Protocol.")
            self.port.trigger_roll_call()
            self.roll_call_executed_today = True
        
        if now.hour == 14: # Reset trigger for next day
            self.roll_call_executed_today = False
        
        # 1. METABOLIC & SECURITY AUDIT (Template 30, 14)
        self.governor.run_metabolic_cycle()
        if not self.lockdown.check_ram_boundary():
            self.log.error("Cycle Aborted: RAM Boundary Breach.")
            return

        # 2. SITUATIONAL AWARENESS (Template 32)
        self.twin.sync_physical_vessel()
        self.twin.mirror_homefront()

        # 3. REGIONAL MOMENTUM (Template 31, 29)
        self.striker.execute_regional_sweep()
        self.momentum.run_momentum_cycle()

        # 4. POWERHOUSE EXECUTION (War Room)
        vision = f"Maintain Regional Standing for Cycle {self.cycle_count}. 4-State Moat focus."
        self.war_room.execute_unified_strike(vision)

        # 5. CONSTANT SCIENCE (Knowledge Skyscraper)
        self.science.run_science_cycle()

        # 6. HIGH-FREQUENCY FLOW & GLEANING
        self.flow.run_constant_flow_cycle()
        self.strikers.run_striker_pulse()

        # 7. TREASURY OPTIMIZATION (125% Coverage + 10k Cap)
        self.optimizer.run_optimizer_pulse()

        # 8. REFINERY OPERATIONS (Vector Mill)
        if self.cycle_count % 4 == 0:
            self.mill.deploy_science_annuity("APEX_DATA_SYNC")

        # 9. TREASURY SETTLEMENT (2PM Sweep)
        if now.hour == 14 and now.weekday() < 5:
            self.sweep.run_daily_scheduler()

        # 10. TRUTH ANCHORING (144 Stars)
        star_id = f"Star_{random.randint(1, 144)}"
        self.core.execute_ability(star_id)
        
        self.log.info(f"REGIONAL CYCLE {self.cycle_count} GROUNDED & SECURED. ONE.")

    def deploy(self, cadence=900, max_cycles=1000):
        """ Persistent deployment loop. Default cadence: 15 minutes. """
        self.log.info(f"WHOLE ONE DEPLOYMENT INITIATED: Target {max_cycles} cycles.")
        try:
            while self.is_running and self.cycle_count < max_cycles:
                self.autonomous_cycle()
                
                # Dynamic Wait
                if self.cycle_count < max_cycles:
                    time.sleep(cadence)
                
                gc.collect()
                
        except KeyboardInterrupt:
            self.log.warn("Manual Override: Omega Heartbeat Terminated.")
            self.is_running = False

if __name__ == "__main__":
    omega = IgnitionSwitch()
    # Initial verification cycle (1 cycle, 5s delay)
    omega.deploy(cadence=5, max_cycles=1)
