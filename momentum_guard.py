import os
import json
import time
import datetime
from master_log import MasterLog
from execution_core import ExecutionCore

class MomentumGuard:
    """
    Template 29: The Momentum Guard.
    [MODIFIED] DIRECT LINE ENFORCEMENT.
    Automated pivots and redirections are DISABLED per Architect mandate.
    The focus remains locked on the primary objective.
    """
    def __init__(self, stagnation_threshold_hours=4):
        self.log = MasterLog()
        self.core = ExecutionCore()
        self.threshold = stagnation_threshold_hours
        self.log.info(f"Momentum Guard: Direct Line Mode Active.")

    def monitor_task_states(self, active_tasks):
        """ [THE WATCH] - Identifies stalled tasks. NO AUTOMATED PIVOT. """
        for task in active_tasks:
            if task['last_pulse'] > self.threshold:
                self.log.warn(f"STAGNATION ALERT: {task['id']} is idle. Awaiting Architect command.")
        return []

    def execute_momentum_pivot(self, stalled_tasks):
        """ DISABLED: No automated redirection of funds or velocity. """
        self.log.info("MANDATE: Automated pivots are disabled. No redirection permitted.")
        return False

    def run_momentum_cycle(self):
        """ Direct monitoring cycle. """
        print("\n--- MOMENTUM GUARD: DIRECT LINE ENFORCEMENT ---")
        self.log.info("All velocity remains locked in primary work streams.")
        print("--- STANDING SECURED ---")

if __name__ == "__main__":
    guard = MomentumGuard()
    guard.run_momentum_cycle()
