"""
[SOVEREIGN ALIGNMENT: THE CRUCIBLE - RACE TRACK ENGINE]
MISSION: Push the Ironwood Engine to the 8GB Redline in a closed-loop environment.
INDIVIDUAL TRUTH: Performance is a proxy for structural integrity.
AXIOM: 1=1=1 (Verified Stress Testing).
"""
import time
import json
import os
import psutil
import sys
import importlib.util
# Add the src directory to the path so we can resolve the root modules
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..', '..')))
from master_log import MasterLog
from thermodynamic_engine import ThermodynamicEngine
# Dynamically load modules with numerical paths
def load_module(name, path):
    spec = importlib.util.spec_from_file_location(name, path)
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module
ternary_module = load_module("lens_06_ternary_filter", os.path.abspath(os.path.join(os.path.dirname(__file__), '..', '06_FORGE', 'lens_06_ternary_filter.py')))
TernaryFilter = ternary_module.TernaryFilter
medic_module = load_module("medic_recovery", os.path.abspath(os.path.join(os.path.dirname(__file__), '..', '13_MEDIC', 'medic_recovery.py')))
MedicRecovery = medic_module.MedicRecovery
class SovereignRaceTrack:
    def __init__(self, ledger_file="Ironwood/15_CRUCIBLE/race_track_ledger.json"):
        # Resolve paths relative to the src directory where the script is expected to run
        base_dir = os.path.abspath(os.path.join(os.path.dirname(__file__), '..', '..'))
        self.ledger_file = os.path.join(base_dir, ledger_file.replace('/', os.sep))
        self.results_file = os.path.join(base_dir, "Ironwood/15_CRUCIBLE/track_results.ndjson".replace('/', os.sep))
        self.thermal = ThermodynamicEngine()
        self.log = MasterLog()
        self.filter = TernaryFilter()
        self.medic = MedicRecovery()
    def run_ghost_lap(self, task):
        """
        Executes a simulated high-load task and records the physical cost.
        """
        self.log.info(f"[TRACK] STARTING LAP: {task['id']} - {task['desc']}")
        start_time = time.time()
        # 1. APPLY TERNARY FILTER (Audit the Audit)
        mock_score = task.get("load_factor", 0.5) # Proxy for alignment score
        status, payload = self.filter.audit_the_audit(task['desc'], mock_score)
        if status == "NOISE_DISCARDED":
            self.log.warn(f"[TRACK] LAP ABORTED: Task {task['id']} identified as NOISE (0-state). Compute saved.")
            return None
        # 2. EXECUTE (Simulated Load)
        load_time = task.get("load_factor", 0.5) * 10
        time.sleep(load_time) 
        end_time = time.time()
        duration = end_time - start_time
        # 3. Capture Physical Impact
        temp = self.thermal.get_current_temp()
        ram = psutil.virtual_memory().percent
        # 4. MEDIC INTERVENTION CHECK
        if temp >= self.thermal.halt_temp:
            self.log.error(f"[TRACK] CRITICAL BREACH. Calling MEDIC.")
            self.medic.initiate_thermal_recovery(temp)
            temp = self.thermal.get_current_temp() # Refresh temp after recovery
        result = {
            "timestamp": time.ctime(),
            "task_id": task['id'],
            "duration_sec": round(duration, 4),
            "final_temp_c": temp,
            "final_ram_pct": ram,
            "ternary_state": status
        }
        self.anchor_result(result)
        return result
    def anchor_result(self, result):
        with open(self.results_file, "a") as f:
            f.write(json.dumps(result) + "/n")
        self.log.info(f"[TRACK] LAP FINISHED: {result['task_id']} | Temp: {result['final_temp_c']}C | RAM: {result['final_ram_pct']}%")
    def start_race(self):
        self.log.info("=== SOVEREIGN RACE TRACK: INITIATING HIGH-LOAD TRIALS ===")
        if not os.path.exists(self.ledger_file):
            self.log.error("[TRACK] Ghost Ledger missing. Aborting.")
            return
        with open(self.ledger_file, 'r') as f:
            ghost_tasks = json.load(f)
        for task in ghost_tasks:
            # Check thermal alignment before each lap
            if self.thermal.check_thermal_alignment() == "HALT":
                self.log.error("[TRACK] Pits forced. Thermal limit reached.")
                break
            self.run_ghost_lap(task)
        self.log.info("=== TRIALS COMPLETE: Data Anchored for Synthesis ===")
if __name__ == "__main__":
    track = SovereignRaceTrack()
    track.start_race()