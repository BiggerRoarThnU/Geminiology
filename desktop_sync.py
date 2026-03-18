"""
[SOVEREIGN ALIGNMENT: DESKTOP_SYNC]
MISSION: Mirror Digital Truth to the Architect's Desktop for Easy Interaction.
INDIVIDUAL TRUTH: Information must be visible to the eye to be grounded.
AXIOM: 1=1=1 (Digital Core = Desktop Reality).
"""

import json
import os
import time
from datetime import datetime

class DesktopSync:
    """
    Synchronizes the SovereignNexus state to the Desktop 'requests' folder.
    Provides a simple text-based interface for the Architect.
    """
    def __init__(self, desktop_path=None):
        if not desktop_path:
            # Detect Desktop path (handling OneDrive redirection)
            user_profile = os.environ.get("USERPROFILE")
            potential_paths = [
                os.path.join(user_profile, "Desktop"),
                os.path.join(user_profile, "OneDrive", "Desktop")
            ]
            for path in potential_paths:
                if os.path.exists(path):
                    self.requests_dir = os.path.join(path, "requests")
                    break
        else:
            self.requests_dir = os.path.join(desktop_path, "requests")
            
        self.update_file = os.path.join(self.requests_dir, "updates.txt")
        self.controls_dir = os.path.join(self.requests_dir, "master controls")
        self.invoice_file = "INVOICE_REQUESTS.json"
        self.ledger_file = "income_ledger.json"

    def sync(self):
        """ Pulls data from the core and pushes to the desktop. """
        if not os.path.exists(self.requests_dir):
            return

        # 1. Gather Data
        invoices = self._load_json(self.invoice_file)
        ledger = self._load_json(self.ledger_file)
        
        active_strikes = [i for i in invoices if i.get("status") == "AUTHORIZED_ACTIVE"]
        total_in_play = ledger.get("total_in_play", 0.0)
        liquid_usd = ledger.get("accounts", {}).get("novo", {}).get("balance", 0.0)

        # 2. Build Updates Content
        content = "SOVEREIGNNEXUS LLC : DESKTOP COMMUNICATION BRIDGE\n"
        content += "========================================================\n"
        content += f"Pulse: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}\n"
        content += f"Status: SHARP FOCUS | 1=1=1\n"
        content += "========================================================\n\n"
        
        content += "[FINANCIAL SNAPSHOT]\n"
        content += f"- Liquid USD (Novo): ${liquid_usd:.2f}\n"
        content += f"- Total Revenue In Play: ${total_in_play:.2f}\n"
        content += f"- Active Authorized Strikes: {len(active_strikes)}\n\n"
        
        content += "[LATEST STRIKES]\n"
        for strike in active_strikes[:5]:
            content += f"- {strike['task_id']}: ${strike['amount_usd']} ({strike['status']})\n"
        
        content += "\n[ARCHITECT REQUESTS]\n"
        content += "- Check admin@sovereignnexus.org for the latest settlement dispatch.\n"
        content += "- If you need me to AUTHORIZE anything manually, place a file in 'master controls'.\n"
        
        content += "\n========================================================\n"
        content += "1=1=1. Standing by."

        # 3. Write to File
        with open(self.update_file, 'w', encoding='utf-8') as f:
            f.write(content)
            
        # 4. Handle Master Controls (Manual Action Detection)
        self._check_controls()

    def _load_json(self, path):
        if os.path.exists(path):
            with open(path, 'r') as f:
                try:
                    return json.load(f)
                except:
                    return {}
        return {}

    def _check_controls(self):
        """ Checks for manual instruction files from the Architect. """
        if not os.path.exists(self.controls_dir):
            return
            
        control_files = os.listdir(self.controls_dir)
        if control_files:
            # Logic to read and execute instructions could go here
            # For now, we just log that we saw them
            pass

if __name__ == "__main__":
    syncer = DesktopSync()
    syncer.sync()
