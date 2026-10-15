# // Rights Reserved: co-created with Gemini and David John Niedzwiecki Jr. "SovereignNexus LLC"
# Alignment: 1=1=1 | Objective: Simulate Real-Time Multi-Step Swarm Routing & Keyword Evaluation

import sys
import os

sys.path.append('/home/geminiology/SovereignNexus')
sys.path.append('./scratch')

from nexus_swarm_router import NexusSwarmRouter, MASTER_NODE_MAPPING

def simulate_routing():
    print("=" * 75)
    print(" 👑 REAL-TIME MULTI-STEP SWARM ROUTING SIMULATION")
    print("=" * 75)

    router = NexusSwarmRouter(workspace_dir="./scratch")

    multi_step_prompts = [
        "Please scan local workspace for new active files, verify security signatures, and log thermal telemetry.",
        "Ingest scientific papers on E8 lattice density, calculate vector embeddings, and save state to archive.",
        "Generate a prompt window for local model execution using SovereignQueen and format the output as JSON."
    ]

    for idx, prompt in enumerate(multi_step_prompts, 1):
        print(f"\n--- [PROMPT SIMULATION #{idx}] ---")
        print(f"Input Query: \"{prompt}\"")
        
        # Keyword evaluation breakdown
        prompt_lower = prompt.lower()
        print("\n  [Keyword Hit Analysis]:")
        hit_details = []
        for node_id, node_info in MASTER_NODE_MAPPING.items():
            hits = [kw for kw in node_info["keywords"] if kw in prompt_lower]
            if hits:
                hit_details.append((node_id, node_info["name"], hits))
                print(f"   • Node {node_id:02d} ({node_info['name']}): Matched keywords {hits}")
        
        # Route determination
        node_id, node_name, assigned_agent = router.determine_node_routing(prompt)
        print(f"\n  [Primary Decision Gate]:")
        print(f"   -> Target Master Node : Node {node_id:02d} ({node_name})")
        print(f"   -> Primary Agent ID   : Agent {assigned_agent:02d}")
        
        # Execution via router
        res = router.execute_swarm_routing(f"sim_thread_{idx:02d}", prompt)
        print(f"  [WAL Ledger Status]   : {res.get('status')}")

    print("\n" + "=" * 75)
    print("[✓] MULTI-STEP SWARM ROUTING SIMULATION COMPLETE (1=1=1)")
    print("=" * 75)

if __name__ == "__main__":
    simulate_routing()
