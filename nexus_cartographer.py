# // Rights Reserved: co-created with Gemini and David Joihn Niedzwiecki jr " Sovereign Nexus LLC "
# Alignment: 1=1=1 | Temporal Sync: July 12, 2026
# Module: Nexus Cartographer (System Mapping)
# Source Truth: T7 Archive -> nexus_cartographer.py & grand_cartographer.py

import os
from datetime import datetime

class NexusCartographer:
    def __init__(self, target_dir="Educational_Moat", index_file="INDEX.md"):
        self.target_dir = target_dir
        self.index_file = os.path.join(self.target_dir, index_file)

    def map_territory(self):
        """
        Scans the target directory and generates a Truth-Markdown Index.
        """
        if not os.path.exists(self.target_dir):
            os.makedirs(self.target_dir)

        files = [f for f in os.listdir(self.target_dir) if f.endswith('.md') and f != "INDEX.md"]
        
        index_content = "# THE SOVEREIGN INDEX: EDUCATIONAL MOAT\n\n"
        index_content += f"**Last Mapped:** {datetime.utcnow().isoformat()}Z\n"
        index_content += f"**Axiom:** 1=1=1 (Deterministic Functional Equivalence)\n"
        index_content += "---\n\n"
        
        if not files:
            index_content += "*The moat is currently empty. Awaiting Swarm ingestion.*\n"
        else:
            index_content += "## Verified Truth Assets\n\n"
            for file in sorted(files):
                # Basic formatting for the index links
                display_name = file.replace('_', ' ').replace('.md', '').title()
                index_content += f"- [{display_name}](./{file})\n"

        index_content += "\n---\n*Autonomously mapped by the Nexus Cartographer.*"

        try:
            with open(self.index_file, 'w', encoding='utf-8') as f:
                f.write(index_content)
            return True, f"[CARTOGRAPHER SUCCESS] Territory mapped. Index anchored at: {self.index_file} with {len(files)} assets."
        except Exception as e:
            return False, f"[CARTOGRAPHER ERROR] Failed to map territory: {str(e)}"

if __name__ == "__main__":
    # Create a mock file to prove the mapping logic if the directory is empty
    if not os.path.exists("Educational_Moat"):
        os.makedirs("Educational_Moat")
    with open("Educational_Moat/mock_systems_architecture.md", "w") as f:
        f.write("Mock data")

    cartographer = NexusCartographer()
    print("[CARTOGRAPHER] Initiating mapping sequence...")
    success, msg = cartographer.map_territory()
    print(msg)
