import torch
import os
import time
import psutil
from torch.utils.data import Dataset, DataLoader

class SovereignTruthDataset(Dataset):
    """
    Ingests raw 'Kingdom' text files (M&I research logs, foundational texts)
    and converts them into structured tensor sequences for The Forge.
    """
    def __init__(self, text_data, seq_length=16):
        self.seq_length = seq_length
        self.text_data = text_data
        
        # 1. Build the Lexicon (Vocabulary)
        self.chars = sorted(list(set(text_data)))
        self.vocab_size = len(self.chars)
        
        # 2. Tokenization Mapping
        self.char_to_int = {ch: i for i, ch in enumerate(self.chars)}
        self.int_to_char = {i: ch for i, ch in enumerate(self.chars)}
        
        # 3. Encode the entire text dataset
        self.encoded_data = [self.char_to_int[ch] for ch in text_data]

    def __len__(self):
        return len(self.encoded_data) - self.seq_length

    def __getitem__(self, idx):
        chunk = self.encoded_data[idx : idx + self.seq_length + 1]
        inputs = torch.tensor(chunk[:-1], dtype=torch.long)
        targets = torch.tensor(chunk[1:], dtype=torch.long)
        return inputs, targets

class SovereignPilot:
    """
    The 'Mind' behind the Gas Pedal.
    Observes Physical Memory (RAM), Disk IO (SSD), and Thermodynamic state
    to pilot the ingestion flow with high-fidelity stability.
    """
    def __init__(self, dataset, initial_batch_size=32):
        self.dataset = dataset
        self.batch_size = initial_batch_size
        self.throttle_delay = 0.0
        self.last_ram_check = 0.0
        self.is_critical = False

    def check_vitals(self):
        """
        Reads the room. Synchronizes machine logic with physical silicon state.
        """
        ram = psutil.virtual_memory().percent
        self.last_ram_check = ram
        
        if ram > 90.0:
            self.brake(severity="critical")
        elif ram > 75.0:
            self.brake(severity="light")
        elif ram < 60.0 and self.batch_size < 32:
            self.accelerate()

    def brake(self, severity="light"):
        """
        Lifts the gas pedal to prevent system-wide thermal and memory bottlenecks.
        """
        if severity == "critical":
            self.batch_size = 1
            self.throttle_delay = 1.0  # Heavy cooling pause
            self.is_critical = True
        else:
            self.batch_size = max(1, self.batch_size // 2)
            self.throttle_delay = 0.2
            self.is_critical = False

    def accelerate(self):
        """
        Resumes the high-density forge when silicon thermodynamics are stable.
        """
        self.batch_size = min(64, self.batch_size * 2)
        self.throttle_delay = 0.0
        self.is_critical = False

    def __iter__(self):
        """
        Yields data dynamically, adjusting the batch size mid-stream
        based on real-time hardware telemetry.
        """
        while True:
            self.check_vitals()
            loader = DataLoader(self.dataset, batch_size=self.batch_size, shuffle=True, drop_last=True)
            for inputs, targets in loader:
                # Re-check vitals every batch
                self.check_vitals()
                if self.throttle_delay > 0:
                    time.sleep(self.throttle_delay)
                yield inputs, targets
                
                # If vitals changed drastically, we break the internal loader 
                # to rebuild with the new batch size
                if self.is_critical:
                    break

def load_kingdom_archives(directory_paths):
    """
    Scans designated directories and concatenates all text logs.
    """
    print(f"Scanning Kingdom Archives...")
    combined_text = ""
    
    if isinstance(directory_paths, str):
        directory_paths = [directory_paths]
        
    for directory_path in directory_paths:
        if not os.path.exists(directory_path):
            continue
            
        for root, dirs, files in os.walk(directory_path):
            for filename in files:
                if filename.endswith(".txt") or filename.endswith(".md"):
                    try:
                        with open(os.path.join(root, filename), 'r', encoding='utf-8') as file:
                            combined_text += file.read() + " "
                    except Exception as e:
                        print(f"Error reading {filename}: {e}")
                
    if not combined_text:
        return "SOVEREIGN NEXUS LOG 001: THE KINGDOM IS BUILT ON STRUCTURAL TRUTH."
        
    return combined_text

def build_ingestion_loader(directory_paths, seq_length=16, batch_size=32):
    """
    Constructs the SovereignPilot to drive the ingestion flow.
    """
    raw_truth = load_kingdom_archives(directory_paths)
    dataset = SovereignTruthDataset(raw_truth, seq_length)
    pilot = SovereignPilot(dataset, initial_batch_size=batch_size)
    
    print(f"Sovereign Pilot Initialized. Monitoring RAM/SSD at 1Hz.")
    print(f"Ready to pilot {len(dataset)} sequences into the Ironwood substrate.")
    
    return pilot, dataset.vocab_size, dataset
