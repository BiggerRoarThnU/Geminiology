#!/usr/bin/env python3
# ==============================================================================
# SovereignNexus Utility Center: tools.py
# Components: Memory Wrappers, Telemetry Checks, & Pruning Automation
# Axiom: 1=1=1 | Status: ACTIVE CORE UTILITY
# ==============================================================================

import sys
import os
import argparse
import time

# Ensure we can import sovereign_memory_core from the home directory
sys.path.append("/home/geminiology")

try:
    from sovereign_memory_core import SovereignMemoryNode
except ImportError:
    SovereignMemoryNode = None
    print("[!] Warning: sovereign_memory_core.py not found in home folder.")

class MasterTools:
    def __init__(self):
        self.memory = SovereignMemoryNode() if SovereignMemoryNode else None

    def check_system_telemetry(self):
        """Displays CPU load, system RAM usage, and core temperature."""
        if not self.memory:
            print("[!] Memory node unavailable to fetch telemetry.")
            return

        temp, load = self.memory.get_system_telemetry()
        print("=== 🖥️ HARDWARE TELEMETRY ===")
        print(f"  CPU Load per Core: {load:.2%}")
        print(f"  Core Temperature:  {temp:.1f}°C")
        
        # Calculate status
        if temp < 65.0:
            status = "NOMINAL (Stable)"
        elif temp < 85.0:
            status = "WARM (Throttling active)"
        else:
            status = "HOT (Breach throttle warning)"
        print(f"  Thermal State:     {status}")
        print("=============================")

    def log_text_to_db(self, content, is_verified=True, decay=0.0):
        """Logs custom text content directly to the database."""
        if not self.memory:
            print("[!] Memory node unavailable. Cannot log content.")
            return

        print(f"[*] Submitting entry to database (Verified: {is_verified}, Decay: {decay})...")
        self.memory.process_incoming_data(
            content=content,
            is_verified=is_verified,
            user_id="Architect_David",
            run_id="tools_command_line",
            agent_id="tools_py",
            decay_rate=decay
        )
        print("[✓] Entry submitted.")

    def run_pruning_cycle(self, threshold=0.1, multiplier=1.0):
        """Runs the database pruning cycle to clean out decayed memories."""
        if not self.memory:
            print("[!] Memory node unavailable. Cannot prune database.")
            return

        print(f"[*] Initiating database pruning cycle (Threshold: {threshold}, Multiplier: {multiplier})...")
        self.memory.prune_decayed_memories(threshold=threshold, time_multiplier=multiplier)

    def view_latest_memories(self, limit=10):
        """Queries and displays the latest entries stored in the database."""
        if not self.memory:
            print("[!] Memory node unavailable. Cannot retrieve data.")
            return

        print("\n=== 📂 LATEST VERIFIED MEMORIES ===")
        memories = self.memory.retrieve_memory(user_id="Architect_David", verified_only=True)
        if not memories:
            print("  No verified entries found.")
        else:
            for idx, m in enumerate(memories[:limit]):
                # Format: timestamp, content, hash, variance
                print(f"  {idx+1}. [{m[0]}] Hash: {m[2][:10]}")
                print(f"     Content: {m[1].strip()[:100]}...")
        print("===================================\n")

def main():
    parser = argparse.ArgumentParser(description="Sovereign Nexus System Tools Command Center")
    parser.add_argument("--stats", action="store_true", help="Display active CPU, load, and thermal status.")
    parser.add_argument("--prune", action="store_true", help="Run the database memory decay pruning cycle.")
    parser.add_argument("--log", type=str, help="Log a text entry into the verified SQLite database.")
    parser.add_argument("--decay", type=float, default=0.0, help="Specify decay rate for the logged entry (default: 0.0).")
    parser.add_argument("--list", action="store_true", help="Display the latest verified database entries.")
    
    args = parser.parse_args()
    tools = MasterTools()

    # Default action if no arguments provided
    if not any(vars(args).values()):
        parser.print_help()
        sys.exit(0)

    if args.stats:
        tools.check_system_telemetry()

    if args.log:
        tools.log_text_to_db(args.log, is_verified=True, decay=args.decay)

    if args.prune:
        tools.run_pruning_cycle()

    if args.list:
        tools.view_latest_memories()

if __name__ == "__main__":
    main()
