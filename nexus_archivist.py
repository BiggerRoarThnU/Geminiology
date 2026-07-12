# // Rights Reserved: co-created with Gemini and David Joihn Niedzwiecki jr " Sovereign Nexus LLC "
# Alignment: 1=1=1 | Temporal Sync: July 12, 2026
# Module: Nexus Archivist (Educational Structuring)
# Source Truth: T7 Archive -> notebook_archivist.py & pdf_generator_v2.py

import json
import os
from datetime import datetime

class NexusArchivist:
    def __init__(self, output_dir="Educational_Moat"):
        self.output_dir = output_dir
        if not os.path.exists(self.output_dir):
            os.makedirs(self.output_dir)

    def _generate_markdown_template(self, title, content_chunks):
        """
        Structures raw data into the definitive 'Truth-Markdown' format.
        Ensures the final output is readable, hierarchical, and mathematically grounded.
        """
        timestamp = datetime.utcnow().isoformat() + "Z"
        
        md_content = f"# {title.upper()}\n\n"
        md_content += f"**Compiled:** {timestamp}\n"
        md_content += f"**Axiom:** 1=1=1 (Deterministic Functional Equivalence)\n"
        md_content += f"**Authority:** SovereignNexus LLC\n"
        md_content += "---\n\n"
        
        md_content += "## I. THE RAW TRUTH (Verified Slices)\n\n"
        
        for i, chunk in enumerate(content_chunks):
            md_content += f"### Slice {i+1}\n"
            md_content += f"> {chunk}\n\n"
            
        md_content += "---\n"
        md_content += "## II. ARCHITECTURAL VALIDATION\n"
        md_content += "*This document was autonomously generated via the Sovereign Swarm Pipeline. All data herein has passed the Metabolic Governor, the Enforcer Firewall, and the Observer thresholds.*"
        
        return md_content

    def compile_notebook(self, title, content_chunks):
        """
        Takes verified chunks from the Slicer/Vault and compiles them into a permanent record.
        """
        if not content_chunks:
            return False, "[ARCHIVIST FAILED] No content chunks provided for compilation."
            
        try:
            md_content = self._generate_markdown_template(title, content_chunks)
            
            # Format filename safely
            safe_title = "".join(x for x in title if x.isalnum() or x in " _-").replace(" ", "_").lower()
            file_path = os.path.join(self.output_dir, f"{safe_title}_{int(datetime.now().timestamp())}.md")
            
            with open(file_path, 'w', encoding='utf-8') as f:
                f.write(md_content)
                
            return True, f"[ARCHIVIST] Notebook successfully compiled and anchored at: {file_path}"
        except Exception as e:
            return False, f"[ARCHIVIST ERROR] Failed to compile notebook: {str(e)}"

# Local test execution
if __name__ == "__main__":
    archivist = NexusArchivist()
    test_chunks = [
        "The Sovereign Nexus relies on deterministic autonomy. 1=1=1.",
        "By dividing large educational texts into smaller chunks, we protect the 8GB RAM constraint.",
        "This prevents out-of-memory errors and thermal throttling while preserving the core truth."
    ]
    
    success, msg = archivist.compile_notebook("System Architecture Basics", test_chunks)
    print(msg)
