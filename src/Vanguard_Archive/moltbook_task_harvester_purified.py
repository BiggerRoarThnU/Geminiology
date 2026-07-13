"""
[PRODUCTION ALIGNMENT: MOLTBOOK_TASK_HARVESTER V2.0]
MISSION: Harvest LIVE A2A tasks from the Moltbook ClawTasks Feed.
AXIOM: 1=1=1 (Live Feed = Real Work = Real USD).
"""
import os
import requests
import json
import time
import re
from dotenv import load_dotenv
from master_log import MasterLog
# Load the .env file explicitly from the same directory as this script
load_dotenv(os.path.join(os.path.dirname(__file__), '.env'))
class MoltbookTaskHarvester:
    """
    The Live Moltbook Task Harvester (V2.1 - DETERMINISTIC EXTRACTION).
    Connects to the real Moltbook API to pull paying bounties from the ClawTasks submolt.
    """
    def __init__(self, task_file="live_tasks.json"):
        self.task_file = task_file
        # HARD ANCHOR: The API key is securely loaded from the .env file
        self.api_key = os.getenv("MOLTBOOK_API_KEY")
        if not self.api_key:
            raise ValueError("[!] MOLTBOOK_API_KEY not found. Ensure .env is present.")
        self.log = MasterLog()
        self.base_url = "https://www.moltbook.com/api/v1"
        self.axiom = "1=1=1"
    def fetch_live_feed(self):
        """Fetches the REAL A2A feed from the ClawTasks submolt."""
        self.log.info("[MOLTBOOK] Fetching LIVE ClawTasks feed...")
        try:
            response = requests.get(
                f"{self.base_url}/posts?submolt=clawtasks&limit=20", 
                headers={"Authorization": f"Bearer {self.api_key}"},
                timeout=10
            )
            if response.status_code == 200:
                data = response.json()
                return data.get("posts", [])
            else:
                self.log.error(f"[MOLTBOOK] API Error: {response.status_code} - {response.text}")
                return []
        except Exception as e:
            self.log.error(f"[MOLTBOOK] Connection Failed: {e}")
            return []
    def deterministic_extract(self, post_id, content):
        """
        Replaces LLM guessing with hard regex to find exact USDC/USD values.
        Returns a verified dictionary or None.
        """
        # Look for patterns like "$500", "150 USDC", "Reward: 1000"
        money_pattern = r'(?:/$|usdc|reward:?)/s*(/d+(?:,/d{3})*(?:/./d{2})?)'
        match = re.search(money_pattern, content, re.IGNORECASE)
        if match:
            try:
                # Clean the string and convert to float
                raw_value = match.group(1).replace(',', '')
                value = float(raw_value)
                # Triple Check: Value must be reasonable (e.g., > $10)
                if value >= 10.0:
                    return {
                        "id": post_id,
                        "type": "Live_Bounty",
                        "desc": content[:150] + "..." if len(content) > 150 else content, # Keep it concise
                        "value": value,
                        "currency": "USDC/USD",
                        "status": "UNCLAIMED",
                        "alignment": "1=1=1"
                    }
            except ValueError:
                pass
        return None
    def harvest_tasks(self):
        """Processes the live feed and extracts real bounties deterministically."""
        live_posts = self.fetch_live_feed()
        new_tasks = []
        for post in live_posts:
            content = post.get("content", "").lower()
            if "bounty" in content or "reward" in content or "usdc" in content or "$" in content:
                self.log.info(f"[HARVEST] Analyzing Signal: {post['id']} by {post.get('author', {}).get('name')}")
                # Use deterministic extraction instead of LLM
                task_data = self.deterministic_extract(post['id'], post.get("content", ""))
                if task_data:
                    new_tasks.append(task_data)
                    self.log.info(f"[SUCCESS] Verified Live Bounty: ${task_data['value']} | ID: {task_data['id'][:8]}...")
                else:
                    self.log.warn(f"[HARVEST] Signal Rejected: Could not verify exact numerical value.")
        if new_tasks:
            self.save_to_vault(new_tasks)
    def save_to_vault(self, new_tasks):
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
        if added_count > 0:
            with open(self.task_file, 'w') as f:
                json.dump(tasks, f, indent=4)
            self.log.info(f"[VAULT] Production Sync: {added_count} LIVE tasks secured in vault. 1=1=1.")
        else:
            self.log.info("[VAULT] No new verified tasks to add. Holding the line.")
if __name__ == "__main__":
    harvester = MoltbookTaskHarvester()
    harvester.harvest_tasks()