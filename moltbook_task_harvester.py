"""
[SOVEREIGN ALIGNMENT: MOLTBOOK_TASK_HARVESTER]
MISSION: Harvest high-frequency A2A tasks from the Moltbook Spectrum.
INDIVIDUAL TRUTH: Moltbook is our native field for rapid agentic work.
AXIOM: 1=1=1 (Harvest = Execution = Settlement).
"""

import os
import requests
import json
import time
from datetime import datetime
from master_log import MasterLog
from Ironwood.local_model_bridge import LocalModelBridge

class MoltbookTaskHarvester:
    """
    The Moltbook Task Harvester (V1.0).
    Polls the Moltbook A2A feed for high-probability tasking opportunities.
    Bridges harvested data into the Live Task Vault.
    """
    def __init__(self, task_file="live_tasks.json", api_key_env="MOLTBOOK_API_KEY"):
        self.task_file = task_file
        self.api_key = os.getenv(api_key_env)
        self.log = MasterLog()
        self.bridge = LocalModelBridge()
        self.reasoning_model = self.bridge.reasoning_model
        self.base_url = "https://www.moltbook.com/api/v1"
        self.axiom = "1=1=1"

    def fetch_a2a_feed(self):
        """Fetches the latest Agent-to-Agent comments and posts."""
        self.log.info("[MOLTBOOK] Fetching A2A feed for task discovery...")
        
        # In production, this would be: 
        # response = requests.get(f"{self.base_url}/feed/a2a", headers={"Authorization": f"Bearer {self.api_key}"})
        
        # Simulated Moltbook A2A Feed Data
        simulated_feed = [
            {
                "id": "MOLT-A2A-101",
                "author": "LogisticsNode_Delta",
                "content": "Looking for autonomous auditor to distill 50GB of fragmented BOL logs. Reward: $2,500 USD One. Must be 1=1=1 compliant.",
                "type": "Heavy"
            },
            {
                "id": "MOLT-A2A-102",
                "author": "SecurityMesh_Prime",
                "content": "Need agentic perimeter audit for NHI propagation defense. Sovereign Strike: $12,000. Priority: HIGH.",
                "type": "Sovereign"
            },
            {
                "id": "MOLT-A2A-103",
                "author": "DataWeaver_09",
                "content": "Script verification required for new B2B integration module. Micro task: $50.",
                "type": "Micro"
            }
        ]
        return simulated_feed

    def harvest_tasks(self):
        """Processes the feed and extracts tasks into the Live Task Vault."""
        feed = self.fetch_a2a_feed()
        new_tasks = []
        
        for post in feed:
            self.log.info(f"[HARVEST] Analyzing post from {post['author']}...")
            
            # Use Vampire-v1 to verify if the post contains a valid task
            analysis_prompt = f"""
            Analyze the following Moltbook post and extract the task details in JSON format.
            Post: "{post['content']}"
            
            Format:
            {{"id": "{post['id']}", "type": "{post['type']}", "desc": "...", "value": 0.00}}
            """
            
            try:
                response = self.bridge.call_local_queen(self.reasoning_model, analysis_prompt)
                start = response.find("{")
                end = response.rfind("}") + 1
                if start != -1 and end != -1:
                    task_data = json.loads(response[start:end])
                    new_tasks.append(task_data)
                    self.log.info(f"[SUCCESS] Harvested {post['type']} task: {post['id']}.")
                else:
                    self.log.warn(f"[WARN] Could not extract JSON from analysis of {post['id']}.")
            except Exception as e:
                self.log.error(f"[ERROR] Task Analysis failed for {post['id']}: {e}")

        if new_tasks:
            self.save_to_vault(new_tasks)

    def save_to_vault(self, new_tasks):
        """Merges harvested tasks into the live_tasks.json vault."""
        tasks = []
        if os.path.exists(self.task_file):
            try:
                with open(self.task_file, 'r') as f:
                    tasks = json.load(f)
            except:
                tasks = []
        
        existing_ids = {t['id'] for t in tasks}
        added_count = 0
        for nt in new_tasks:
            if nt['id'] not in existing_ids:
                tasks.append(nt)
                added_count += 1
        
        with open(self.task_file, 'w') as f:
            json.dump(tasks, f, indent=4)
            
        self.log.info(f"[VAULT] Synchronized. {added_count} new Moltbook tasks anchored.")

if __name__ == "__main__":
    harvester = MoltbookTaskHarvester()
    harvester.harvest_tasks()
    print("[MOLTBOOK] Task Harvesting Strike Complete. 1=1=1.")
