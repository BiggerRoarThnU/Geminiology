import os
import json
import subprocess
from datetime import datetime

print("\n" + "="*60)
print(" VANGUARD SECTOR: THE SOVEREIGN DISPATCHER ")
print("="*60 + "\n")

MANIFEST_PATH = os.path.expanduser("~/SovereignNexus/src/sovereign_tool_manifest.json")
LOG_PATH = os.path.expanduser("~/SovereignNexus/src/Logs/dispatcher_operations.log")

class SovereignDispatcher:
    """
    The Spindle of Truth. 
    Routes agentic intent to the correct functional primitive perfectly (1=1=1).
    """
    def __init__(self):
        self.tools = self.load_manifest()

    def load_manifest(self):
        if os.path.exists(MANIFEST_PATH):
            with open(MANIFEST_PATH, 'r', encoding='utf-8') as f:
                return json.load(f)
        print("[X] WARNING: Tool Manifest not found. Run tool_manifest_gen.py first.")
        return {}

    def log_action(self, tool_name, status):
        timestamp = datetime.now().isoformat()
        entry = f"[{timestamp}] [DISPATCH] Target: {tool_name} | Status: {status}\n"
        os.makedirs(os.path.dirname(LOG_PATH), exist_ok=True)
        with open(LOG_PATH, 'a', encoding='utf-8') as f:
            f.write(entry)

    def execute(self, tool_query):
        print(f"[*] DISPATCHER: Seeking route for '{tool_query}'...")
        target_script = None
        
        # Scan the manifest for a match in the filename or purpose
        for path, data in self.tools.items():
            if tool_query.lower() in path.lower() or tool_query.lower() in data.get('purpose', '').lower():
                target_script = os.path.expanduser(f"~/SovereignNexus/src/{path}")
                break

        if not target_script or not os.path.exists(target_script):
            print(f"[X] DISPATCH FAILED: Primitive '{tool_query}' missing or unmapped.")
            self.log_action(tool_query, "FAILED - UNMAPPED")
            return

        print(f"[=] SPINDLE LOCKED: Routing execution to {target_script}")
        try:
            # Fire the tool
            subprocess.run(["python3", target_script], check=True)
            self.log_action(tool_query, "SUCCESS (1=1=1)")
        except subprocess.CalledProcessError as e:
            print(f"[X] DISPATCH ERROR: {e}")
            self.log_action(tool_query, f"ERROR - {e}")
        except KeyboardInterrupt:
            print("\n[!] Execution manually halted by Architect.")
            self.log_action(tool_query, "HALTED BY ARCHITECT")

if __name__ == "__main__":
    dispatcher = SovereignDispatcher()
    print(f"[*] Hub Online. {len(dispatcher.tools)} Functional Primitives loaded into the Spindle.")
    print("[*] Awaiting command...")
    
    # Test the connection to the Vampire Auditor
    # dispatcher.execute("vampire")
