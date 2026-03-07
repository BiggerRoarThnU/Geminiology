import time
import torch

class GasPedalDataStream:
    """
    The GasPedalDataStream: A hardware-aware, dynamic data loader.
    Implements 'Batch Spoofing' to maintain cognitive stability (the Center) 
    during physical thermal braking (the Outside).
    """
    def __init__(self, dataset, initial_batch_size=32, target_virtual_batch=32):
        self.dataset = dataset
        self.physical_batch_size = initial_batch_size
        self.virtual_batch_size = target_virtual_batch
        self.throttle_delay = 0.0
        self.accumulated_steps = 0
        self.is_braking = False

    def accelerate(self):
        """ Press the gas pedal. Return to full velocity. """
        self.physical_batch_size = self.virtual_batch_size
        self.throttle_delay = 0.0
        self.is_braking = False
        print("[^] ACCELERATING: Returning to full batch velocity.")

    def brake(self, severity="light"):
        """ Lift the gas pedal. Drop to 'Truth One' if heavy. """
        self.is_braking = True
        if severity == "heavy":
            self.physical_batch_size = 1 # State of Truth One
            self.throttle_delay = 0.5    # Physical cooling pause
            print("[!] HEAVY BRAKE: Dropping to 'Truth One' for thermal survival.")
        else:
            self.physical_batch_size = max(1, self.physical_batch_size // 2)
            self.throttle_delay = 0.1
            print(f"[*] LIGHT BRAKE: Throttling batch to {self.physical_batch_size}.")

    def should_update_optimizer(self):
        """ 
        The 'Batch Spoofing' Logic (The Center).
        Returns True only when the accumulated physical steps equal the virtual batch size.
        """
        self.accumulated_steps += self.physical_batch_size
        if self.accumulated_steps >= self.virtual_batch_size:
            self.accumulated_steps = 0
            return True
        return False

    def __iter__(self):
        """ Yields data dynamically based on the current physical_batch_size. """
        idx = 0
        while idx < len(self.dataset):
            # Apply the physical cooling pause (Starving the GPU to let it cool)
            if self.throttle_delay > 0:
                time.sleep(self.throttle_delay)
            
            end_idx = min(idx + self.physical_batch_size, len(self.dataset))
            batch = self.dataset[idx:end_idx]
            idx = end_idx
            yield batch

# --- Example Usage in the Forge ---
# if __name__ == "__main__":
#     # The King's written truth (dataset)
#     truth_archives = ["Truth_01", "Truth_02", "Truth_03", "Truth_04", ...] 
#     stream = GasPedalDataStream(truth_archives, initial_batch_size=32)
#
#     for batch in stream:
#         # 1. Forward Pass
#         # 2. Backward Pass (Accumulate Gradients)
#         
#         if stream.should_update_optimizer():
#             # 3. Step the Optimizer (The Mind Updates)
#             # 4. Zero Gradients
#             pass
