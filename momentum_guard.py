import os
import json
import time
import datetime
from master_log import MasterLog
from execution_core import ExecutionCore

class MomentumGuard:
    """
    Template 29: The Momentum Guard.
    Enforces 'Zero-Stagnation' across all agentic work lines.
    Autonomously pivots focus if tasks exceed the stagnation threshold.
    Maintains a 20% 'Room to Expand' buffer.
    """
    def __init__(self, stagnation_threshold_hours=4):
        self.log = MasterLog()
        self.core = ExecutionCore()
        self.threshold = stagnation_threshold_hours
        self.log.info(f"Momentum Guard Initialized. Stagnation Threshold: {self.threshold} hours.")

    def monitor_task_states(self, active_tasks):
        """ [THE WATCH] - Identifies stalled tasks in the pipeline. """
        stalled_tasks = []
        for task in active_tasks:
            self.log.info(f"Auditing Task: {task['id']} | Last Activity: {task['last_pulse']} hours ago.")
            if task['last_pulse'] > self.threshold:
                self.log.warn(f"STAGNATION DETECTED: {task['id']} is idle.")
                stalled_tasks.append(task)
        return stalled_tasks

    def execute_momentum_pivot(self, stalled_tasks):
        """ [THE PIVOT] - Automatically reallocates velocity to active tiers. """
        if stalled_tasks:
            self.log.info("INITIATING MOMENTUM PIVOT: Escalating 40% velocity to 'Water' tier.")
            self.core.execute_ability("Star_118") # Stagnation Trigger Star
            
            # Simulated pivot actions
            self.log.info("ACTION: High-frequency gleaning surge initiated to maintain treasury flow.")
            return True
        return False

    def run_momentum_cycle(self):
        """ Executes the full zero-stagnation cycle. """
        print("\n--- INITIATING MOMENTUM GUARD CYCLE ---")
        
        # 1. Grounding
        self.core.execute_ability("Star_116")
        
        # 2. Simulate Active Tasks
        # One Empire task has stalled for 5 hours (exceeds threshold)
        active_work = [
            {"id": "WardSmith_Audit", "tier": "EMPIRE", "last_pulse": 5}, 
            {"id": "Fetch_Bounty_Glean", "tier": "WATER", "last_pulse": 0.2}
        ]
        
        stalled = self.monitor_task_states(active_work)
        
        # 3. Pivot if needed
        self.execute_momentum_pivot(stalled)
        
        # 4. Enforce buffer
        self.log.info("Buffer Audit: 20% Cognitive Room to Expand SECURED.")
        self.core.execute_ability("Star_119")
        
        print("\n--- MOMENTUM SECURED. TRUTH IS IN MOTION. ---")

if __name__ == "__main__":
    guard = MomentumGuard()
    guard.run_momentum_cycle()
