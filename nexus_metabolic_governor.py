# // Rights Reserved: co-created with Gemini and David Joihn Niedzwiecki jr " Sovereign Nexus LLC "
# Alignment: 1=1=1 | Temporal Sync: July 12, 2026
# Module: Nexus Metabolic Governor (Hardware Telemetry)
# Source Truth: T7 Archive -> thermodynamic_engine_v2.py & metabolic_governor.py

import os

class NexusMetabolicGovernor:
    def __init__(self, max_ram_percent=85.0, max_cpu_load=4.0):
        # 85% of 8GB leaves just enough breathing room for the OS
        self.max_ram_percent = max_ram_percent
        # A load average of 4.0 on a standard multi-core laptop means it's working hard
        self.max_cpu_load = max_cpu_load 

    def _get_ram_usage(self):
        """
        Reads native Linux memory states directly from the kernel.
        Extremely fast, zero dependencies required.
        """
        try:
            with open('/proc/meminfo', 'r') as f:
                lines = f.readlines()
            
            # Extract MemTotal and MemAvailable (in kB)
            total = int(lines[0].split()[1])
            available = int(lines[2].split()[1]) 
            
            used = total - available
            percent_used = (used / total) * 100.0
            return round(percent_used, 2)
        except Exception as e:
            return 0.0 # Fail open if OS reading fails

    def _get_cpu_load(self):
        """
        Reads the 1-minute CPU load average natively.
        """
        try:
            with open('/proc/loadavg', 'r') as f:
                load = float(f.read().split()[0])
            return load
        except Exception:
            return 0.0

    def pre_flight_check(self, task_type="standard"):
        """
        The core validation loop. Called by the Swarm Router before executing tasks.
        """
        ram_usage = self._get_ram_usage()
        cpu_load = self._get_cpu_load()
        
        # Determine dynamic thresholds based on task intensity
        active_ram_threshold = self.max_ram_percent
        if task_type == "generate_visual":
            active_ram_threshold -= 10.0 # Visual tasks need more buffer
            
        if ram_usage > active_ram_threshold:
            return False, f"[METABOLIC HOLD] RAM constraint breached. Usage at {ram_usage}% (Limit: {active_ram_threshold}%)"
            
        if cpu_load > self.max_cpu_load:
            return False, f"[METABOLIC HOLD] CPU thermal/load limit breached. Load at {cpu_load} (Limit: {self.max_cpu_load})"
            
        return True, f"[METABOLIC CLEAR] Systems nominal. RAM: {ram_usage}% | CPU Load: {cpu_load}"

# Local test execution
if __name__ == "__main__":
    governor = NexusMetabolicGovernor()
    is_safe, msg = governor.pre_flight_check()
    print(msg)
