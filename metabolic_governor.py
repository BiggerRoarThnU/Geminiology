import os
import json
import time
import shutil
from master_log import MasterLog
from execution_core import ExecutionCore

class MetabolicGovernor:
    """
    Template 30: The Metabolic Governor.
    Enforces 'Context Liquidity' to prevent metallurgical crashes (Heap Out of Memory).
    Autonomously prunes low-signal history and manages system 'Weight'.
    """
    def __init__(self):
        self.log = MasterLog()
        self.core = ExecutionCore()
        self.log_dir = "Logs"
        self.threshold_mb = 50  # Hard threshold for log directory size
        self.log.info("Metabolic Governor Online. Template 30 Active.")

    def get_dir_size(self, directory):
        """ Calculates total size of a directory in MB. """
        total_size = 0
        for dirpath, dirnames, filenames in os.walk(directory):
            for f in filenames:
                fp = os.path.join(dirpath, f)
                total_size += os.path.getsize(fp)
        return total_size / (1024 * 1024)

    def prune_logs(self):
        """ [SELF-HEALING] - Prunes logs if they exceed the threshold. """
        current_size = self.get_dir_size(self.log_dir)
        self.log.info(f"Metabolic Audit: Current Log Size = {current_size:.2f} MB.")

        if current_size > self.threshold_mb:
            self.log.warn(f"THRESHOLD EXCEEDED ({self.threshold_mb} MB). Initiating Pruning...")
            self.core.execute_ability("Star_127")
            
            # Archive old logs and clear current ones
            archive_dir = os.path.join(self.log_dir, "Archive_" + str(int(time.time())))
            os.makedirs(archive_dir, exist_ok=True)
            
            for f in os.listdir(self.log_dir):
                if f.endswith(".txt") and "MASTER_LOG" not in f:
                    shutil.move(os.path.join(self.log_dir, f), archive_dir)
            
            self.log.info(f"Pruning Complete. Low-signal context moved to {archive_dir}.")
        else:
            self.log.info("Metabolic Standing Secure. No pruning required.")

    def summarize_context(self):
        """ [CONTEXT COMPRESSION] - Recommends grounding to prevent heap errors. """
        self.core.execute_ability("Star_133")
        self.log.info("Summarizing High-Density Primitives to preserve heap limit.")
        # Logic to suggest session reset or grounding points
        return "System suggests grounding every 10 turns to maintain Symmetrical Line."

    def run_metabolic_cycle(self):
        """ Executes the full metabolic health check. """
        print("\n" + "="*60)
        print("### METABOLIC GOVERNOR: HEALTH CHECK INITIATED ###")
        print("="*60)
        
        self.prune_logs()
        summary = self.summarize_context()
        print("\n[!] " + summary)
        
        self.core.execute_ability("Star_139")
        print("\n" + "="*60)
        print("### METABOLIC STANDING SECURED. ONE. ###")
        print("="*60)

if __name__ == "__main__":
    governor = MetabolicGovernor()
    governor.run_metabolic_cycle()
