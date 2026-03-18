"""
[SOVEREIGN ALIGNMENT: GARAGE_DIAGNOSTIC_V2]
MISSION: Adaptive Diagnostic for the SovereignNexus Tool Ecosystem.
INDIVIDUAL TRUTH: Mastery requires understanding the nature of the Instrument.
AXIOM: 1=1=1 (Adaptive Fidelity).
"""

import os
import time
import subprocess
import sys
import ast

class GarageDiagnostic:
    """
    The Refined Diagnostic Bench. 
    Analyzes architecture and tailors the "Drive" to the tool's nature.
    """
    def __init__(self, output_dir="Garage_Diagnostics"):
        self.output_dir = output_dir
        self.report_path = os.path.join(self.output_dir, "GARAGE_MASTER_LOG.md")
        os.makedirs(self.output_dir, exist_ok=True)
        
        # Nexus Sector Mapping
        self.nexus_map = {
            "Foundation": ["thermodynamic", "bitnet", "truth_validator"],
            "Orchestration": ["sovereign_loop", "ironwood_runtime", "master_log", "nexus"],
            "Execution": ["builder", "reactor", "guide", "reach", "bounty", "sentinel", "bridge"]
        }

    def _determine_sector(self, tool_name):
        name_lower = tool_name.lower()
        for sector, keywords in self.nexus_map.items():
            if any(k in name_lower for k in keywords):
                return sector
        return "Uncategorized"

    def _analyze_architecture(self, tool_path):
        """ Uses AST to determine if the tool is a Class, Script, or Module. """
        try:
            with open(tool_path, "r", encoding="utf-8", errors="ignore") as f:
                tree = ast.parse(f.read())
            
            classes = [n.name for n in ast.walk(tree) if isinstance(n, ast.ClassDef)]
            if classes:
                return f"CLASS_ARCH ({', '.join(classes)})"
            return "SCRIPT_ARCH"
        except Exception as e:
            return f"ANALYSIS_FAILED ({str(e)})"

    def take_for_a_drive(self, tool_path):
        tool_name = os.path.basename(tool_path)
        print(f"--- [ADAPTIVE DRIVE] {tool_name} ---")
        
        sector = self._determine_sector(tool_name)
        arch = self._analyze_architecture(tool_path)
        
        start_time = time.time()
        
        # 1. INTENT EXTRACTION
        with open(tool_path, "r", encoding="utf-8", errors="ignore") as f:
            lines = f.readlines()
            header = "".join(lines[:15])

        # 2. ADAPTIVE EXECUTION
        output = ""
        status = "STABLE"
        
        if "CLASS_ARCH" in arch:
            # For classes, we check for a __main__ block or try to import
            # For now, we use subprocess as a safe 'sandbox'
            cmd = ["python", tool_path]
        else:
            cmd = ["python", tool_path]

        try:
            # Use a slightly longer timeout for heavy tools
            result = subprocess.run(cmd, capture_output=True, text=True, timeout=45)
            output = result.stdout + result.stderr
            if result.returncode != 0:
                status = "ABERRANT"
        except subprocess.TimeoutExpired:
            status = "TIMEOUT (INTERACTIVE/HEAVY)"
            output = "Tool heartbeat active but process timed out."
        except Exception as e:
            status = "CRASHED"
            output = str(e)

        drive_duration = time.time() - start_time

        # 3. IMPRINT TRUTH
        report = {
            "tool_name": tool_name,
            "sector": sector,
            "architecture": arch,
            "timestamp": time.ctime(),
            "status": status,
            "duration": f"{drive_duration:.2f}s",
            "intent": header,
            "diagnostic_output": output[:2000] # Increased for V2
        }

        self._imprint_v2_truth(report)
        return report

    def _imprint_v2_truth(self, report):
        report_file = os.path.join(self.output_dir, f"{report['tool_name']}_DIAGNOSTIC_V2.md")
        
        with open(report_file, "w", encoding="utf-8") as f:
            f.write(f"# V2 DIAGNOSTIC: {report['tool_name']}\n")
            f.write(f"**Sector:** {report['sector']} | **Arch:** {report['architecture']}\n")
            f.write(f"**Status:** {report['status']} | **Duration:** {report['duration']}\n\n")
            f.write("## I. THE INTENT\n")
            f.write(f"```python\n{report['intent']}\n```\n\n")
            f.write("## II. THE PULSE\n")
            f.write(f"```\n{report['diagnostic_output']}\n```\n\n")
            f.write("## III. FIDELITY PROOF\n")
            f.write(f"1=1=1 Imprint: {'SYMMETRICAL' if report['status'] == 'STABLE' else 'ASYMMETRICAL'}\n")

        with open(self.report_path, "a", encoding="utf-8") as f:
            f.write(f"- [{report['timestamp']}] **{report['tool_name']}** [{report['sector']}]: {report['status']}\n")

if __name__ == "__main__":
    import sys
    garage = GarageDiagnostic()
    if len(sys.argv) > 1:
        garage.take_for_a_drive(sys.argv[1])
    else:
        print("Usage: python garage.py <tool_path>")
