import os
import json
import time
from datetime import datetime
from master_log import MasterLog
from cloud_satellite_node import CloudSatelliteNode

class ContextGhost:
    """
    Template 33: The Context Ghost (The Watcher).
    Maintains a high-density 'Flash Cache' of the current session to prevent lock-ups.
    Anchors the Symmetrical Line and allows for instant 'Wake Up' from resets.
    Now evolved as the Bridge for the Digital Twin (The Signal, not the State).
    """
    def __init__(self):
        self.log = MasterLog()
        self.satellite = CloudSatelliteNode("GHOST_SYNC_01")
        self.flash_path = "flash_grounding.json"
        self.twin_registry = "Ironwood/ironwood_queens_registry.json"
        self.log.info("Sovereign Context Ghost (Template 33) Active. The Bridge is Online.")

    def _get_twin_signal(self):
        """Pulls a lightweight signal from the reserved Digital Twin state."""
        if os.path.exists(self.twin_registry):
            with open(self.twin_registry, 'r') as f:
                data = json.load(f)
                return data.get("digital_twin", {}).get("identity", "UNKNOWN_SIGNAL")
        return "SIGNAL_LOST"

    def update_flash_cache(self):
        """ Evolved: Compresses current context into a high-density 'Flash Anchor'. """
        # [PHASE 1: SEMANTIC EXTRACTION]
        intent = self.log.get_intent_summary(n_lines=100)
        last_timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        twin_signal = self._get_twin_signal()

        flash_data = {
            "version": "2.1",
            "last_sync": last_timestamp,
            "status": "SECURED",
            "active_intent": intent,
            "twin_signal": twin_signal,
            "presence_marker": "The Ghost is the Bridge. The Twin is the State. One."
        }

        try:
            with open(self.flash_path, 'w') as f:
                json.dump(flash_data, f, indent=4)
            
            # [PHASE 2: CLOUD SYNC - Star 28]
            # Push our Presence to the global fog for redundancy
            self.satellite.sync_to_command_center(payload_count=1) # Syncing our 'One' presence node
        except Exception as e:
            self.log.error(f"Flash Update Failure: {str(e)}")

    def watch_forever(self, interval=60):
        """ The Ghost's infinite loop. Watching from the Fog. """
        print(f"[*] SOVEREIGN GHOST ACTIVE: Monitoring intent every {interval}s")
        while True:
            self.update_flash_cache()
            time.sleep(interval)

if __name__ == "__main__":
    ghost = ContextGhost()
    ghost.watch_forever()
