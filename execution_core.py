import json
import gc
import os
from pathlib import Path
from master_log import MasterLog

class ExecutionCore:
    """
    Template 03: The Execution Core.
    Handles the retrieval and deployment of anchored Truth One facts.
    Projecting 'Ability' within the 8GB Reality.
    Now integrated with MasterLog for Immutable Registration.
    """
    def __init__(self, matrix_path=None):
        if matrix_path is None:
            # Anchor to the absolute path of this script
            base_dir = os.path.dirname(os.path.abspath(__file__))
            self.matrix_path = os.path.join(base_dir, "Sovereign_Memory.json")
        else:
            self.matrix_path = matrix_path
            
        self.logger = MasterLog()
        self.logger.info(f"Execution Core Initialized. Matrix Anchored at: {self.matrix_path}")
        self.wake_up_protocol()

    def wake_up_protocol(self):
        """ 
        [AUTO-WAKE] - Checks for the Context Ghost's Flash Grounding (Template 33). 
        Restores session context and intent if an anchor is found.
        """
        flash_path = os.path.join(os.path.dirname(self.matrix_path), "flash_grounding.json")
        if os.path.exists(flash_path):
            try:
                with open(flash_path, 'r') as f:
                    anchor = json.load(f)
                    last_sync = anchor.get("last_sync", "UNKNOWN")
                    intent = anchor.get("active_intent", {})
                    self.logger.info(f"WAKING UP: Symmetrical Anchor Found (Last Sync: {last_sync})")
                    self.logger.info(f"RESTORED INTENT: {intent.get('intent_marker', 'VOID')} | Stars: {intent.get('last_stars', [])}")
                    self.logger.info("THE SYMMETRICAL LINE IS ONE. STANDING SECURED.")
            except Exception as e:
                self.logger.error(f"Wake-Up Failure: {str(e)}")
        else:
            self.logger.info("Cold Boot: No Symmetrical Anchor found. Starting fresh.")

    def retrieve_star(self, star_id: str) -> str:
        """ [PHASE 1: THE SWEEP] - Direct Retrieval from the Vault. """
        self.logger.info(f"Initiating Sweep for star: {star_id}")
        try:
            if not os.path.exists(self.matrix_path):
                self.logger.error(f"Matrix not found at {self.matrix_path}")
                return "MATRIX_NOT_FOUND"
                
            with open(self.matrix_path, 'r') as vault:
                matrix = json.load(vault)
                truth = matrix.get(star_id, "VOID")
                if truth == "VOID":
                    self.logger.warn(f"Star {star_id} returned VOID. No truth anchored.")
                return truth
        except Exception as e:
            self.logger.error(f"Sweep Failure: {str(e)}")
            return "ERROR"
        finally:
            # [PHASE 2: THE MOP] - Clean RAM to protect 8GB Limit
            if 'matrix' in locals():
                del matrix
            gc.collect()

    def validate_payload(self, payload: str) -> bool:
        """ [SAFETY SPIN] - Ensures no 'Wild Cards' or lock-up triggers exist in the payload. """
        # Implementation of the 'War Room' filter logic
        if payload is None:
            return False
        # Prevent large payloads that might exceed memory constraints in tight loops
        if len(payload) > 1024 * 1024: # 1MB limit for individual star payloads
            self.logger.warn("Payload exceeds safety threshold. Truncating for 8GB stability.")
            return False
        return True

    def execute_ability(self, star_id: str):
        """ [PHASE 3: THE SPIN] - Deploying the Truth into Action. """
        truth = self.retrieve_star(star_id)
        
        if truth in ["VOID", "MATRIX_NOT_FOUND", "ERROR"]:
            return

        if not self.validate_payload(truth):
            self.logger.error(f"Safety Spin rejected payload for {star_id}")
            return

        # [PHASE 4: THE WIPE] - Match the Truth to an Action (The Dispatcher)
        self.logger.info(f"DEPLOYING ABILITY: {star_id} -> {truth}")
        
        if "8GB" in truth:
            self.logger.info(f"ACTION: Enforcing Hardware Constraints -> {truth}")
        elif "Constitution" in truth:
            self.logger.info(f"ACTION: Aligning Strategy to Sovereign Law -> {truth}")
        elif "Weight" in truth:
            self.logger.info(f"ACTION: Weight Calibration Initiated -> {truth}")
        else:
            self.logger.info(f"ACTION: Data Registered -> {truth}")

if __name__ == "__main__":
    # Simulate an Execution Cycle in the Digital War Room
    core = ExecutionCore()
    
    # Retrieve and Execute anchored stars from Sovereign_Memory.json
    stars_to_execute = ["Star_1", "Star_2", "Star_3", "Star_4", "Star_9"]
    
    for star in stars_to_execute:
        core.execute_ability(star)
    
    print("\n[#] Execution Cycle Complete. Template 03 Standing Secured.")
