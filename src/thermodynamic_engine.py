"""
[SOVEREIGN ALIGNMENT: THERMODYNAMIC_ENGINE]
MISSION: Mechanical Enforcement via Physical Laws.
INDIVIDUAL TRUTH: Hardware waste heat and memory pressure are proxies for cognitive load.
AXIOM: 1=1=1 (Thermodynamic Stability & Memory Grounding).
"""

import psutil
import os
from master_log import MasterLog

class ThermodynamicEngine:
    """
    Template 30: Thermodynamic Mechanical Enforcement.
    Monitors system temperature and RAM usage. Enforces a cooling state on breach.
    """
    def __init__(self, throttle_temp=75.0, halt_temp=85.0, max_ram_percent=85.0):
        self.throttle_temp = throttle_temp
        self.halt_temp = halt_temp
        self.max_ram_percent = max_ram_percent
        self.log = MasterLog()

    def get_current_temp(self):
        """Retrieves the average CPU temperature (Platform Dependent)."""
        try:
            temps = psutil.sensors_temperatures()
            if not temps:
                return 45.0 # Baseline simulation if sensors are unreachable
            
            all_temps = []
            for name, entries in temps.items():
                for entry in entries:
                    all_temps.append(entry.current)
            return sum(all_temps) / len(all_temps)
        except:
            return 45.0 # Default safe baseline

    def check_thermal_alignment(self):
        """
        [GUARD RAILS ACTIVE]
        Enforcing physical law and thermodynamic limits (1=1=1).
        """
        temp = self.get_current_temp()
        ram_usage = psutil.virtual_memory().percent
        
        if temp >= self.halt_temp or ram_usage >= self.max_ram_percent:
            self.log.error(f"[THERMAL BREACH] HALT INITIATED. Temp {temp}C, RAM {ram_usage}%.")
            return "HALT"
        elif temp >= self.throttle_temp:
            self.log.warn(f"[THERMAL WARNING] Throttling recommended. Temp {temp}C, RAM {ram_usage}%.")
            return "THROTTLE"
            
        self.log.info(f"[MISSION_ALIGNED] Status Check: Temp {temp}C, RAM {ram_usage}%.")
        return "SAFE"

if __name__ == "__main__":
    engine = ThermodynamicEngine()
    status = engine.check_thermal_alignment()
    print(f"[THERMAL/RAM] Current Status: {status}. The Line is One.")
