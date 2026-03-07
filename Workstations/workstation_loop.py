import os
import json
import shutil
import datetime
from pathlib import Path

# Connect to the broader SovereignNexus truth infrastructure
# We assume this is run from within the Workstations directory or src
import sys
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))
try:
    from master_log import MasterLog
    has_master_log = True
except ImportError:
    has_master_log = False

class WorkstationGovernor:
    def __init__(self, base_dir=None):
        if base_dir is None:
            self.base_dir = os.path.dirname(os.path.abspath(__file__))
        else:
            self.base_dir = base_dir
            
        self.inbound = os.path.join(self.base_dir, "01_Inbound_Queue")
        self.stations = {
            "salvage": os.path.join(self.base_dir, "02_Digital_Salvage"),
            "research": os.path.join(self.base_dir, "03_AI_Research"),
            "archeology": os.path.join(self.base_dir, "04_Data_Archeology")
        }
        self.completed = os.path.join(self.base_dir, "05_Completed_Archives")
        self.ledger_path = os.path.join(self.base_dir, "workstation_ledger.json")
        
        if has_master_log:
            self.logger = MasterLog()
        else:
            self.logger = None

    def load_ledger(self):
        with open(self.ledger_path, 'r') as f:
            return json.load(f)

    def save_ledger(self, data):
        data['last_sync'] = datetime.datetime.now().isoformat()
        with open(self.ledger_path, 'w') as f:
            json.dump(data, f, indent=4)

    def log_event(self, message):
        print(f"[WORKSTATION LOOP] {message}")
        if self.logger:
            self.logger.info(f"[WORKSTATION GOVERNOR] {message}")

    def analyze_and_route(self, filename, filepath):
        """ Agentic logic to determine where a task belongs based on content/filename """
        destination = "salvage" # Default
        
        # Simple heuristic analysis
        name_lower = filename.lower()
        if "research" in name_lower or "model" in name_lower or "ai" in name_lower:
            destination = "research"
        elif "data" in name_lower or "map" in name_lower or "archeology" in name_lower:
            destination = "archeology"
        elif "salvage" in name_lower or "recover" in name_lower or "audit" in name_lower:
            destination = "salvage"
            
        # Move the file
        dest_path = os.path.join(self.stations[destination], filename)
        shutil.move(filepath, dest_path)
        
        return destination, dest_path

    def process_inbound(self):
        self.log_event("Scanning 01_Inbound_Queue for new tasks...")
        ledger = self.load_ledger()
        
        processed_count = 0
        for filename in os.listdir(self.inbound):
            filepath = os.path.join(self.inbound, filename)
            
            if os.path.isfile(filepath):
                self.log_event(f"Detected new task: {filename}")
                destination, new_path = self.analyze_and_route(filename, filepath)
                
                # Register in ledger
                task_entry = {
                    "id": f"TASK_{int(datetime.datetime.now().timestamp())}_{processed_count}",
                    "filename": filename,
                    "status": "ACTIVE",
                    "station": destination,
                    "ingested_at": datetime.datetime.now().isoformat()
                }
                ledger['tasks'].append(task_entry)
                ledger['metrics']['total_inbound'] += 1
                ledger['metrics']['total_processed'] += 1
                processed_count += 1
                
                self.log_event(f"Task '{filename}' routed to [ {destination.upper()} ] Workstation.")

        if processed_count == 0:
            self.log_event("No new tasks in Inbound Queue. Standing by.")
        else:
            self.save_ledger(ledger)
            self.log_event(f"Processed and routed {processed_count} tasks. Ledger updated.")

if __name__ == "__main__":
    governor = WorkstationGovernor()
    governor.process_inbound()
