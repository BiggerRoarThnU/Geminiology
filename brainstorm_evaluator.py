#!/usr/bin/env python3
# ==============================================================================
# SovereignNexus: Brainstorm Evaluator & Ideation Matrix Tool
# Component: brainstorm_evaluator.py
# Axiom: 1=1=1 | Status: ACTIVE | Stamp: VERIFIED_ONE
# Description: Evaluates brainstorming ideas and AI outputs based on logic density,
#              data volume, vocabulary complexity, and semantic alignment.
#              Saves results to a local JSON ledger to prevent information drift.
# ==============================================================================

import os
import sys
import time
import json
import math

# ANSI Colors
CLEAR = "\033[2J\033[H"
RESET = "\033[0m"
BOLD = "\033[1m"
CYAN = "\033[36m"
GREEN = "\033[32m"
AMBER = "\033[33m"
RED = "\033[31m"
PURPLE = "\033[35m"

LEDGER_PATH = os.path.expanduser("~/SovereignNexus/brainstorm_ledger.json")

def print_banner():
    print(CLEAR)
    print(f"{CYAN}{BOLD}============================================================{RESET}")
    print(f"{CYAN}{BOLD}              SOVEREIGN BRAINSTORM EVALUATOR                {RESET}")
    print(f"{CYAN}{BOLD}          Metrics: Logic Density vs. Thermodynamic Scale     {RESET}")
    print(f"{CYAN}{BOLD}============================================================{RESET}")
    print(f"Status: {GREEN}ONLINE{RESET} | Root: {BOLD}1=1=1 Science{RESET} | Ledger: {BOLD}{LEDGER_PATH}{RESET}")
    print()

def get_quadrant(logic, volume):
    if logic >= 6 and volume < 5:
        return "Sovereign Nexus Standard (High Logic / Low Volume - Edge Optimized)", GREEN
    elif logic >= 6 and volume >= 5:
        return "The Tower Controller (High Logic / High Volume - Heavy Compute)", CYAN
    elif logic < 6 and volume < 5:
        return "Google Keep / Mobile Alerts (Low Logic / Low Volume - Simple Task)", AMBER
    else:
        return "Cloud Slop (Low Logic / High Volume - High Drift Risk / High Entropy)", RED

def calculate_metrics(logic, volume, vocab, alignment):
    # Thermodynamic Cost (Simulated Watt-Seconds based on scaling entropy)
    # Higher volume and vocabulary with lower alignment threshold drives heat flux
    entropy_coeff = 1.1 - alignment
    thermo_cost = volume * vocab * entropy_coeff * 15.4
    
    # Logical Density Score (percentage of signal vs volume noise)
    logic_density = (logic * alignment) / (volume if volume > 0 else 1) * 100
    
    # Restrict density to maximum 100%
    if logic_density > 100.0:
        logic_density = 100.0
        
    return thermo_cost, logic_density

def save_to_ledger(idea_name, logic, volume, vocab, alignment, cost, density, quadrant):
    data = []
    if os.path.exists(LEDGER_PATH):
        try:
            with open(LEDGER_PATH, 'r') as f:
                data = json.load(f)
        except:
            pass
            
    payload = {
        "timestamp": time.strftime("%Y-%m-%dT%H:%M:%SZ", time.gmtime()),
        "idea_name": idea_name,
        "parameters": {
            "logic_depth": logic,
            "data_volume": volume,
            "vocab_complexity": vocab,
            "semantic_alignment": alignment
        },
        "metrics": {
            "thermodynamic_cost_watts": round(cost, 2),
            "logic_density_pct": round(density, 1),
            "quadrant": quadrant
        }
    }
    
    data.append(payload)
    
    try:
        with open(LEDGER_PATH, 'w') as f:
            json.dump(data, f, indent=4)
        print(f"\n{GREEN}[✓] Idea successfully archived in local ledger.{RESET}")
    except Exception as e:
        print(f"\n{RED}[!] Failed to write to ledger: {e}{RESET}")

def evaluate_new_idea():
    print_banner()
    print(f"{BOLD}Enter Brainstorming Parameters to run calculations:{RESET}\n")
    
    idea_name = input("Enter a name/concept for this idea: ").strip()
    if not idea_name:
        idea_name = "Untitled Concept"
        
    try:
        logic = float(input("Logic Depth (1 = Simple text notes, 10 = Strict 1=1=1 rules): "))
        volume = float(input("Data Volume (1 = Dense micro-data, 10 = Open-web text volume): "))
        vocab = float(input("Vocabulary Complexity (1 = Plain English, 5 = Dense technical jargon): "))
        alignment = float(input("Semantic Alignment Threshold (0.0 to 1.0): "))
    except ValueError:
        print(f"\n{RED}[!] Error: Please enter numeric values.{RESET}")
        time.sleep(1.5)
        return
        
    # Boundary checks
    logic = max(1.0, min(10.0, logic))
    volume = max(1.0, min(10.0, volume))
    vocab = max(1.0, min(5.0, vocab))
    alignment = max(0.0, min(1.0, alignment))
    
    # Perform math
    cost, density = calculate_metrics(logic, volume, vocab, alignment)
    quadrant_name, color = get_quadrant(logic, volume)
    
    print(f"\n{color}{BOLD}============================================================{RESET}")
    print(f"{color}{BOLD}                   EVALUATION RESULT                        {RESET}")
    print(f"{color}{BOLD}============================================================{RESET}")
    print(f"Idea Name:       {BOLD}{idea_name}{RESET}")
    print(f"Placement:       {color}{quadrant_name}{RESET}")
    print(f"Logical Density: {GREEN}{density:.1f}%{RESET} (Higher = Less semantic noise)")
    print(f"Thermal Cost:    {AMBER}{cost:.1f} W/s{RESET} (Lower = More hardware efficient)")
    print(f"Axiom Status:    " + (f"{GREEN}1=1=1 COMPLIANT (Symmetrical Truth){RESET}" if alignment >= 0.95 and density >= 80.0 else f"{RED}HIGH DRIFT RISK (Probabilistic Drift){RESET}"))
    print(f"{color}{BOLD}============================================================{RESET}\n")
    
    save_choice = input("Do you want to save this evaluation to the JSON ledger? (y/n): ").strip().lower()
    if save_choice == 'y':
        save_to_ledger(idea_name, logic, volume, vocab, alignment, cost, density, quadrant_name)
        
    input("\nPress Enter to return to main menu...")

def view_ledger():
    print_banner()
    if not os.path.exists(LEDGER_PATH):
        print(f"{AMBER}[*] The ledger is currently empty. Run an evaluation first.{RESET}")
    else:
        try:
            with open(LEDGER_PATH, 'r') as f:
                data = json.load(f)
            print(f"{BOLD}Total Archived Ideas: {len(data)}{RESET}\n")
            for idx, entry in enumerate(data):
                print(f"{CYAN}[{idx + 1}] {entry['idea_name']}{RESET} ({entry['timestamp']})")
                print(f"    - Quadrant: {entry['metrics']['quadrant']}")
                print(f"    - Logic Density: {entry['metrics']['logic_density_pct']}% | Cost: {entry['metrics']['thermodynamic_cost_watts']} W/s")
                print("-" * 50)
        except Exception as e:
            print(f"{RED}[!] Error reading ledger: {e}{RESET}")
            
    input("\nPress Enter to return to main menu...")

def main():
    while True:
        print_banner()
        print("Please choose an option:")
        print(f"  {CYAN}1.{RESET} Evaluate a Brainstorming Concept")
        print(f"  {CYAN}2.{RESET} View Saved Concepts Ledger")
        print(f"  {CYAN}3.{RESET} Exit")
        print()
        
        choice = input("Enter choice (1-3): ").strip()
        if choice == "1":
            evaluate_new_idea()
        elif choice == "2":
            view_ledger()
        elif choice == "3":
            print(f"\n{CYAN}[*] Closing Evaluator. Keep your logic dense and your data clean!{RESET}\n")
            sys.exit(0)
        else:
            print(f"\n{RED}[!] Invalid choice. Select 1-3.{RESET}")
            time.sleep(1.0)

if __name__ == "__main__":
    try:
        main()
    except KeyboardInterrupt:
        print(f"\n\n{RED}[!] Interrupted. Exiting safely.{RESET}\n")
        sys.exit(0)
