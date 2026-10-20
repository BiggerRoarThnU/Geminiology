#!/usr/bin/env python3
"""
SovereignNexus Core Verification Suite
Test: Continuous Wave BPSK <-> 1.58-Bit Spatial Ternary Bridge
Axiom: 1=1=1 (Intent == Physics == Code)
"""
import sys
import os
import numpy as np

# Dynamic root resolution
ROOT_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.append(os.path.join(ROOT_DIR, "src"))

from nexus_wave_routing import sovereign_spectral_convolution

def test_wave_reconstruction():
    message = "Axiom 1=1=1: The Sovereign Edge."
    
    # 1. BPSK Modulation: Bit 0 -> 0 rad (+1.0), Bit 1 -> pi rad (-1.0)
    raw_bytes = message.encode("utf-8")
    bits = np.unpackbits(np.frombuffer(raw_bytes, dtype=np.uint8))
    bpsk_signal = 1.0 - 2.0 * bits.astype(float)
    
    # 2. 2D Spatial Manifold Padding
    grid_dim = int(np.ceil(np.sqrt(len(bpsk_signal))))
    padded_signal = np.pad(bpsk_signal, (0, (grid_dim * grid_dim) - len(bpsk_signal)), mode='constant')
    spatial_grid = padded_signal.reshape((grid_dim, grid_dim))
    
    # 3. Spectral Convolution (FFT Low-Pass -> IFFT -> Spatial Ternary Strike)
    ternary_gate, reconstructed_spatial = sovereign_spectral_convolution(spatial_grid, keep_modes=grid_dim)
    
    # 4. Phase Demodulation
    recovered_flat = reconstructed_spatial.flatten()[:len(bits)]
    recovered_bits = np.where(recovered_flat < 0, 1, 0).astype(np.uint8)
    recovered_bytes = np.packbits(recovered_bits).tobytes()
    recovered_message = recovered_bytes.decode("utf-8", errors="replace")
    
    assert message == recovered_message, f"Parity failure: expected '{message}', got '{recovered_message}'"
    print(f"[✓] Bridge Parity Confirmed: '{recovered_message}'")

if __name__ == "__main__":
    test_wave_reconstruction()
