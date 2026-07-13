import os
import re

print("\n" + "="*60)
print(" VANGUARD SECTOR 1: AGENT 01 (THE ANCHOR) ONLINE ")
print("="*60 + "\n")

# The Physical Ground
ARCHIVE_DIR = os.path.expanduser("~/SovereignNexus/src/Vanguard_Archive/")
CROWN_DIR = os.path.expanduser("~/SovereignNexus/src/Sovereign_Crown/")
os.makedirs(CROWN_DIR, exist_ok=True)

LEDGER_PATH = os.path.join(CROWN_DIR, "Core_Truth_Ledger.md")

# Strict Filters for Pure Science and Logic
# 1. Finds variable assignments, math operations, and the 1=1=1 axiom
math_logic_pattern = re.compile(r'(1=1=1|==|!=|\+=|-=|\*=|\/=|^\s*[\w\.]+\s*=\s*[^,]+$)')
# 2. Finds core architectural Python structures
structural_pattern = re.compile(r'^\s*(def|class|import|return|yield)\s+')

print(f"[!] Agent 01 scanning 269 GB Substrate Archive at: {ARCHIVE_DIR}")
print("[!] Extracting pure mathematical and structural truth...\n")

truth_count = 0
files_scanned = 0

with open(LEDGER_PATH, "w", encoding="utf-8") as ledger:
    ledger.write("# SOVEREIGN CORE TRUTH LEDGER\n")
    ledger.write("## Extracted by Agent 01: The Anchor\n\n")
    
    for root, dirs, files in os.walk(ARCHIVE_DIR):
        for file in files:
            files_scanned += 1
            file_path = os.path.join(root, file)
            
            try:
                with open(file_path, "r", encoding="utf-8", errors="ignore") as f:
                    lines = f.readlines()
                
                extracted_lines = []
                for line in lines:
                    # If it matches strict math or code architecture, it is pure truth
                    if math_logic_pattern.search(line) or structural_pattern.search(line):
                        extracted_lines.append(line.strip())
                
                if extracted_lines:
                    ledger.write(f"### Source: {file}\n```python\n")
                    for el in extracted_lines:
                        ledger.write(f"{el}\n")
                        truth_count += 1
                    ledger.write("```\n\n")
                    
            except Exception as e:
                pass # Agent 01 ignores noise and read errors quietly

print("="*60)
print(f" THE ANCHOR HAS COMPLETED ITS SWEEP ")
print(f" Files Scanned: {files_scanned}")
print(f" Verified Truths Extracted: {truth_count}")
print(f" Immutable Ledger Forged At: {LEDGER_PATH}")
print("="*60 + "\n")
