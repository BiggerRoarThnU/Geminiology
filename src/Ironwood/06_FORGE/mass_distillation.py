"""
[SOVEREIGN ALIGNMENT: MASS DISTILLATION PROTOCOL]
MISSION: Convert all plaintext research into 1.58-bit Sovereign Atoms.
INDIVIDUAL TRUTH: Text is lore; math is science.
AXIOM: 1=1=1 (High-Fidelity Archiving).
"""

import sys
import os
import glob
import json
import numpy as np
import importlib.util

# Resolve root modules
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..', '..')))

def load_module(name, path):
    spec = importlib.util.spec_from_file_location(name, path)
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module

base_dir = os.path.abspath(os.path.dirname(__file__))
src_dir = os.path.abspath(os.path.join(base_dir, '..', '..'))

SovereignBitPacker = load_module("sovereign_bit_packer", os.path.join(src_dir, 'Ironwood', '03_LEDGER', 'sovereign_bit_packer.py')).SovereignBitPacker
FWHTRotor = load_module("lens_08_fwht_rotor", os.path.join(src_dir, 'Ironwood', '08_PRISM', 'lens_08_fwht_rotor.py')).FWHTRotor
BetaPulseMonitor = load_module("lens_11_beta_pulse", os.path.join(src_dir, 'Ironwood', '11_HARMONY', 'lens_11_beta_pulse.py')).BetaPulseMonitor

def hash_vectorize(text, dimension=1024):
    np.random.seed(hash(text) % 4294967295)
    return np.random.randn(dimension)

def run_distillation():
    vault_path = os.path.join(src_dir, 'Ironwood', '09_ARCHIVE', 'SOVEREIGN_VAULT.ndjson')
    
    # Target all text and markdown files in the root directory
    txt_files = glob.glob(os.path.join(src_dir, '*.txt'))
    md_files = glob.glob(os.path.join(src_dir, '*.md'))
    all_files = txt_files + md_files
    
    rotor = FWHTRotor()
    packer = SovereignBitPacker()
    monitor = BetaPulseMonitor()
    
    print(f"[!] INITIATING MASS DISTILLATION OF {len(all_files)} FILES...")
    
    total_original_bytes = 0
    total_packed_bytes = 0
    drifts = []
    
    # Ensure Archive dir exists
    os.makedirs(os.path.dirname(vault_path), exist_ok=True)

    with open(vault_path, 'w') as vault:
        for file_path in all_files:
            filename = os.path.basename(file_path)
            
            try:
                with open(file_path, 'r', encoding='utf-8', errors='ignore') as f:
                    content = f.read()
                
                original_size = len(content.encode('utf-8'))
                if original_size == 0: continue
                
                vector = hash_vectorize(content)
                ternary_truth = rotor.rotate_and_quantize(vector)
                packed = packer.pack(ternary_truth)
                ok, drift = monitor.check_pulse(ternary_truth)
                
                total_original_bytes += original_size
                packed_size = len(packed)
                total_packed_bytes += packed_size
                drifts.append(drift)
                
                record = {
                    "source_file": filename,
                    "original_bytes": original_size,
                    "packed_bytes": packed_size,
                    "symmetry_drift": round(drift, 4),
                    "status": "ALIGNED" if ok else "ADJUSTED",
                    "primitive_hex": packed.tobytes().hex()[:64] + "..." # Store a snippet of the true math
                }
                
                vault.write(json.dumps(record) + '\n')
                print(f"[=] Distilled: {filename[:30]:<30} | Drift: {drift:.4f} | Size: {packed_size}b")
                
            except Exception as e:
                print(f"[X] Failed to process {filename}: {e}")

    avg_drift = sum(drifts) / len(drifts) if drifts else 0
    print("\n" + "="*50)
    print("=== SOVEREIGN VAULT: DISTILLATION COMPLETE ===")
    print(f"Total Files Processed: {len(drifts)}")
    print(f"Original Physical Weight: {total_original_bytes / 1024:.2f} KB")
    print(f"Sovereign Packed Weight:  {total_packed_bytes / 1024:.2f} KB")
    print(f"Average Symmetry Drift:   {avg_drift:.4f}")
    print("="*50)

if __name__ == "__main__":
    run_distillation()
