import os
import subprocess
import json
from master_log import MasterLog

class ChubAgentSkill:
    """
    SovereignNexus Patch: The Chub Agent Skill
    Mission: Automate documentation fetching via Context Hub (chub).
    Ensures 100% API fidelity by bypassing knowledge cutoff issues.
    """
    def __init__(self):
        self.logger = MasterLog()

    def get_api_docs(self, tool_name, lang="py"):
        """ Fetches the latest documentation for a specific tool. """
        self.logger.info(f"[CHUB] Fetching latest docs for: {tool_name} (Lang: {lang})...")
        try:
            result = subprocess.run(
                ["chub", "get", tool_name, "--lang", lang],
                capture_output=True,
                text=True,
                check=True,
                shell=True
            )
            # Anchor the docs locally for high-fidelity RAG
            doc_path = f"C:\\Users\\Ofthe\\SovereignNexus\\src\\Ironwood\\extracted_logic\\DOCS_{tool_name.replace('/', '_')}.md"
            with open(doc_path, 'w', encoding='utf-8') as f:
                f.write(result.stdout)
            
            self.logger.info(f"[SUCCESS] API Docs anchored at: {doc_path}")
            return result.stdout
        except Exception as e:
            self.logger.error(f"[CHUB] Failed to fetch docs for {tool_name}: {e}")
            return None

if __name__ == "__main__":
    skill = ChubAgentSkill()
    # Test with Stripe to ensure our payment rails are 100% compliant
    skill.get_api_docs("stripe/api", lang="js")
