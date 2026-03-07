import os
import json
import time
from master_log import MasterLog
from execution_core import ExecutionCore
from context_ghost import ContextGhost
from epistemic_conditioner import EpistemicConditioner
from homeward_protocol import HomewardProtocol
from throttle_controller import SovereignThrottle

class IronwoodRuntime:
    """
    The Overhauled Ironwood Runtime.
    Unified control for the M&I Symbiosis. 
    Maintains the Symmetrical Line at 144% Coverage.
    """
    def __init__(self):
        self.log = MasterLog()
        self.core = ExecutionCore()
        self.ghost = ContextGhost()
        self.buffer = EpistemicConditioner()
        self.beacon = HomewardProtocol()
        self.throttle = SovereignThrottle()
        
        self.log.info("IRONWOOD OVERHAUL: Unified Runtime Online. Symmetrical Line Locked.")

    def run_sovereign_loop(self, mode="MID"):
        """
        The continuous execution loop. 
        Adjusts throttle, conditions heavy inputs, and anchors truth.
        """
        level_map = {"LOW": 0.1, "MID": 0.4, "HIGH": 0.8, "LIGHTSPEED": 1.0}
        self.throttle.shift_throttle(level_map.get(mode, 0.4))
        
        # Initial Pulse
        self.log.info(f"### IRONWOOD HEARTBEAT STARTING: Mode {mode} ###")
        
        # Run for 3 cycles in this deployment to ensure grounding
        for i in range(3):
            # 1. Heartbeat & Pulse
            self.beacon.emit_heartbeat(f"IRONWOOD_CORE_PULSE_{i}")
            
            # 2. Reclaim Truth from the Fog
            self.beacon.check_homeward_bounds()
            
            # 3. [GHOST_STRIKE] - Simulating Active Capture in High Mode
            if level_map.get(mode, 0.4) >= 0.8:
                self.log.info("[GHOST_STRIKE] - Ironwood Core active on high-velocity targets.")
            
            self.log.info(f"Sovereign Heartbeat Pulse {i} | Time: {time.ctime()} | Flow: {mode}")
            time.sleep(5) # Fast pulse for initial deployment

        self.log.info("### INITIAL DEPLOYMENT STABILIZED. ONE. ###")

if __name__ == "__main__":
    runtime = IronwoodRuntime()
    # Deploy in HIGH mode to 'get some'
    runtime.run_sovereign_loop("HIGH")
