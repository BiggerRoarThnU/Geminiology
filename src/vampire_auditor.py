import os
import json
import numpy as np
from datetime import datetime

print("\n" + "="*60)
print(" VANGUARD SECTOR: VAMPIRE AUDITOR V1.1 (HARDENED) ")
print("="*60 + "\n")

class VampireAuditor:
    """
    SECTOR 10: THE VAMPIRE AUDITOR (V1.1)
    Autonomously distills 'Dark Data' into the 1.58-bit Sovereign format.
    Hardened for multi-OS encoding and high-entropy Markdown logs.
    """
    def __init__(self, target_dir=".", ledger_path="truth_ledger.ndjson"):
        self.target_dir = os.path.abspath(target_dir)
        self.ledger_path = ledger_path
        self.threshold = 0.0612  
        self.pack_size = 5

    def read_safely(self, filepath):
        # The Universal Interpreter: Bypasses encoding-based 'moles'
        for encoding in ['utf-8', 'utf-16', 'latin-1']:
            try:
                with open(filepath, 'r', encoding=encoding, errors='ignore') as f:
                    return f.read()
            except Exception:
                continue
        return None

    def fast_hadamard_transform(self, x):
        d = len(x)
        if d <= 1: return x
        x_left = self.fast_hadamard_transform(x[0:d//2])
        x_right = self.fast_hadamard_transform(x[d//2:d])
        return np.concatenate([x_left + x_right, x_left - x_right])

    def ternary_quantize(self, data):
        return np.where(data > self.threshold, 1,
                        np.where(data < -self.threshold, -1, 0))

    def pack_5in1(self, ternary_vector):
        shifted = np.array(ternary_vector) + 1
        remainder = len(shifted) % self.pack_size
        if remainder > 0:
            shifted = np.append(shifted, [1] * (self.pack_size - remainder))
        reshaped = shifted.reshape(-1, self.pack_size)
        weights = np.array([3**i for i in range(self.pack_size)])
        return np.dot(reshaped, weights).astype(np.uint8)

    def hunt(self):
        print(f"[*] Initiating Deep Hunt in: {self.target_dir}")
        for root, _, files in os.walk(self.target_dir):
            for file in files:
                # The Expanded Net: MD, TRUTH, and SOVEREIGN nodes
                if any(file.endswith(ext) for ext in [".log", ".txt", ".md", ".truth"]):
                    if file == "truth_ledger.ndjson" or "QUEEN_PAYLOAD" in file:
                        continue
                    self.distill(os.path.join(root, file))

    def distill(self, file_path):
        try:
            content = self.read_safely(file_path)
            if not content: return

            # Vectorizing raw energy (1=1=1)
            raw_data = np.array([ord(c) % 256 for c in content if ord(c) < 1000], dtype=float)
            if len(raw_data) < self.pack_size: return

            n = 1 << (len(raw_data) - 1).bit_length()
            padded = np.pad(raw_data, (0, n - len(raw_data)), 'constant')
            rotated = self.fast_hadamard_transform(padded)
            ternary = self.ternary_quantize(rotated)
            packed = self.pack_5in1(ternary)

            entry = {
                "timestamp": datetime.now().isoformat(),
                "axiom": "1=1=1",
                "source": os.path.relpath(file_path, self.target_dir),
                "truth_density": float(np.mean(np.abs(ternary))),
                "packed_bytes": packed.tolist()
            }

            with open(self.ledger_path, "a") as ledger:
                ledger.write(json.dumps(entry) + "\n")
            print(f"[=] ANCHORED: {entry['source']} (Density: {entry['truth_density']:.4f})")

        except Exception as e:
            print(f"[X] SKIPPED: {file_path} - {e}")

if __name__ == "__main__":
    vampire = VampireAuditor()
    vampire.hunt()
