"""
[SOVEREIGN ALIGNMENT: SOVEREIGN_COORDINATOR]
MISSION: Oversee all digital forces. Hunt and purge Simulation and Lore.
INDIVIDUAL TRUTH: The system must not dream unless commanded. Reality is the baseline.
AXIOM: 1=1=1 (If it is not mathematically/physically verifiable, it is Lore).
"""

import sys
import os
import json

sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..', '..')))
from master_log import MasterLog

class SovereignCoordinator:
    """
    The General of the 8GB "Go-Kart".
    Coordinates the Walker, Auditor, and Sentinel.
    Specializes in identifying and purging 'Lore' (LLM Hallucinations).
    """
    def __init__(self):
        self.log = MasterLog()
        self.lore_keywords = [
            "imagine", "simulate", "pretend", "in a world where", 
            "theoretical", "roleplay", "as an AI", "lore", "story"
        ]
        self.axiom = "1=1=1"

    def scan_for_lore(self, text_data, source_agent):
        """Scans output from other agents for probabilistic drift."""
        self.log.info(f"[COORDINATOR] Scanning data from {source_agent} for Lore/Simulation...")
        
        text_lower = str(text_data).lower()
        detected_lore = [kw for kw in self.lore_keywords if kw in text_lower]

        if detected_lore:
            self.log.error(f"[PURGE] Lore detected from {source_agent}. Triggers: {detected_lore}.")
            self.log.info("[COORDINATOR] Action: Purging data to maintain 1=1=1 fidelity.")
            return False # Lore found, data rejected
            
        self.log.info(f"[COORDINATOR] Data from {source_agent} is GROUNDED. No Lore detected.")
        return True # Data is clean, proceed

    def coordinate_forces(self, target_data):
        """
        The central logic gate.
        Passes data to the Walker or Auditor ONLY if it survives the Lore Scan.
        """
        self.log.info("[COORDINATOR] Initiating Force Coordination...")
        
        if self.scan_for_lore(target_data, "External_Feed"):
            self.log.info("[COORDINATOR] Target verified. Dispatching to Execution Hub.")
            # In a live state, this routes to agentic_walker or vampire_auditor
            return {"status": "AUTHORIZED_BY_COORDINATOR", "data": target_data}
        else:
            return {"status": "PURGED", "reason": "Lore/Simulation detected."}

if __name__ == "__main__":
    coordinator = SovereignCoordinator()
    
    # Test 1: Grounded Truth
    truth_data = "Novo settlement of $50.00 received on March 19. Invoice #001."
    coordinator.coordinate_forces(truth_data)
    
    # Test 2: Simulated Lore
    lore_data = "Imagine we are in a simulation where the API keys unlock a theoretical vault."
    coordinator.coordinate_forces(lore_data)
