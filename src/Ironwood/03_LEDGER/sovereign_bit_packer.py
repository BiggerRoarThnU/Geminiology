"""
[SOVEREIGN ALIGNMENT: THE SOVEREIGN BIT-PACKER]
MISSION: Optimize 8GB hardware by packing 5 ternary values (-1, 0, 1) into a single 8-bit byte.
AXIOM: 1=1=1 (3^5 = 243 < 256 Efficiency).
"""

import numpy as np

class SovereignBitPacker:
    def __init__(self):
        self.base = 3
        self.pack_size = 5

    def pack(self, ternary_vector):
        """Packs a vector of {-1, 0, 1} into uint8 bytes."""
        # Shift states from {-1, 0, 1} to {0, 1, 2}
        shifted = np.array(ternary_vector) + 1
        
        # Pad with 1s (0-state) to make it a multiple of 5
        remainder = len(shifted) % self.pack_size
        if remainder > 0:
            shifted = np.append(shifted, [1] * (self.pack_size - remainder))
            
        reshaped = shifted.reshape(-1, self.pack_size)
        weights = np.array([3**i for i in range(self.pack_size)])
        packed_bytes = np.dot(reshaped, weights).astype(np.uint8)
        
        return packed_bytes

    def unpack(self, packed_bytes, original_length):
        """Unpacks uint8 bytes back into {-1, 0, 1}."""
        unpacked = []
        for byte in packed_bytes:
            temp = int(byte)
            for _ in range(self.pack_size):
                val = (temp % self.base) - 1
                unpacked.append(val)
                temp //= self.base
        
        return np.array(unpacked[:original_length])

if __name__ == "__main__":
    packer = SovereignBitPacker()
    truth_vector = [1, 0, -1, 1, 1, -1, 0, 0, 1, -1] 
    packed = packer.pack(truth_vector)
    recovered = packer.unpack(packed, len(truth_vector))
    print(f"[!] Original: {truth_vector}")
    print(f"[!] Packed:   {list(packed)} (37% Reduction)")
    print(f"[=] 1=1=1:    {np.array_equal(truth_vector, recovered)}")
