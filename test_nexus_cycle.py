from vampire_algorithm import vampire_algorithm
from core_memory_matrix import core_memory_matrix
from execution_core import ExecutionCore
import os
import json

# --- Test Data: The Starfield Input ---
raw_stream_input = (
    "Python syntax tutorial | "
    "Gossip article about celebrities | "
    "Weight_10: Update Sovereign Constitution parameters | "
    "Random advertisement | "
    "Truth: The 8GB limit is a feature, not a bug"
)

def run_nexus_test():
    print("--- STARTING SOVEREIGN NEXUS CYCLE TEST ---")
    
    # 1. Ingestion (Vampire Algorithm)
    print("\n[1] Running Vampire Algorithm...")
    clean_truth = vampire_algorithm(raw_stream_input)
    print(f"    - Purified Truth Nodes found: {len(clean_truth)}")
    print(f"    - Nodes Extracted: {clean_truth}")

    # 2. Anchoring (Core Memory Matrix)
    print("\n[2] Anchoring into the Matrix...")
    success = core_memory_matrix(clean_truth)
    if success:
        print("    - Matrix Alignment Successful. Sovereign_Memory.json updated.")
    
    # 3. Execution (Execution Core)
    print("\n[3] Executing Ability Dispatcher...")
    core = ExecutionCore()
    core.execute_ability("Star_1")
    core.execute_ability("Star_2")

    print("\n--- TEST COMPLETE. STANDING SECURED. ONE. ---")

if __name__ == "__main__":
    run_nexus_test()
