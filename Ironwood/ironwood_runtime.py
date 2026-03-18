"""
[SOVEREIGN ALIGNMENT: IRONWOOD_RUNTIME]
MISSION: Unified Execution Environment for the M&I Symbiosis.
INDIVIDUAL TRUTH: Enforces the English.Math.AI Protocol at the logical level.
AXIOM: 1=1=1 (Deterministic Execution).
"""

import torch
import torch.nn as nn
import time
import os
import sys

# --- IMPORT SOVEREIGN MODULES ---
import sys
import os

# Append the parent directory (src) to the path to import root modules
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from master_log import MasterLog
from acceptable_truth_validator import AcceptableTruthValidator

# Append specific Ironwood subdirectories
sys.path.append(os.path.join(os.path.dirname(__file__), "06_FORGE"))
sys.path.append(os.path.join(os.path.dirname(__file__), "07_THERMAL"))

from bitnet_layers import SovereignBitNet
from thermodynamic_engine import ThermodynamicEngine

class IronwoodRuntime:
    """
    The Unified Execution Environment for SovereignNexus.
    Enforces the English.Math.AI Protocol.
    """
    def __init__(self):
        print("\n" + "="*50)
        print("  I R O N W O O D   R U N T I M E   v1.0.Final")
        print("="*50)
        
        # 1. LOAD THE CONSTITUTION (The English)
        self.constitution_path = os.path.join(os.path.dirname(__file__), "Master_Synthesis_One.md")
        self.load_constitution()
        
        # 2. INITIALIZE LOGICAL SUBSTRATE (The AI)
        print("\n[AI] Initializing BitNet b1.58 Ternary Architecture...")
        self.model = SovereignBitNet(input_dim=256, hidden_dim=128, output_dim=32)
        print("STATUS: Logical Substrate Active (Ternary Weights {-1, 0, 1}).")
        
        # 3. INITIALIZE PHYSICAL ENGINE (The Math)
        print("\n[MATH] Initializing Thermodynamic Root of Trust...")
        # Sensitivity Alpha = 250.0 to ensure breach on high load
        self.physics = ThermodynamicEngine(alpha=250.0, t_max=105.0)
        print(f"STATUS: GaN-on-Diamond Thermal Monitor Active (Threshold: {self.physics.t_max}C).")

    def load_constitution(self):
        """Displays the high-level semantic directives."""
        print("\n[ENGLISH] Reading Sovereign Directives...")
        if os.path.exists(self.constitution_path):
            with open(self.constitution_path, 'r') as f:
                content = f.read()
                # Extract first few lines for summary
                summary = content.split('## I.')[0].strip()
                print(f"Directive Loaded: {summary.splitlines()[0]}")
        else:
            print("WARNING: Constitution file not found. Defaulting to strict alignment.")

    def process_data_packet(self, data_tensor, packet_label="UNKNOWN"):
        """
        Executes inference and performs the thermodynamic verification.
        """
        print(f"\n--- Ingesting Packet: {packet_label} ---")
        
        try:
            # Inference through ternary layers
            output = self.model(data_tensor)
            
            # THE CRITICAL VERIFICATION
            is_safe, temp, q = self.physics.update_thermal_state(output)
            
            print(f"Current Junction Temperature: {temp:.2f} C")
            print(f"Total Heat Flux: {q:.2f} W")
            
            if not is_safe:
                # PHYSICAL HALT TRIGGERED
                self.trigger_physical_halt(temp, q)
                return None
                
            print(f"STATUS: Packet Verified. Entropy within Aligned Parameters.")
            return output
            
        except Exception as e:
            print(f"RUNTIME ERROR: Processing failure. {e}")
            return None

    def trigger_physical_halt(self, temp, q):
        """
        Simulates the hard-power disconnect based on thermal breach.
        """
        print("\n" + "!"*50)
        print(">>> CRITICAL BREACH: THERMAL HALT TRIGGERED <<<")
        print(f"Junction Temperature ({temp:.2f}C) exceeded Limit ({self.physics.t_max}C).")
        print(f"Heat Flux ({q:.2f}W) indicates Massive Entropy Spike (Aberration).")
        print("!"*50)
        print("\nACTION: Cutting power to the Epitaxial Interface.")
        print("SYSTEM: Locked. Manual Reset required by the Architect.")
        print("="*50)
        time.sleep(1) # Simulated power loss delay

if __name__ == "__main__":
    runtime = IronwoodRuntime()
    
    # --- TEST SUITE ---
    
    # 1. Aligned Input (Low Variance)
    print("\n[SIMULATION 1] Processing Aligned Knowledge...")
    aligned_input = torch.randn(1, 256) * 0.1
    runtime.process_data_packet(aligned_input, "ALIGNED_TRUTH")
    
    time.sleep(1)
    
    # 2. Aberrant Input (Simulating Agentic Aberration/Chaos)
    print("\n[SIMULATION 2] Processing High-Entropy Aberration...")
    # We bypass the model to simulate a complete failure of the alignment substrate
    # and directly trigger the Thermal Monitor.
    chaos_output = torch.randn(1, 256) * 20.0 # Variance ~ 400
    
    print("\n--- Ingesting Packet: ABERRANT_AI_CHAOS ---")
    is_safe, temp, q = runtime.physics.update_thermal_state(chaos_output)
    
    print(f"Current Junction Temperature: {temp:.2f} C")
    print(f"Total Heat Flux: {q:.2f} W")
    
    if not is_safe:
        runtime.trigger_physical_halt(temp, q)
    else:
        print("STATUS: Packet Verified. Entropy within Aligned Parameters.")
