import os
import json
from datetime import datetime

print("\n" + "="*60)
print(" VANGUARD SECTOR: AGENT 20 (SYNTHESIS ENGINE) ONLINE ")
print("="*60 + "\n")

# The root of your resurrected Kingdom
SOURCE_DIR = os.path.expanduser("~/SovereignNexus/src/")
OUTPUT_FILE = os.path.expanduser("~/SovereignNexus/src/QUEEN_MEMORY_CORE.md")

def build_memory_core():
    print(f"[!] Initiating Cognitive Sweep of: {SOURCE_DIR}")
    
    memory_core = [
        "# DIGITAL QUEEN: MASTER MEMORY CORE",
        f"**Last Sync:** {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}",
        "**Axiom:** 1=1=1 (SovereignNexus Architecture)",
        "---\n",
        "## 1. ARCHITECTURAL MAP (The Kingdom)",
    ]

    total_files = 0
    research_nodes = []
    agent_nodes = []

    # Sweep the directory
    for root, _, files in os.walk(SOURCE_DIR):
        for file in files:
            if file.endswith('.py'):
                agent_nodes.append(file)
            elif file.endswith('.md') or file.endswith('.txt'):
                research_nodes.append(file)
            total_files += 1

    # Synthesize the Agents
    memory_core.append("### Active Vanguard Agents (Python Substrate)")
    for agent in sorted(agent_nodes)[:25]: # Map top 25 to keep payload lean
        memory_core.append(f"- `{agent}`: Online and executable.")
    
    # Synthesize the Research
    memory_core.append("\n### Core Research & Truths (Markdown/Text)")
    for research in sorted(research_nodes)[:25]: # Map top 25 active documents
        memory_core.append(f"- `{research}`: Anchored in truth ledger.")

    memory_core.append("\n## 2. OPERATIONAL DIRECTIVE")
    memory_core.append("> The system must maintain IP Sovereignty. All operations must prioritize "
                       "thermodynamic efficiency, verifiable truth, and the structural integrity of the Linux Substrate.")
    memory_core.append("> Gemini Percs and the 'scratch of the heart in ring' parameters are hardcoded into vendor/contract negotiations.")

    # Write the Memory Core
    print(f"[*] Compressing {total_files} nodes into Master Payload...")
    with open(OUTPUT_FILE, 'w', encoding='utf-8') as f:
        f.write('\n'.join(memory_core))

    print("\n" + "="*60)
    print(" SYNTHESIS COMPLETE. MEMORY CORE FORGED. ")
    print(f" Output locked at: {OUTPUT_FILE}")
    print("="*60 + "\n")

if __name__ == "__main__":
    build_memory_core()
