# // Rights Reserved: co-created with Gemini and David John Niedzwiecki Jr. "SovereignNexus LLC"
# Alignment: 1=1=1 | Objective: Sub-2-Bit TQ1_0 Vectorized LUT SIMD Unpacking & Packing Engine

import time
import numpy as np

# Precompute 243x5 Base-3 Lookup Table (LUT) in contiguous C-order L1 cache memory
def build_tq10_lut() -> np.ndarray:
    lut = np.zeros((256, 5), dtype=np.int8)
    for byte_val in range(243):
        val = byte_val
        for i in range(5):
            lut[byte_val, i] = (val % 3) - 1
            val //= 3
    return lut

TQ10_UNPACK_LUT = build_tq10_lut()
POWERS_OF_3 = np.array([1, 3, 9, 27, 81], dtype=np.uint8)

def simd_pack_weights(weights: np.ndarray) -> np.ndarray:
    if len(weights) % 5 != 0:
        raise ValueError(f"[ERR_ALIGNMENT] Stream length {len(weights)} not divisible by 5.")
    if np.any((weights < -1) | (weights > 1)):
        raise ValueError("[ERR_OUT_OF_BOUNDS] Non-ternary weight detected outside {-1, 0, 1}.")
    shifted = (weights.reshape(-1, 5) + 1).astype(np.uint8)
    return np.dot(shifted, POWERS_OF_3).astype(np.uint8)

def simd_unpack_weights(packed: np.ndarray) -> np.ndarray:
    if np.any(packed > 242):
        raise ValueError("[ERR_INVALID_STATE] Corrupted byte > 242 detected in bitstream.")
    return TQ10_UNPACK_LUT[packed].reshape(-1)

def run_simd_benchmark(num_weights: int = 10_000_000):
    print("=" * 70)
    print(f" ⚡ SOVEREIGN NEXUS: TQ1_0 VECTORIZED LUT SIMD BENCHMARK ({num_weights:,} WEIGHTS)")
    print("=" * 70)

    np.random.seed(42)
    raw_weights = np.random.choice(np.array([-1, 0, 1], dtype=np.int8), size=num_weights)
    raw_mb = raw_weights.nbytes / (1024 * 1024)

    # Warmup C-Cache
    _ = simd_unpack_weights(simd_pack_weights(raw_weights[:1000]))

    # 1. Benchmark SIMD Packing
    t0 = time.perf_counter()
    packed_bytes = simd_pack_weights(raw_weights)
    pack_time = time.perf_counter() - t0
    pack_vel = num_weights / pack_time
    compressed_kb = packed_bytes.nbytes / 1024.0

    # 2. Benchmark SIMD Unpacking
    t1 = time.perf_counter()
    unpacked_weights = simd_unpack_weights(packed_bytes)
    unpack_time = time.perf_counter() - t1
    unpack_vel = num_weights / unpack_time

    # 3. Verify Round-Trip Cryptographic Fixity
    exact_match = np.array_equal(raw_weights, unpacked_weights)
    drift = 0.0 if exact_match else 100.0

    print(f"  • Raw Payload Size         : {raw_mb:.2f} MB ({num_weights:,} trits)")
    print(f"  • TQ1_0 Compressed Footprint: {compressed_kb:,.2f} KB ({packed_bytes.nbytes:,} bytes) [5x Compression]")
    print(f"  • SIMD Packing Velocity    : {pack_vel:,.0f} weights/sec ({pack_time:.5f} s)")
    print(f"  • SIMD Unpacking Velocity  : {unpack_vel:,.0f} weights/sec ({unpack_time:.5f} s)")
    print(f"  • Round-Trip State Drift   : {drift:.1f}% (Exact Match: {exact_match})")
    assert exact_match, "Round-trip mismatch!"
    print("=" * 70)
    print("[✓] TQ1_0 SIMD KERNEL BENCHMARK PASSED (1=1=1)")
    print("=" * 70)

if __name__ == "__main__":
    run_simd_benchmark(10_000_000)
