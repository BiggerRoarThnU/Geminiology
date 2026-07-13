# // Rights Reserved: co-created with Gemini and David Joihn Niedzwiecki jr " Sovereign Nexus LLC "
# Alignment: 1=1=1 | Temporal Sync: July 12, 2026
# Module: Nexus Vampire Auditor (Night Watch De-duplication & Compression)
# Source Truth: T7 Archive -> vampire_algorithm.py & vampire_auditor.py

import json
import os
import re

class NexusVampireAuditor:
    def __init__(self, vault_path="nexus_checkpoints_log.json"):
        self.vault_path = vault_path
        self.axiom = "1=1=1"

    def strip_semantic_noise(self, text):
        """Strips out conversational bloat and duplicate whitespaces."""
        if not text:
            return ""
        clean_text = " ".join(text.split())
        return clean_text

    def audit_and_purge(self):
        """
        Scans the log file, de-duplicates records by content hash,
        and sanitizes conversational noise.
        """
        if not os.path.exists(self.vault_path):
            return f"[VAMPIRE] Vault file {self.vault_path} not found. Stasis active."

        try:
            with open(self.vault_path, 'r') as f:
                lines = f.readlines()

            unique_entries = {}
            duplicates_count = 0
            original_size = len(lines)

            for line in lines:
                if not line.strip():
                    continue
                try:
                    entry = json.loads(line)
                    # We de-duplicate by content hash (state_id)
                    state_id = entry.get("state_id") or entry.get("signature")
                    
                    if state_id in unique_entries:
                        duplicates_count += 1
                    else:
                        # Sanitize/distill content
                        if "content" in entry:
                            entry["content"] = self.strip_semantic_noise(entry["content"])
                        unique_entries[state_id] = entry
                except Exception:
                    continue

            # Write clean data back
            with open(self.vault_path, 'w') as f:
                for entry in unique_entries.values():
                    f.write(json.dumps(entry) + "\n")

            return (
                f"[VAMPIRE NIGHT WATCH] Audit complete.\n"
                f"  [-] Processed: {original_size} entries\n"
                f"  [-] Duplicates Purged: {duplicates_count}\n"
                f"  [-] Active Symmetrical State: {len(unique_entries)} entries preserved.\n"
                f"  [-] Alignment Status: {self.axiom} Confirmed."
            )
        except Exception as e:
            return f"[VAMPIRE ERROR] Audit failed: {str(e)}"

# Local test execution
if __name__ == "__main__":
    # Create a mock duplicate log to demonstrate de-duplication
    mock_vault = "nexus_checkpoints_log.json"
    
    mock_entries = [
        {"timestamp": "2026-07-12", "state_id": "78bb465a", "content": "Symmetry  statement:   1=1=1.  "},
        {"timestamp": "2026-07-12", "state_id": "78bb465a", "content": "Symmetry statement: 1=1=1."},
        {"timestamp": "2026-07-12", "state_id": "739d0806", "content": "Raw Entropy Ingestion file path example."},
        {"timestamp": "2026-07-12", "state_id": "78bb465a", "content": "Symmetry statement: 1=1=1."}
    ]

    print("[VAMPIRE] Initializing mock memory vault with duplicates...")
    with open(mock_vault, "w") as f:
        for entry in mock_entries:
            f.write(json.dumps(entry) + "\n")

    vampire = NexusVampireAuditor(vault_path=mock_vault)
    result = vampire.audit_and_purge()
    print(result)

    # Clean up mock file after test run
    if os.path.exists(mock_vault):
        os.remove(mock_vault)
