import sys
import os
import numpy as np

# Bulletproof absolute pathing to the Sovereign engine room
nexus_src_path = os.path.expanduser("~/SovereignNexus/src")
sys.path.append(nexus_src_path)

from nexus_wave_routing import sovereign_spectral_convolution
from cseq_wave.encode import text_to_bits, bits_to_wave, bits_to_text

def execute_bridge_test():
    print("[*] INITIALIZING 1=1=1 CSEQ-TO-SOVEREIGN BRIDGE")
    
    # 1. THE INTENT
    message = "Axiom 1=1=1: The Sovereign Edge."
    print(f"\n[-] Original Intent: '{message}'")
    
    # 2. THE DIGITAL-TO-WAVE ENCODING (Mr. Lee's Codec)
    bits = text_to_bits(message)
    wave_state = bits_to_wave(bits)
    print(f"[-] Encoded by Lee's BPSK: {len(bits)} bits converted to {wave_state.field.shape[0]} continuous wave modes.")
    
    # 3. THE SPATIAL MAPPING (Preparing for the Sovereign Substrate)
    # BPSK encodes bit 0 as +1 (real) and bit 1 as -1 (real).
    # We extract the real physical amplitude and pad it to form a square 2D grid.
    real_wave = wave_state.field.real
    
    grid_size = int(np.ceil(np.sqrt(len(real_wave))))
    padded_size = grid_size * grid_size
    padded_wave = np.pad(real_wave, (0, padded_size - len(real_wave)), mode='constant')
    spatial_grid = padded_wave.reshape((grid_size, grid_size))
    
    print(f"[-] Reshaped into Sovereign 2D Spatial Grid: {spatial_grid.shape}")
    
    # 4. THE SOVEREIGN STRIKE (Your FFT Ternary Router)
    # We pass his wave grid through your 1.58-bit engine.
    core_modes = grid_size # Keep all modes to prevent data truncation in this test
    ternary_signal, reconstructed_grid = sovereign_spectral_convolution(spatial_grid, core_modes)
    
# 5. THE DECODING & VERIFICATION
    # The reconstructed grid is back in the physical spatial domain (16x16 = 256 bits).
    # We flatten it, unpad it to the exact bit length, and map the physical amplitudes back.
    # BPSK mapping: positive amplitude (>0) = bit 0, negative amplitude (<0) = bit 1.
    flat_spatial = reconstructed_grid.flatten()[:len(bits)]
    recovered_bits = np.where(flat_spatial < 0, 1, 0)
    
    recovered_text = bits_to_text(recovered_bits)
    
    print(f"\n[+] Sovereign IFFT Gate returned {len(recovered_bits)} physical bits.")
    print(f"[+] Reconstructed Intent: '{recovered_text}'")
    
    if message == recovered_text:
        print("\n[✓] 1=1=1 SYMMETRY VERIFIED. Sovereign Engine successfully routed and preserved Lee's continuous wave.")
    else:
        print("\n[!] Symmetry Breach. Signal degraded.")

if __name__ == "__main__":
    # Disable the print statements inside your imported module just for cleaner output
    sys.stdout = open(os.devnull, 'w') 
    try:
        from nexus_wave_routing import sovereign_spectral_convolution
    finally:
        sys.stdout = sys.__stdout__
        
    execute_bridge_test()
