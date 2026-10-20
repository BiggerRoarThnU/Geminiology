import numpy as np
import time

def sovereign_spectral_convolution(spatial_signal, keep_modes):
    """
    1=1=1 Axiom: Continuous Wave logic for the Sovereign Edge.
    Converts spatial data into wave frequencies, correctly truncates high-frequency noise 
    using 2D FFT corner-packing, and enforces Ternary gating in the SPATIAL domain.
    """
    print("[*] Shifting Substrate from Spatial Domain to Frequency Domain...")
    start_time = time.time()
    
    # 1. THE FORWARD PASS: Convert 2D spatial grid to continuous wave
    wave_state = np.fft.rfft2(spatial_signal)
    
    # 2. THE CHOP SHOP (FREQUENCY DOMAIN): Low-Pass Filter
    compressed_wave = np.zeros_like(wave_state)
    compressed_wave[:keep_modes, :keep_modes] = wave_state[:keep_modes, :keep_modes]
    compressed_wave[-keep_modes:, :keep_modes] = wave_state[-keep_modes:, :keep_modes]
    
    # 3. THE INVERSE PASS: Return to Physical Reality FIRST
    # We must bring the wave back to the spatial domain before snapping it to integers
    filtered_spatial_state = np.fft.irfft2(compressed_wave, s=spatial_signal.shape)
    
    # 4. THE TERNARY STRIKE (SPATIAL DOMAIN): The Hardware Gate
    # Now that we are back in physical space, we force the continuous wave 
    # into our strict 1.58-bit Sovereign logic (-1, 0, 1)
    ternary_routing_signal = np.sign(filtered_spatial_state).astype(np.int8)
    
    calc_time = (time.time() - start_time) * 1000
    print(f"[*] Spectral Convolution Complete in {calc_time:.3f} ms.")
    
    return ternary_routing_signal, filtered_spatial_state

if __name__ == "__main__":
    # We generate structured wave noise rather than flat random white noise.
    # White noise has a flat spectrum (impossible to filter). This proves the math works.
    print("[-] Generating 1,000,000-Point Structured Context Grid...")
    x = np.linspace(0, 10 * np.pi, 1000)
    y = np.linspace(0, 10 * np.pi, 1000)
    xv, yv = np.meshgrid(x, y)
    
    # Base truth (sine/cosine waves) mixed with random noise
    mock_heavy_signal = np.sin(xv) + np.cos(yv) + (np.random.rand(1000, 1000) * 0.5)
    
    core_modes = 16
    ternary_signal, processed_space = sovereign_spectral_convolution(mock_heavy_signal, core_modes)
    
    print(f"[+] Original Structured Grid Shape: {mock_heavy_signal.shape}")
    print(f"[+] Compressed Ternary Wave Shape: {ternary_signal.shape} (Data Type: {ternary_signal.dtype})")
    print(f"[+] Final Reconstructed Spatial Shape: {processed_space.shape}")
