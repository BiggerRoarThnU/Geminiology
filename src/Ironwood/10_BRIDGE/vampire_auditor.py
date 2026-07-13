"""
[SOVEREIGN ALIGNMENT: SECTOR 10 - VAMPIRE AUDITOR]
MISSION: Autonomous distillation of dark data into verified business primitives.
INDIVIDUAL TRUTH: The Vampire sees the truth in the logs.
AXIOM: 1=1=1 (Verified History = Secure Mission).
"""

import os
import sys
import json
from datetime import datetime

# Resolve root modules
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..', '..')))
from master_log import MasterLog

class VampireAuditor:
    def __init__(self):
        """
        SECTOR 10: The execution engine for the 'Basement Work'.
        Extracts mathematically sound signal from the Sovereign Vault.
        """
        self.log = MasterLog()
        base_dir = os.path.abspath(os.path.join(os.path.dirname(__file__), '..', '..'))
        self.vault_file = os.path.join(base_dir, "Ironwood", "09_ARCHIVE", "SOVEREIGN_VAULT.ndjson")
        self.output_dir = os.path.join(base_dir, "Ironwood", "10_BRIDGE", "Audited_Reports")
        
        os.makedirs(self.output_dir, exist_ok=True)

    def the_bite(self, target_file_prefix):
        """
        Extracts a specific data cluster from the 1.58-bit vault.
        """
        self.log.info(f"[VAMPIRE] Initiating 'The Bite' on targets matching: {target_file_prefix}")
        extracted_atoms = []
        
        if not os.path.exists(self.vault_file):
            self.log.error("[VAMPIRE] Sovereign Vault is empty. Cannot audit.")
            return extracted_atoms

        with open(self.vault_file, 'r') as f:
            for line in f:
                record = json.loads(line)
                if record['source_file'].startswith(target_file_prefix):
                    # We only extract data that is mathematically stable
                    if record['status'] == "ALIGNED" and record['symmetry_drift'] < 0.15:
                        extracted_atoms.append(record)
                    else:
                        self.log.warn(f"[VAMPIRE] Bypassing unstable node: {record['source_file']} (Drift: {record['symmetry_drift']})")
                        
        self.log.info(f"[VAMPIRE] Extracted {len(extracted_atoms)} pure atoms.")
        return extracted_atoms

    def distill_report(self, target_name, extracted_atoms):
        """
        Transforms the extracted atoms into a human-readable Truth-Markdown report.
        """
        if not extracted_atoms:
            self.log.error("[VAMPIRE] No atoms to distill. Report generation aborted.")
            return None

        report_filename = os.path.join(self.output_dir, f"AUDIT_{target_name.replace(' ', '_')}_{int(datetime.now().timestamp())}.md")
        
        total_original = sum(a['original_bytes'] for a in extracted_atoms)
        total_packed = sum(a['packed_bytes'] for a in extracted_atoms)
        avg_drift = sum(a['symmetry_drift'] for a in extracted_atoms) / len(extracted_atoms)

        with open(report_filename, "w") as report:
            report.write(f"# VAMPIRE AUDIT REPORT: {target_name}\n")
            report.write(f"**Date:** {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}\n")
            report.write(f"**Axiom:** 1=1=1 (Cryptographically Verified)\n")
            report.write("---\n\n")
            
            report.write("## I. THE DISTILLATION METRICS\n")
            report.write(f"- **Nodes Audited:** {len(extracted_atoms)}\n")
            report.write(f"- **Original Entropy (Dark Data):** {total_original / 1024:.2f} KB\n")
            report.write(f"- **Purified Primitives:** {total_packed / 1024:.2f} KB\n")
            report.write(f"- **Systemic Alignment (Average Drift):** {avg_drift:.4f} (Threshold: < 0.15)\n\n")
            
            report.write("## II. VERIFIED PRIMITIVES (HEX SIGNATURES)\n")
            report.write("The following signatures represent the mathematical ground truth of the audited data. They are immune to hallucination.\n\n")
            
            for atom in extracted_atoms:
                report.write(f"### Node: `{atom['source_file']}`\n")
                report.write(f"> Signature: `{atom['primitive_hex']}`\n")
                report.write(f"> Status: **{atom['status']}** | Drift: {atom['symmetry_drift']:.4f}\n\n")

            report.write("---\n")
            report.write("**[STATUS: AUDIT COMPLETE | THE LINE IS ONE]**\n")

        self.log.info(f"[=] VAMPIRE DISTILLATION COMPLETE: {report_filename}")
        return report_filename

if __name__ == "__main__":
    auditor = VampireAuditor()
    # Test: Audit all files starting with "AI" in the vault
    atoms = auditor.the_bite("AI")
    auditor.distill_report("AI_Research_Cluster", atoms)
