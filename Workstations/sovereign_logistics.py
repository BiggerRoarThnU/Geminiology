import os
import json
import datetime
import shutil

# Connect to the broader SovereignNexus truth infrastructure
import sys
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))
try:
    from master_log import MasterLog
    has_master_log = True
except ImportError:
    has_master_log = False

try:
    # Handle both direct and package-level imports
    try:
        from workstation_loop import WorkstationGovernor
    except ImportError:
        from .workstation_loop import WorkstationGovernor
    has_governor = True
except (ImportError, ValueError):
    has_governor = False

class SovereignLogistics:
    def __init__(self, base_dir=None):
        if base_dir is None:
            # We assume we are in src or Workstations
            self.base_dir = os.path.dirname(os.path.abspath(__file__))
            if "Workstations" not in self.base_dir:
                self.base_dir = os.path.join(self.base_dir, "Workstations")
        else:
            self.base_dir = base_dir
            
        self.ledger_path = os.path.join(self.base_dir, "logistics_ledger.json")
        
        if has_governor:
            self.governor = WorkstationGovernor(self.base_dir)
        else:
            self.governor = None
        
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
        print(f"[LOGISTICS ENGINE] {message}")
        if self.logger:
            self.logger.info(f"[SOVEREIGN LOGISTICS] {message}")

    def initiate_handshake(self, client_name, service_type, projected_revenue=0.0):
        """ START: Registers the initial handshake and creates the project folder. """
        ledger = self.load_ledger()
        
        project_id = f"NEXUS_{int(datetime.datetime.now().timestamp())}"
        project_entry = {
            "id": project_id,
            "client": client_name,
            "service": service_type,
            "status": "HANDSHAKE",
            "revenue": projected_revenue,
            "payment_verified": False,
            "created_at": datetime.datetime.now().isoformat(),
            "completed_at": None,
            "handshake_verified": True
        }
        
        ledger['projects'].append(project_entry)
        ledger['active_handshakes'] += 1
        self.save_ledger(ledger)
        
        self.log_event(f"New Handshake Initiated: {client_name} for [ {service_type.upper()} ]. Project ID: {project_id}")
        
        # Create a trigger file in the Inbound Queue
        trigger_filename = f"{project_id}_{client_name}_START.txt"
        trigger_path = os.path.join(self.base_dir, "01_Inbound_Queue", trigger_filename)
        with open(trigger_path, 'w') as f:
            f.write(f"Project: {client_name}\nService: {service_type}\nID: {project_id}\nStatus: START")
            
        # Run the Governor to route the new project
        self.governor.process_inbound()
        
        return project_id

    def verify_and_complete(self, project_id, actual_revenue):
        """ END: Confirms payment, updates the ledger, and archives the project. """
        ledger = self.load_ledger()
        
        for project in ledger['projects']:
            if project['id'] == project_id:
                project['status'] = "COMPLETED"
                project['payment_verified'] = True
                project['revenue'] = actual_revenue
                project['completed_at'] = datetime.datetime.now().isoformat()
                
                ledger['total_revenue'] += actual_revenue
                ledger['active_handshakes'] -= 1
                ledger['completed_cycles'] += 1
                
                self.save_ledger(ledger)
                self.log_event(f"Project {project_id} [ {project['client']} ] SEVERED AND ARCHIVED. Revenue: ${actual_revenue}")
                
                # Move from active station to Completed Archives
                # (Simple heuristic: find file in station and move)
                self._archive_files(project_id)
                return True
        
        self.log_event(f"ERROR: Project ID {project_id} not found in ledger.")
        return False

    def _archive_files(self, project_id):
        stations = ["02_Digital_Salvage", "03_AI_Research", "04_Data_Archeology"]
        archive_dir = os.path.join(self.base_dir, "05_Completed_Archives")
        
        for station in stations:
            station_path = os.path.join(self.base_dir, station)
            for filename in os.listdir(station_path):
                if project_id in filename:
                    shutil.move(os.path.join(station_path, filename), os.path.join(archive_dir, filename))
                    self.log_event(f"File {filename} moved to [ COMPLETED ARCHIVES ]. Loop Closed.")

if __name__ == "__main__":
    # Test: Initiate a new handshake for an Agentic Workflow project
    engine = SovereignLogistics()
    p_id = engine.initiate_handshake("A2 Global Shipping", "Agentic_Workflow", 500.0)
    
    # Simulate completion
    time_delay = 1 # Simulation
    engine.verify_and_complete(p_id, 500.0)
