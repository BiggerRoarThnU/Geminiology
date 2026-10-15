# // Rights Reserved: co-created with Gemini and David John Niedzwiecki Jr. "SovereignNexus LLC"
# Alignment: 1=1=1 | Objective: Benchmark TQ1_0 Base-3 Weight Packing Across 1,000,000 Weights

import random
import sys
import time
import tracemalloc
from typing import List

class TQ10Engine:
    POWERS_OF_3 = [1, 3, 9, 27, 81]

    @classmethod
    def pack_chunk(cls, weights: List[int]) -> int:
        byte_val = 0
        for i in range(5):
            w = weights[i]
            if w not in (-1, 0, 1):
                raise ValueError(f"[ERR_OUT_OF_BOUNDS] Non-ternary weight detected: {w}")
            byte_val += (w + 1) * cls.POWERS_OF_3[i]
        return byte_val

    @classmethod
    def unpack_byte(cls, byte_val: int) -> List[int]:
        if byte_val > 242:
            raise ValueError(f"[ERR_INVALID_STATE] Byte {byte_val} exceeds base-3 limit (242). Corrupted bitstream.")
        
        trits = []
        val = byte_val
        for _ in range(5):
            trits.append((val % 3) - 1)
            val //= 3
        return trits

    @classmethod
    def pack_stream(cls, weights: List[int]) -> bytearray:
        if len(weights) % 5 != 0:
            raise ValueError(f"[ERR_ALIGNMENT] Weight stream length ({len(weights)}) is not divisible by 5.")
        
        packed = bytearray(len(weights) // 5)
        for i in range(0, len(weights), 5):
            packed[i // 5] = cls.pack_chunk(weights[i:i+5])
        return packed

    @classmethod
    def unpack_stream(cls, packed_bytes: bytearray) -> List[int]:
        unpacked = []
        for b in packed_bytes:
            unpacked.extend(cls.unpack_byte(b))
        return unpacked

def run_1M_benchmark(num_weights: int = 1_000_000):
    print("=" * 70)
    print(f"[*] SOVEREIGN EDGE BENCHMARK: TQ1_0 BASE-3 PACKING ({num_weights:,} WEIGHTS)")
    print("=" * 70)

    print("[1/5] Generating random ternary weights W in {-1, 0, 1}...")
    random.seed(42)
    raw_weights = [random.choice([-1, 0, 1]) for _ in range(num_weights)]
    
    raw_size_mb = sys.getsizeof(raw_weights) / (1024 * 1024)
    print(f"      -> Generated {len(raw_weights):,} weights.")
    print(f"      -> In-Memory Raw Python List Overhead: {raw_size_mb:.2f} MB")

    tracemalloc.start()
    
    print("\n[2/5] Benchmarking TQ1_0 Packing (1,000,000 weights -> 200,000 bytes)...")
    start_time = time.perf_counter()
    packed_bytes = TQ10Engine.pack_stream(raw_weights)
    pack_duration = time.perf_counter() - start_time
    
    _, pack_peak_ram = tracemalloc.get_traced_memory()
    tracemalloc.reset_peak()

    packed_size_kb = len(packed_bytes) / 1024
    pack_qps = num_weights / pack_duration
    pack_mbps = (len(packed_bytes) / (1024 * 1024)) / pack_duration

    print(f"      -> Packing Complete in: {pack_duration:.4f} seconds")
    print(f"      -> Packing Velocity    : {pack_qps:,.0f} weights/sec")
    print(f"      -> Throughput          : {pack_mbps:.2f} MB/s")
    print(f"      -> Compressed Size     : {packed_size_kb:.2f} KB (200,000 bytes)")
    print(f"      -> Peak RAM Delta      : {pack_peak_ram / 1024:.2f} KB")

    print("\n[3/5] Benchmarking TQ1_0 Unpacking (200,000 bytes -> 1,000,000 weights)...")
    start_time = time.perf_counter()
    unpacked_weights = TQ10Engine.unpack_stream(packed_bytes)
    unpack_duration = time.perf_counter() - start_time

    _, unpack_peak_ram = tracemalloc.get_traced_memory()
    tracemalloc.stop()

    unpack_qps = num_weights / unpack_duration

    print(f"      -> Unpacking Complete in: {unpack_duration:.4f} seconds")
    print(f"      -> Unpacking Velocity  : {unpack_qps:,.0f} weights/sec")
    print(f"      -> Peak RAM Delta      : {unpack_peak_ram / 1024 / 1024:.2f} MB")

    print("\n[4/5] Verifying Cryptographic Round-Trip Fixity...")
    is_exact_match = (raw_weights == unpacked_weights)
    drift = 0.0 if is_exact_match else 100.0
    
    print(f"      -> Round-Trip Match    : {is_exact_match}")
    print(f"      -> Replay State Drift  : {drift:.1f}%")
    assert is_exact_match, "[FATAL] Cryptographic verification mismatch!"

    print("\n[5/5] Stress-Testing Failure Modes & Error Registers...")
    
    # Test 1: Non-Ternary Injection
    try:
        TQ10Engine.pack_stream([2, 0, 1, -1, 0])
        print("      [!] FAILED: Non-ternary weight was not caught!")
    except ValueError as e:
        print(f"      [✓] Caught Non-Ternary Injection : {e}")

    # Test 2: Invalid Byte > 242
    try:
        TQ10Engine.unpack_byte(245)
        print("      [!] FAILED: Invalid byte > 242 was not caught!")
    except ValueError as e:
        print(f"      [✓] Caught Invalid Base-3 Byte   : {e}")

    # Test 3: Un-aligned Stream Length
    try:
        TQ10Engine.pack_stream([1, 0, -1])
        print("      [!] FAILED: Unaligned length was not caught!")
    except ValueError as e:
        print(f"      [✓] Caught Stream Alignment Error: {e}")

    print("\n" + "=" * 70)
    print("[✓] BENCHMARK COMPLETE: TQ1_0 ENGINE VERIFIED (1=1=1)")
    print("=" * 70)

if __name__ == "__main__":
    run_1M_benchmark(1_000_000)
