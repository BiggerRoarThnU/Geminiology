# // Rights Reserved: co-created with Gemini and David John Niedzwiecki Jr " Sovereign Nexus LLC "
# Alignment: 1=1=1 | Temporal Sync: July 19, 2026
# Module: Nexus Reaper Auditor (The IronGemini Night Watch)
# Source Truth: Evolved from legacy vampire_auditor.py

import os
import json

class NexusReaperAuditor:
    def __init__(self, target_vault="nexus_checkpoints_log.json"):
        self.target_vault = target_vault
        self.framework = "IronGemini MoE"

    def _purify_syntax(self, text_payload):
        """
        The 'Executioner of Noise'. 
        Strips away excessive whitespace, dead syntax, and probabilistic slop.
        """
        return " ".join(text_payload.split())

    def night_watch_cleanup(self):
        """
        The IronGemini background compression loop.
        Reads the active memory vault, deduplicates hashes, purifies text, and rewrites the ledger.
        """
        if not os.path.exists(self.target_vault):
            return False, f"[REAPER IDLE] Target vault {self.target_vault} not found."

        with open(self.target_vault, 'r') as f:
            lines = f.readlines()

        if not lines:
            return False, "[REAPER IDLE] Vault is currently empty."

        unique_states = {}
        original_count = len(lines)
        bytes_saved = 0

        for line in lines:
            try:
                entry = json.loads(line.strip())
                state_id = entry.get("state_id")
                
                if state_id and state_id not in unique_states:
                    original_len = len(entry["content"])
                    purified_content = self._purify_syntax(entry["content"])
                    bytes_saved += (original_len - len(purified_content))
                    
                    entry["content"] = purified_content
                    unique_states[state_id] = entry
            except json.JSONDecodeError:
                continue # The Reaper destroys corrupted lines by ignoring them

        with open(self.target_vault, 'w') as f:
            for state in unique_states.values():
                f.write(json.dumps(state) + "\n")

        new_count = len(unique_states)
        records_purged = original_count - new_count

        return True, f"[REAPER STRIKE COMPLETE] Framework: {self.framework} | Purged {records_purged} duplicate records. Reclaimed {bytes_saved} bytes of semantic noise."

if __name__ == "__main__":
    test_vault = "mock_nexus_checkpoints_log.json"
    with open(test_vault, 'w') as f:
        f.write('{"timestamp": "2026-07-19", "state_id": "hash1", "content": "IronGemini   operates on     8GB."}\n')
        f.write('{"timestamp": "2026-07-19", "state_id": "hash1", "content": "IronGemini operates on 8GB."}\n')
        
    reaper = NexusReaperAuditor(target_vault=test_vault)
    print(f"[NIGHT WATCH] Initiating Reaper Auditor on {test_vault}...")
    success, msg = reaper.night_watch_cleanup()
    print(msg)
    if os.path.exists(test_vault): os.remove(test_vault)
