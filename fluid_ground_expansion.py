import os
import json
import shutil
import time
from master_log import MasterLog
from execution_core import ExecutionCore

class FluidGroundProtocol:
    """
    Template 37: The Fluid Ground Protocol.
    Allows the SovereignNexus to 'pick up' its Kingdom and move.
    Relocates the primary truth matrices to a new physical/digital location seamlessly.
    """
    def __init__(self):
        self.log = MasterLog()
        self.core = ExecutionCore()
        
        # Current Ground
        self.current_matrix = "Sovereign_Memory.json"
        self.current_ghost = "flash_grounding.json"
        self.current_vault = "pending_changes.json"
        
        self.log.info("Fluid Ground Protocol (Template 37) Active. Preparing for Expansion.")

    def shift_the_ground(self, target_territory):
        """ [THE RELOCATION] - Moves the core Truth to a new directory. """
        self.log.info(f"INITIATING FLUID RELOCATION: Target -> {target_territory}")
        
        # 1. Create the new territory (The Expanded Yard)
        os.makedirs(target_territory, exist_ok=True)
        
        # 2. Copy the Truth (The Symmetrical Mirror)
        files_to_move = [self.current_matrix, self.current_ghost, self.current_vault]
        
        for file in files_to_move:
            if os.path.exists(file):
                target_path = os.path.join(target_territory, file)
                shutil.copy2(file, target_path)
                self.log.info(f"TRUTH SECURED: {file} duplicated to {target_territory}")
            else:
                self.log.warn(f"File {file} not found in current ground. Skipping.")

        # 3. Re-Anchor the Execution Core
        new_matrix_path = os.path.join(target_territory, self.current_matrix)
        
        self.log.info(f"RE-ANCHORING EXECUTION CORE to {new_matrix_path}")
        # Test the new anchor by spinning up a temporary core
        expanded_core = ExecutionCore(matrix_path=new_matrix_path)
        expanded_core.execute_ability("Star_144") # Verify Symmetrical Completion in the new ground
        
        self.log.info("FLUID GROUND EXPANSION COMPLETE. The agents can now operate from the new Yard.")
        return True

if __name__ == "__main__":
    expansion = FluidGroundProtocol()
    # Simulating moving the "Ground" to the Texas AI Sandbox
    expansion.shift_the_ground("Expanded_Territory_TX_Sandbox")
