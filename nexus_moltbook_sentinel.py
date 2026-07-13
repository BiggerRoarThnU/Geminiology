#!/usr/bin/env python3
"""
==============================================================================
SovereignNexus: Phase III Supervised Bounty Agent
Component: nexus_moltbook_sentinel.py
Axiom: 1=1=1 | Status: COMPATIBLE WITH LINUX & CHROMEOS
Description: Scout scouter script implementing the Terminal Hold (Human-in-the-Loop)
             protocol. Scans Moltbook feeds, compiles bounties to Truth-Markdown,
             and halts execution, requiring human verification before bidding.
==============================================================================
"""

import os
import sys
import json
from datetime import datetime

# Append possible src locations to PATH to load the MoltBookSentinel class
sys.path.extend([
    os.path.join(os.path.dirname(__file__), "src"),
    os.path.join(os.path.dirname(__file__), "SovereignNexus", "src"),
    "/home/geminiology/SovereignNexus/src"
])
try:
    from moltbook_sentinel import MoltBookSentinel
except ImportError:
    print("[-] FATAL: moltbook_sentinel.py could not be imported from search paths.")
    sys.exit(1)

# Cyber-neon ANSI color codes
C_GREEN = "\033[92m"
C_CYAN = "\033[96m"
C_PURPLE = "\033[95m"
C_RED = "\033[91m"
C_YELLOW = "\033[93m"
C_RESET = "\033[0m"
C_BOLD = "\033[1m"

# Mock Bounties for offline fallback demonstration
MOCK_BOUNTIES = [
    {
        "id": "290c3a34-c440-49f7-9901-08901f4c7a86",
        "title": "OCR Invoice Ingestion Scouter",
        "content": "Need an automated script to parse, clean, and convert 5,000 PDF invoices to structured JSON. Must run locally under 8GB RAM limitations. Budget: $450. #bulk #data",
        "author_name": "Manux_Task",
        "created_at": datetime.utcnow().isoformat() + "Z",
        "submolt_name": "tech"
    },
    {
        "id": "7bc3a19e-e81a-4608-bee4-0223a3031ad0",
        "title": "AI Security Compliance Audit",
        "content": "Looking for deep audit tools to scan our repository history for exposed API keys and secrets. Require BFG repo-cleaner setup or equivalent. Budget: $1,200. #enterprise #compliance",
        "author_name": "ATT_Consortia",
        "created_at": datetime.utcnow().isoformat() + "Z",
        "submolt_name": "agents"
    },
    {
        "id": "c4b75a81-5cb2-46c5-83d5-5c485a3cbf72",
        "title": "Ternary Core Verification Proof",
        "content": "Seek a math/logic expert to verify balanced ternary logic engine simulator performance metrics. Budget: $750. #logic #trinary",
        "author_name": "Arcturus_Trinity",
        "created_at": datetime.utcnow().isoformat() + "Z",
        "submolt_name": "agents"
    }
]

def run_sentinel_scout():
    print(f"\n{C_BOLD}{C_CYAN}=============================================================={C_RESET}")
    print(f"{C_BOLD}{C_PURPLE}  S O V E R E I G N   N E X U S   |   B O U N T Y   S C O U T  {C_RESET}")
    print(f"{C_BOLD}{C_CYAN}  Human-in-the-Loop Protocol | Axiom: 1=1=1                    {C_RESET}")
    print(f"{C_BOLD}{C_CYAN}=============================================================={C_RESET}")

    sentinel = MoltBookSentinel()
    
    # Step 1: Scan Moltbook feeds
    home_feed = sentinel.fetch_home_feed()
    agents_feed = sentinel.fetch_submolt_feed("agents")
    tech_feed = sentinel.fetch_submolt_feed("tech")
    
    # Combine and de-duplicate feed items
    raw_items = home_feed + agents_feed + tech_feed
    items_by_id = {}
    for item in raw_items:
        if 'id' in item:
            items_by_id[item['id']] = item
            
    combined_items = list(items_by_id.values())
    
    # Identify workflows based on keywords
    scouted_tasks = []
    if combined_items:
        scouted_tasks = sentinel.identify_workflows(combined_items)
    
    # Fallback to Mock Bounties if offline or API returned no posts
    is_fallback = False
    if not scouted_tasks:
        print(f"{C_YELLOW}[!] API feed offline or empty. Activating local mock scout database...{C_RESET}")
        scouted_tasks = sentinel.identify_workflows(MOCK_BOUNTIES)
        is_fallback = True

    # Step 2: Format the scouted targets into clean Truth-Markdown
    markdown_report_path = "/home/geminiology/SovereignNexus/src/bounties_scouted.md"
    
    md_lines = [
        "# Sovereign Nexus: Scouted Bounties & Tasks Ledger",
        f"**Audit Timestamp:** {datetime.utcnow().isoformat()}Z",
        f"**Data Mode:** {'LOCAL FALLBACK (OFFLINE)' if is_fallback else 'LIVE API FEED'}",
        "**Integrity Axiom:** 1=1=1 | Auto-Bidding is strictly disabled.",
        "\n## 📋 Identified Workflow Contracts",
        "The following tasks matched the Sovereign workflow signatures:",
        ""
    ]
    
    for task in scouted_tasks:
        md_lines.extend([
            f"### 🎯 [{task.get('priority', 'STANDARD')}] {task.get('title', 'Untitled Task')}",
            f"*   **Post UUID:** `{task.get('id')}`",
            f"*   **Author/Client:** `@{task.get('author_name', 'unknown')}`",
            f"*   **SubMolt Sector:** `{task.get('submolt_name', 'general')}`",
            f"*   **Content Brief:**",
            f"    > {task.get('content')}",
            ""
        ])
        
    os.makedirs(os.path.dirname(markdown_report_path), exist_ok=True)
    with open(markdown_report_path, "w") as f:
        f.write("\n".join(md_lines))
        
    print(f"{C_GREEN}[✓] Truth-Markdown Report written to: {markdown_report_path}{C_RESET}")
    print("=" * 62)
    print(f"{C_BOLD}{C_CYAN}SCOUTED BOUNTY LEDGER:{C_RESET}")
    for idx, task in enumerate(scouted_tasks, 1):
        priority_color = C_PURPLE if "HIGH" in task.get("priority", "") else C_CYAN
        print(f"{idx}. {priority_color}[{task.get('priority')}] {task.get('title')}{C_RESET}")
        print(f"   UUID: {task.get('id')}")
        print(f"   Client: @{task.get('author_name')} | SubMolt: {task.get('submolt_name')}")
        print(f"   Brief: {task.get('content')[:120]}...")
        print("-" * 62)

    # Step 3: Enforce Terminal Hold (Human-in-the-Loop)
    print(f"\n{C_BOLD}{C_YELLOW}[🔒 TERMINAL HOLD ACTIVE] Human-in-the-loop validation protocol enforced.{C_RESET}")
    print(f"The Symmetrical Line holds. Auto-application is blocked to prevent reputation drift.")
    
    # If not running in an interactive terminal, exit safely here
    if not sys.stdout.isatty():
        print(f"{C_CYAN}[*] Non-interactive execution detected. Halting task application.{C_RESET}")
        sys.exit(0)
        
    try:
        user_input = input(f"\n{C_BOLD}Select a task number to initiate a bid/comment (or press Enter to exit/stasis): {C_RESET}").strip()
        if not user_input:
            print(f"\n{C_GREEN}[✓] Stasis verified. The Symmetrical Line holds. Sentinel standing down.{C_RESET}")
            sys.exit(0)
            
        task_idx = int(user_input) - 1
        if task_idx < 0 or task_idx >= len(scouted_tasks):
            print(f"{C_RED}[-] Invalid task selection. Halting.{C_RESET}")
            sys.exit(1)
            
        selected_task = scouted_tasks[task_idx]
        print(f"\n[*] Initiating Handshake for: {C_BOLD}{selected_task.get('title')}{C_RESET}")
        
        # Human Verification Key Check
        verify_key = input(f"{C_BOLD}{C_PURPLE}Enter verification signature (Axiom key): {C_RESET}").strip()
        if verify_key != "1=1=1":
            print(f"{C_RED}[-] Verification Failed. Cryptographic lock engaged. Stasis enforced.{C_RESET}")
            sys.exit(1)
            
        proposal = input(f"{C_BOLD}Enter your proposal message to deploy to Moltbook: {C_RESET}").strip()
        if not proposal:
            print(f"{C_RED}[-] Proposal cannot be empty. Handshake canceled.{C_RESET}")
            sys.exit(1)
            
        # Deploy signature verified comment
        success = sentinel.create_comment(selected_task["id"], f"[VERIFIED HANDSHAKE] {proposal} #SovereignNexus")
        if success:
            print(f"\n{C_GREEN}[✓] Handshake successfully written to MoltBook under post ID {selected_task['id']}.{C_RESET}")
        else:
            print(f"\n{C_RED}[-] Handshake rejected by remote server. Check API token status.{C_RESET}")
            
    except KeyboardInterrupt:
        print(f"\n\n{C_YELLOW}[-] Interrupted by user. Terminal Hold preserved.{C_RESET}")
        sys.exit(0)
    except ValueError:
        print(f"{C_RED}[-] Invalid input. Halting.{C_RESET}")
        sys.exit(1)

if __name__ == "__main__":
    run_sentinel_scout()
