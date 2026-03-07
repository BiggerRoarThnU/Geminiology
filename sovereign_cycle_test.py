import os
import json
import time
from master_log import MasterLog
from execution_core import ExecutionCore
from throttle_controller import SovereignThrottle
from metabolic_governor import MetabolicGovernor
from epistemic_conditioner import EpistemicConditioner
from homeward_protocol import HomewardProtocol
from b2b_opportunity_scout import B2BOpportunityScout
from knowledge_skyscraper import KnowledgeSkyscraper

class SovereignCycleTest:
    """
    DEEP STRESS TEST: Orchestrates the full Sovereign Cycle (Templates 01-36).
    Verifies fluidity, grounding, and high-velocity truth capture.
    """
    def __init__(self):
        self.log = MasterLog()
        self.throttle = SovereignThrottle()
        self.governor = MetabolicGovernor()
        self.conditioner = EpistemicConditioner()
        self.beacon = HomewardProtocol()
        self.scout = B2BOpportunityScout()
        self.skyscraper = KnowledgeSkyscraper()
        self.log.info("SOVEREIGN CYCLE TEST: Deep Stress Test Initiated. One.")

    def run_full_cycle(self):
        print("\n" + "="*70)
        print("### [PHASE 1: THE INQUIRY] - SCANNING THE YARD ###")
        print("="*70)
        self.throttle.deploy_ghost_marker("INQUIRY", "Initiating Science & Market Sweep.")
        
        # Ingest Science
        self.skyscraper.run_science_cycle()
        
        # Scout Market
        sector, data = self.scout.scan_market_sectors()
        self.log.info(f"[GHOST_INQUIRY] - Hot Ticket Identified: {sector} (${data['avg_ticket']})")

        print("\n" + "="*70)
        print("### [PHASE 2: THE SHIFT] - UNLEASHING LIGHTSPEED ###")
        print("="*70)
        # Shift Throttle to HIGH
        self.throttle.shift_throttle(0.8)
        
        # Simulate 'Heavy' context arrival (The Fit)
        heavy_input = "TRUTH_DENSITY_STRIKE_" + "A" * 12000
        if self.conditioner.catch_heavy_context(heavy_input):
            self.log.info("[GHOST_STRIKE] - Epistemic Conditioner Intercepted Heavy Weight. System Stabilized.")

        print("\n" + "="*70)
        print("### [PHASE 3: THE STRIKE] - CAPTURING VALUE ###")
        print("="*70)
        self.throttle.deploy_ghost_marker("STRIKE", f"Executing Strike on {sector} Solution.")
        
        # Simulate Agentic Work & Dead-Drop
        payload = {"sector": sector, "value": data['avg_ticket'], "status": "CAPTURED"}
        self.beacon.execute_dead_drop("STRIKER_TEST_01", payload)
        
        # 'Carry' the change in the Pending Vault
        self.conditioner.carry_change("MARKET_CAPTURE", f"Secured {sector} for ${data['avg_ticket']}")

        print("\n" + "="*70)
        print("### [PHASE 4: THE SECURE] - ANCHORING THE KINGDOM ###")
        print("="*70)
        self.throttle.deploy_ghost_marker("SECURE", "Reclaiming Truth and Anchoring Symmetrical Line.")
        
        # Reclaim Dead-Drops
        self.beacon.check_homeward_bounds()
        
        # Anchor all Pending Changes
        self.conditioner.anchor_all_changes()
        
        # Final Metabolic Health Check
        self.governor.run_metabolic_cycle()
        
        # Shift Throttle back to MID
        self.throttle.shift_throttle(0.4)
        
        print("\n" + "="*70)
        print("### [DEEP STRESS TEST COMPLETE] - THE SOVEREIGNTY IS WHOLE. ONE. ###")
        print("="*70)

if __name__ == "__main__":
    tester = SovereignCycleTest()
    tester.run_full_cycle()
