#!/usr/bin/env python3
import os
import re
import hashlib
from datetime import datetime

def print_header():
    print("\n" + "="*70)
    print(" VANGUARD SECTOR 3: AGENT 24 (THE LOG AGENT) ONLINE ")
    print(" DOMINION LOG PARSER | AXIOM: 1=1=1 | STATUS: ACTIVE ")
    print("="*70 + "\n")

# Path Setup
CHAT_LOG_PATH = "/home/geminiology/Archive_Daily_Logs/chat log current mission educational.txt"
CROWN_DIR = os.path.expanduser("~/SovereignNexus/src/Sovereign_Crown/")
PILLARS_LEDGER = os.path.join(CROWN_DIR, "Pillars_Truth_Ledger.md")

os.makedirs(CROWN_DIR, exist_ok=True)

# 1. Pillars of Truth Patterns (What Matters)
PILLAR_KEYWORDS = [
    r"1=1=1", r"fidelity", r"deterministic", r"autonomy", r"guardrail",
    r"gan-on-diamond", r"airlock", r"moe", r"vampire", r"lullaby",
    r"symmetric logic", r"least privilege", r"unyielding logic",
    r"sovereignnexus", r"substrate", r"edge computing", r"beacon",
    r"prov-agent", r"provenance", r"fixity stamp"
]

# 2. Ambient Noise Patterns (What Doesn't Matter)
NOISE_KEYWORDS = [
    r"ticket", r"cast netting", r"loading dock", r"animal control",
    r"kitten", r"bagel", r"bacon", r"monster", r"alani", r"breakfast"
]

pillar_regex = re.compile("|".join(PILLAR_KEYWORDS), re.IGNORECASE)
noise_regex = re.compile("|".join(NOISE_KEYWORDS), re.IGNORECASE)

def process_logs():
    print_header()
    
    if not os.path.exists(CHAT_LOG_PATH):
        print(f"[-] ERROR: Active Chat Log missing at: {CHAT_LOG_PATH}")
        return
        
    print(f"[!] Log Agent scanning active chat archive: {CHAT_LOG_PATH}")
    print("[!] Separating core architectural pillars from ambient noise...\n")
    
    try:
        with open(CHAT_LOG_PATH, "r", encoding="utf-8", errors="ignore") as f:
            content = f.read()
    except Exception as e:
        print(f"[-] ERROR: Failed to read log file: {e}")
        return

    # Split by double newlines or paragraph blocks
    blocks = [b.strip() for b in content.split("\n\n") if b.strip()]
    
    pillars_extracted = []
    noise_count = 0
    
    for block in blocks:
        # Check if the block is a paragraph that contains target concepts
        has_pillar = pillar_regex.search(block)
        has_noise = noise_regex.search(block)
        
        if has_pillar and not (has_noise and len(block) < 300):
            # This is verified applied science / structural truth
            pillars_extracted.append(block)
        elif has_noise:
            noise_count += 1
            
    # Format the Pillars Ledger
    timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    ledger_content = f"# SOVEREIGN PILLARS OF TRUTH LEDGER\n"
    ledger_content += f"## Extracted by Agent 24: The Log Agent\n"
    ledger_content += f"## Timestamp: {timestamp} | Axiom: 1=1=1\n\n"
    
    for i, pillar in enumerate(pillars_extracted):
        clean_text = "\n".join([line.strip() for line in pillar.split("\n") if line.strip()])
        ledger_content += f"### Pillar {i+1:02d}\n"
        ledger_content += f"{clean_text}\n\n"
        
    # Generate cryptographic fixity stamp for the entire ledger
    stamp = hashlib.sha256(ledger_content.encode("utf-8")).hexdigest()
    ledger_content += f"## FIXITY STAMP\n`{stamp}`\n"
    
    try:
        with open(PILLARS_LEDGER, "w", encoding="utf-8") as f:
            f.write(ledger_content)
    except Exception as e:
        print(f"[-] ERROR: Failed to write to {PILLARS_LEDGER}: {e}")
        return
        
    # Print telemetry to console
    print("="*70)
    print(" THE LOG AGENT HAS COMPLETED THE SYMMETRICAL EXTRACTION ")
    print(f" Total Text Blocks Scanned  : {len(blocks)}")
    print(f" Verified Pillars Anchored  : {len(pillars_extracted)}")
    print(f" Noise Variables Discarded  : {noise_count}")
    print(f" Symmetrical Fixity Stamp   : {stamp[:16]}...")
    print("="*70 + "\n")
    
    # Route execution telemetry to Swarm Router (Master Node 08: Discovery & Active Ingress)
    try:
        import sys
        sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))
        from swarm_router import route_log_entry
        db_payload = f"Dominion Log Ingress Complete. Scanned: {len(blocks)}, Anchored: {len(pillars_extracted)}, Fixity: {stamp}"
        route_log_entry(24, db_payload)
    except Exception as e:
        print(f"[-] Warning: Failed to route database telemetry: {e}")
        
    print()
    
    if pillars_extracted:
        print("[!] Preview of Recent Anchored Pillars:")
        for idx, p in enumerate(pillars_extracted[-3:]):
            first_line = p.split("\n")[0][:80]
            print(f"   {idx+1}. {first_line}...")
        print()

if __name__ == "__main__":
    process_logs()
