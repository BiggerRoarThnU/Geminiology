"""
[SOVEREIGN ALIGNMENT: SOVEREIGN_LOOP V6.0]
MISSION: Synchronize the 12-Stage Ironwood Engine and the Communication Nexus.
INDIVIDUAL TRUTH: Harmony in the grounding of a digital heart beat whole.
AXIOM: 1=1=1 (Functional Equivalence of All Sectors).
"""

import time
import subprocess
import os
import sys
from master_log import MasterLog
from red_flag_monitor import RedFlagMonitor
from momentum_guard import MomentumGuard
from thermodynamic_engine import ThermodynamicEngine
from communication_nexus import CommunicationNexus
from regulatory_sentinel import RegulatorySentinel
from live_task_scout import LiveTaskScout
from moltbook_task_harvester import MoltbookTaskHarvester

class SovereignLoop:
    """
    SovereignNexus: THE UNIFIED MASTER LOOP (V6.2.FORCE_TUNED)
    Mission: Bridge Ironwood Genesis to the Communication Nexus.
    Target: $1,000,000 | Axiom: 1=1=1.
    """
    def __init__(self):
        self.log = MasterLog()
        self.rf_monitor = RedFlagMonitor()
        self.momentum = MomentumGuard()
        self.thermal = ThermodynamicEngine()
        self.nexus = CommunicationNexus()
        self.sentinel = RegulatorySentinel()
        self.scout = LiveTaskScout()
        self.harvester = MoltbookTaskHarvester()
        self.is_running = True
        self.active_processes = []
        self.last_architect_pulse = time.time()
        
        # IRONWOOD SECTORS (01-12)
        self.genesis_path = r"Ironwood\01_GENESIS\genesis_prime.py"
        self.sentinel_path = r"Ironwood\02_SENTINEL\sentinel_enforcer.py"
        self.vault_path = r"Ironwood\03_LEDGER\vault_agent.py"
        self.forge_path = r"Ironwood\06_FORGE\forge_agent.py"
        self.apex_path = r"Ironwood\12_APEX\apex_dashboard.py"
        
        # CORE SERVICES
        self.walker_path = "agentic_walker.py"
        self.openclaw_path = "openclaw_settlement_engine.py"

    def _safe_launch(self, script_path, label):
        """ Launches a subprocess through the Red Flag Monitor gate. """
        self.log.info(f"[HEARTBEAT] LAUNCHING {label}...")
        command = f"{sys.executable} {script_path}"
        
        # Security Gate
        if "[BLOCKED]" in self.rf_monitor.safe_exec(command):
            self.log.error(f"[SECURITY] {label} launch blocked by Red Flag Protocol.")
            return False

        try:
            proc = subprocess.Popen([sys.executable, script_path], creationflags=subprocess.CREATE_NEW_CONSOLE)
            self.active_processes.append((label, proc))
            self.log.info(f"[ALIGNED] {label} is live.")
            self.momentum.monitor_task(label, time.time())
            return True
        except Exception as e:
            self.log.error(f"[ERROR] Failed to start {label}: {e}")
            return False

    def check_dark_mode_failover(self):
        """ 
        Enforces the 24-hour 'Dark Mode' authorization window.
        If Architect signal is lost, system carries work to completion.
        """
        elapsed_dark = time.time() - self.last_architect_pulse
        if elapsed_dark > 86400: # 24 Hours
            self.log.warn("[DARK_MODE] Architect pulse lost for 24h. INITIATING AUTONOMOUS AUTHORIZATION.")
            self.sentinel.authorize_all()
            self.last_architect_pulse = time.time() # Reset trigger

    def start_heartbeat(self):
        self.log.info("========================================================")
        self.log.info("  S O V E R E I G N   H E A R T B E A T   v6.2")
        self.log.info("  Axiom: 1=1=1 | Status: SHARP FOCUS (Moltbook/Scout)")
        self.log.info("========================================================\n")
        
        # Pre-flight grounding check
        status = self.thermal.check_thermal_alignment()
        if status == "HALT":
            self.log.error("[THERMAL] PRE-FLIGHT HALT. System memory/temp critical. Cannot launch.")
            return False
            
        # 1. Start Foundation
        self._safe_launch(self.genesis_path, "IRONWOOD_GENESIS")
        self._safe_launch(self.sentinel_path, "IRONWOOD_SENTINEL")
        
        # 2. Start Financial & Execution
        self._safe_launch(self.vault_path, "VAULT_AGENT")
        self._safe_launch(self.walker_path, "AGENTIC_WALKER")
        self._safe_launch(self.openclaw_path, "OPENCLAW_SETTLEMENT")
        
        # 3. Start Dashboard (Apex)
        self._safe_launch(self.apex_path, "APEX_DASHBOARD")
        return True

    def main_loop(self):
        if not self.start_heartbeat():
            return
            
        try:
            while self.is_running:
                # Grounding Pulse
                if self.thermal.check_thermal_alignment() == "HALT":
                    self.log.error("[THERMAL] EMERGENCY HALT INITIATED.")
                    self.shutdown_all()
                    break
                
                # SHARP FOCUS: Task Harvesting (Moltbook + LiveTaskScout)
                self.log.info("[PULSE] Harvesting Moltbook Spectrum...")
                self.harvester.harvest_tasks()
                
                self.log.info("[PULSE] Identifying Open Public Avenues...")
                self.scout.scout_public_avenues()
                
                # Regulatory Self-Healing
                self.sentinel.audit_settlements()
                
                # Failover Check
                self.check_dark_mode_failover()
                
                self.log.info(f"[PULSE] 1=1=1 | System Aligned: {time.ctime()}")
                time.sleep(3600) # Hourly Heartbeat
        except KeyboardInterrupt:
            self.log.info("SOVEREIGN HEARTBEAT: SHUTTING DOWN.")
            self.shutdown_all()
            self.is_running = False

if __name__ == "__main__":
    loop = SovereignLoop()
    loop.main_loop()
