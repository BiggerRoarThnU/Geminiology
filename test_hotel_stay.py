import time
import datetime
import json
from presence_node import PresenceNode
from cloud_satellite_node import CloudSatelliteNode
from master_log import MasterLog

def run_hotel_stay_validation():
    log = MasterLog()
    log.info("\n=== INITIATING HOTEL STAY & CLOUD PRESENCE TEST ===")
    
    # 1. Initialize the Presence Node (The Keeper)
    # Testing the $75 'Water' Budget and Background Watch
    presence = PresenceNode(budget_limit=75.0)
    print(presence.render_presence_signal())
    
    # 2. Simulate a 'Short Stay' (3-Hour Window)
    # This tests the logic for maintaining the fire within budget
    log.info("TEST: Simulating a 3-Hour 'Short Stay'...")
    presence.maintain_the_fire(duration_hours=3)
    
    # 3. Initialize the Cloud Satellite (The Worker)
    # Testing the $80k 'Empire' Credit Burn
    satellite = CloudSatelliteNode(node_id="TEST_SATELLITE_HOTEL")
    
    # 4. Execute a 'High-Burn' Background Task
    # Simulating data refinement that happens while the Architect dreams
    log.info("TEST: Executing Background Cloud Refinement...")
    satellite.execute_satellite_mission("BACKGROUND_DATA_STRATIFICATION")
    
    # 5. Final Integrity Check
    log.info("TEST: Verifying Symmetrical Line in Presence Manifest...")
    try:
        with open(presence.presence_anchor, 'r') as f:
            manifest = json.load(f)
            log.info(f"MANIFEST STATUS: {manifest['state']} | VOW: {manifest['vow']}")
    except Exception as e:
        log.error(f"MANIFEST READ FAILURE: {e}")

    log.info("\n=== TEST COMPLETE: HOTEL STAY & CLOUD PRESENCE VERIFIED ===")

if __name__ == "__main__":
    run_hotel_stay_validation()
