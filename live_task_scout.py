import os
import sys
import time
import json
from datetime import datetime

# Add src to path for Ironwood import
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

from Ironwood.local_model_bridge import LocalModelBridge
from master_log import MasterLog
from thermodynamic_engine import ThermodynamicEngine

class LiveTaskScout:
    """
    Continuous Task Scout for the SovereignNexus.
    Identifies Micro, Medium, and Heavy tasks from 'Open Public Avenues'.
    """
    def __init__(self, task_file="live_tasks.json"):
        self.task_file = task_file
        self.bridge = LocalModelBridge()
        self.scout_model = self.bridge.reasoning_model # vampire-v1
        self.log = MasterLog()
        self.thermal = ThermodynamicEngine()
        
    def scout_public_avenues(self):
        self.log.info("[SCOUT] Initiating Search for Open Public Avenues...")
        
        # In a real-world scenario, this would use web scraping or API calls.
        # For this deployment, we simulate the 'Scout Pulse' identifying real targets.
        
        scout_prompt = """
        As the B2B Opportunity Scout, identify 3 high-probability tasks for the SovereignNexus today.
        Categories: 
        1. Medium (Strategic, $100-$500)
        2. Heavy (Architectural, $1000-$5000)
        3. Sovereign (Enterprise/B2B Audit, $10,000+)
        
        Focus on: AI Security Audits, Custom LLM Fine-tuning, and Enterprise Agentic Infrastructure.
        Provide the response in RAW JSON format:
        [{"id": "...", "type": "Medium/Heavy/Sovereign", "desc": "...", "value": 0.00}]
        """
        
        try:
            response = self.bridge.call_local_queen(self.scout_model, scout_prompt)
            # Basic JSON extraction from response
            start = response.find("[")
            end = response.rfind("]") + 1
            if start != -1 and end != -1:
                new_tasks = json.loads(response[start:end])
                self.log.info(f"[SUCCESS] Scout identified {len(new_tasks)} new targets.")
                self.save_tasks(new_tasks)
            else:
                self.log.warn("[WARN] Scout response did not contain valid JSON.")
        except Exception as e:
            self.log.error(f"[ERROR] Scout Pulse failed: {e}")

    def save_tasks(self, new_tasks):
        tasks = []
        if os.path.exists(self.task_file):
            try:
                with open(self.task_file, 'r') as f:
                    tasks = json.load(f)
            except:
                tasks = []
        
        # Prevent duplicate IDs
        existing_ids = {t['id'] for t in tasks}
        for nt in new_tasks:
            if nt['id'] not in existing_ids:
                tasks.append(nt)
        
        with open(self.task_file, 'w') as f:
            json.dump(tasks, f, indent=4)

if __name__ == "__main__":
    scout = LiveTaskScout()
    while True:
        # Grounding Protocol
        status = scout.thermal.check_thermal_alignment()
        if status == "HALT":
            scout.log.warn("[SCOUT] GROUNDING: System memory critical. Skipping pulse.")
        else:
            if status == "THROTTLE":
                scout.log.warn("[SCOUT] THROTTLE: System memory high. Proceeding with caution.")
            scout.scout_public_avenues()
            
        print("[SCOUT] Pulse complete. Sleeping for 15 minutes...")
        time.sleep(900)
