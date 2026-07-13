import os
import time
import json
import random

try:
    import psutil
except ImportError:
    print("[!] psutil required for hardware telemetry. Run: pip install psutil")
    psutil = None

class SovereignMindThrottle:
    """
    Synthesized from the 7-Step 'AI Mind Drives Hardware Throttle' Plan.
    Acts as a self-regulating, hardware-aware throttle driving the system.
    """
    def __init__(self, base_batch_size=32, max_temp=85.0, cpu_load_limit=80.0):
        self.current_batch_size = base_batch_size
        self.max_batch_size = base_batch_size
        self.min_batch_size = 1 # Truth One Density
        
        # Symbolic Grounding Limits
        self.max_temp = max_temp
        self.cpu_load_limit = cpu_load_limit
        
        self.state = "NOMINAL" # States: NOMINAL, BRAKING, ACCELERATING, CRITICAL

    def get_hardware_telemetry(self):
        """Pulls physical hardware metrics to feed the Symbolic Logic Gate."""
        if not psutil:
            return {"cpu_load": 50.0, "temp": 45.0} # Mock data if library missing
            
        load = psutil.cpu_percent(interval=0.1)
        temp = 45.0 # Default fallback
        try:
            # Attempt to read Linux thermal zones
            temps = psutil.sensors_temperatures()
            if temps and 'coretemp' in temps:
                temp = temps['coretemp'][0].current
        except Exception:
            pass # Fallback to 45.0 if sensors are unavailable on ChromeOS VM
            
        return {"cpu_load": load, "temp": temp}

    def predictive_complexity_gate(self, upcoming_files):
        """
        Dynamic Routing Network and Predictive Capabilities.
        Analyzes the upcoming dataset complexity *before* ingestion.
        """
        complexity_score = 0
        for file in upcoming_files:
            if file.endswith('.pdf') or file.endswith('.json'):
                complexity_score += 5 # Heavy processing required
            else:
                complexity_score += 1 # Standard text
                
        return complexity_score

    def evaluate_and_shift_gears(self, upcoming_files):
        """
        Evaluates hardware state and predictive load 
        to trigger .accelerate() or .brake() autonomously.
        """
        telemetry = self.get_hardware_telemetry()
        complexity = self.predictive_complexity_gate(upcoming_files)
        
        # Explicit, unbreakable symbolic logic override
        if telemetry['temp'] >= self.max_temp or telemetry['cpu_load'] >= self.cpu_load_limit:
            self.brake(force=True, reason=f"THERMAL SPIKE ({telemetry['temp']}°C / {telemetry['cpu_load']}% Load)")
            return

        # Predictive Braking
        if complexity > 50 and self.current_batch_size > 4:
            self.brake(force=False, reason=f"HIGH COMPLEXITY DATASET DETECTED (Score: {complexity})")
            return

        # Safe to Accelerate
        if telemetry['temp'] < (self.max_temp - 15) and telemetry['cpu_load'] < 50:
            self.accelerate()

    def brake(self, force=False, reason=""):
        """Reduces batch size to protect hardware."""
        if force:
            self.current_batch_size = self.min_batch_size
            self.state = "CRITICAL_BRAKE"
            print(f"\n[🛑 SYMBOLIC OVERRIDE] HARD BRAKE ENGAGED! {reason}")
            print(f"[!] Batch size dropped to TRUTH ONE ({self.min_batch_size}). Waiting for cooldown...")
            time.sleep(5) # Forced cooling period
        else:
            self.current_batch_size = max(self.min_batch_size, self.current_batch_size // 2)
            self.state = "BRAKING"
            print(f"[\033[93m⚠️ PREDICTIVE BRAKE\033[0m] Slowing ingestion. {reason}. New Batch Size: {self.current_batch_size}")

    def accelerate(self):
        """Increases batch size for maximum efficiency when safe."""
        if self.current_batch_size < self.max_batch_size:
            self.current_batch_size = min(self.max_batch_size, self.current_batch_size * 2)
            self.state = "ACCELERATING"
            print(f"[\033[92m🚀 ACCELERATING\033[0m] Hardware nominal. Increasing velocity. New Batch Size: {self.current_batch_size}")

    def extract_truth_one_density(self, file_path):
        """
        Optimize Ingestion.
        When running at batch size 1 due to thermal limits, maximize value
        by extracting high-density Subject-Predicate-Object (SPO) triples.
        """
        print(f"    [🔍 EXTRACTING SPO TRIPLES] Maximizing token density for: {os.path.basename(file_path)}")
        # Simulated extraction of dense knowledge
        return {"file": file_path, "status": "Dense Truth Anchored"}

    def run_gas_pedal_stream(self, file_list):
        """
        The Mechanical Throttle Implementation.
        Iterates through the data while continuously adjusting the throttle.
        """
        print("\n=== INITIATING NEURO-SYMBOLIC GAS PEDAL STREAM ===")
        total_files = len(file_list)
        idx = 0
        
        while idx < total_files:
            # Look ahead to predict load
            upcoming_batch = file_list[idx:idx + self.current_batch_size]
            
            # The Mind evaluates and shifts gears
            self.evaluate_and_shift_gears(upcoming_batch)
            
            # Execute Ingestion
            print(f"[*] Ingesting batch of {len(upcoming_batch)} files... (Status: {self.state})")
            
            if self.current_batch_size == self.min_batch_size:
                self.extract_truth_one_density(upcoming_batch[0])
            
            time.sleep(1) # Simulated processing time
            idx += len(upcoming_batch)
            
        print("=== STREAM COMPLETE. HARDWARE SECURE. ===")

if __name__ == "__main__":
    # Generate a mock list of 100 files with varying complexities
    mock_files = [f"doc_{i}.txt" if random.random() > 0.2 else f"heavy_data_{i}.pdf" for i in range(100)]
    
    throttle_engine = SovereignMindThrottle(base_batch_size=16)
    throttle_engine.run_gas_pedal_stream(mock_files)
