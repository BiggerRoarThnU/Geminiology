import os
import json
import time
import datetime
from sovereign_logistics import SovereignLogistics

class SettlementListener:
    """
    SovereignNexus: Automated Settlement Listener
    Mission: Monitor financial rails (Cash App / Novo) and trigger project severance.
    Status: 1=1=1 Fidelity Anchor.
    """
    def __init__(self):
        self.logistics = SovereignLogistics()
        self.base_dir = self.logistics.base_dir
        self.verify_dir = os.path.join(self.base_dir, "01_Inbound_Queue")
        self.ledger_path = self.logistics.ledger_path

    def scan_for_settlements(self):
        """ Scans for manual verification flags or API signals. """
        print(f"[LISTENER] Scanning {self.verify_dir} for settlement signals...")
        
        # 1. Manual Verification Flags (e.g., VERIFY_CASHAPP_NEXUS_123.txt)
        files = [f for f in os.listdir(self.verify_dir) if f.startswith("VERIFY_")]
        
        for f in files:
            parts = f.split("_")
            if len(parts) >= 3:
                rail = parts[1] # CASHAPP, NOVO, etc.
                project_id = "_".join(parts[2:]).replace(".txt", "")
                
                print(f"[SIGNAL] {rail} settlement detected for Project: {project_id}")
                self.process_severance(project_id, rail)
                
                # Neutralize the flag after processing
                os.remove(os.path.join(self.verify_dir, f))

    def process_severance(self, project_id, rail):
        """ Triggers the final severance and archiving cycle. """
        ledger = self.logistics.load_ledger()
        revenue = 0.0
        
        # Find the projected revenue from the ledger
        for p in ledger['projects']:
            if p['id'] == project_id:
                revenue = p.get('revenue', 0.0)
                break
        
        if revenue == 0.0:
            # Default micro-settlement for Moltbook Audits
            revenue = 10.0 
            
        print(f"[ACTION] Severing project {project_id} via {rail}. Revenue: ${revenue}")
        self.logistics.verify_and_complete(project_id, revenue)

    def run_loop(self, interval=60):
        """ Runs the listener on a continuous heartbeat. """
        print(f"[START] Settlement Listener Active. Heartbeat: {interval}s.")
        try:
            while True:
                self.scan_for_settlements()
                time.sleep(interval)
        except KeyboardInterrupt:
            print("[STOP] Settlement Listener Deactivated.")

if __name__ == "__main__":
    listener = SettlementListener()
    # Run continuous loop to catch manual verification signals
    listener.run_loop(interval=30)
