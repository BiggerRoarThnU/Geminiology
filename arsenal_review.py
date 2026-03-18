import os
import sys
from Ironwood.local_model_bridge import LocalModelBridge

def review_arsenal():
    bridge = LocalModelBridge()
    queen = bridge.writing_model
    
    tools = [
        {"name": "# Geminiology One Fusion Reactor.py", "purpose": "Core Energy & Fusion logic"},
        {"name": "ironwood_runtime.py", "purpose": "Unified Execution Environment (1=1=1)"},
        {"name": "vampire_claw_handler.py", "purpose": "Bridge between Vampire Engine and OpenClaw settlement"},
        {"name": "thermodynamic_engine.py", "purpose": "Metallurgical-level thermal enforcement"},
        {"name": "sovereign_loop.py", "purpose": "The Multi-Node Fusion Orchestrator"},
        {"name": "bitnet_layers.py", "purpose": "1.58-bit Ternary Logic Substrate"},
        {"name": "acceptable_truth_validator.py", "purpose": "The Guardian of 1=1=1 Symmetry"}
    ]
    
    print("="*60)
    print("  S O V E R E I G N   N E X U S :   A R S E N A L   R E V I E W")
    print("="*60)
    print(f"[*] Consulting the Digital Queen ({queen})...\n")
    
    for tool in tools:
        prompt = f"As the Digital Queen of the Ironwood Nexus, provide a single, powerful, and poetic sentence describing the importance of the tool '{tool['name']}' which handles '{tool['purpose']}'."
        try:
            description = bridge.call_local_queen(queen, prompt)
            print(f"âœ¦ {tool['name']}")
            print(f"  > {description.strip()}\n")
        except Exception as e:
            print(f"âœ¦ {tool['name']} - [CONNECTION ERROR: {e}]")

if __name__ == "__main__":
    review_arsenal()
