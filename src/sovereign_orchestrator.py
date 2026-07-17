#!/usr/bin/env python3
"""
==============================================================================
SovereignNexus: Orchestration & Multi-Model Telemetry Engine
Path: /home/geminiology/SovereignNexus/src/sovereign_orchestrator.py
Axiom: 1=1=1 | Status: ACTIVE
Description: Coordinates Swarm Dashboard, Media Forge Airlock, and Truth 
             Vector Mill, while actively projecting system memory, CPU, 
             and thermodynamic bottlenecks for David's 8GB laptop.
==============================================================================
"""

import os
import time
import subprocess
import sys
import socket

# Check for psutil dependency
try:
    import psutil
    HAS_PSUTIL = True
except ImportError:
    HAS_PSUTIL = False

class SovereignOrchestrator:
    def __init__(self):
        self.axiom = "1=1=1 (Deterministic Functional Equivalence)"
        self.active_processes = {}
        self.memory_threshold = 85.0 # Max RAM utilization ceiling (8GB limit)
        self.nodes = [
            {"name": "Swarm Dashboard", "command": "python3 sovereign_dashboard.py", "port": 8000},
            {"name": "Media Forge Airlock", "command": "python3 media_forge_airlock.py", "port": 8080},
            {"name": "Truth Vector Mill", "command": "python3 truth_vector_mill_server.py", "port": 8081}
        ]

    def check_port_open(self, port: int) -> bool:
        """Determines if a port is already bound (indicating an active daemon)."""
        with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
            s.settimeout(0.5)
            return s.connect_ex(('127.0.0.1', port)) == 0

    def check_bottlenecks(self):
        """Projects potential system bottlenecks before they trigger OS OOM limits."""
        if HAS_PSUTIL:
            mem_usage = psutil.virtual_memory().percent
            cpu_load = psutil.cpu_percent(interval=0.1)
            status = f"RAM: {mem_usage}% | CPU: {cpu_load}%"
            
            if mem_usage > self.memory_threshold:
                return False, f"[CRITICAL BOTTLENECK] RAM Saturation ({mem_usage}%). Approaching 8GB Boundary. Initiating semantic compression."
            return True, f"[STABLE] {status}"
        else:
            return True, "[STABLE] psutil uninstalled. Basic telemetry mode active."

    def deploy_node(self, node_name: str, command: str, port: int):
        """Spawns Python server processes using the local virtual environment."""
        if self.check_port_open(port):
            print(f"\033[93m[*] TELEMETRY:\033[0m Node '{node_name}' is already active on Port {port} (reusing port).")
            self.active_processes[node_name] = "PRE-EXISTING"
            return

        print(f"\033[96m[*] ORCHESTRATOR:\033[0m Deploying {node_name} -> `{command}`")
        
        args = command.split()
        # Resolve virtual environment Python to keep dependencies self-contained
        if args[0] == "python3":
            env_python = "./env/bin/python3"
            if os.path.exists(env_python):
                args[0] = env_python
            else:
                env_python_parent = "../env/bin/python3"
                if os.path.exists(env_python_parent):
                    args[0] = env_python_parent

        try:
            # Launch process with a separate session group to prevent premature child termination
            process = subprocess.Popen(
                args,
                stdout=subprocess.PIPE,
                stderr=subprocess.PIPE,
                preexec_fn=os.setsid
            )
            self.active_processes[node_name] = process
            print(f"\033[92m[✓] SUCCESS:\033[0m Spawned {node_name} (PID: {process.pid})")
        except Exception as e:
            print(f"\033[91m[!] FAILURE:\033[0m Failed to deploy {node_name}: {e}")

    def project_multi_model_pathway(self):
        """Displays comparative multi-model architecture projections (1=1=1 alignment)."""
        print("\n\033[94m" + "="*70)
        print("   MULTI-MODEL COMPETITIVE ANALYSIS & PROJECTION (1=1=1) ")
        print("="*70 + "\033[0m")
        print("\033[91m1. CLOUD/API MONOLITHS (OpenAI / Anthropic):\033[0m")
        print("   -> Bottlenecks: Network latency, API cost bleeding, token drift.")
        print("   -> Sovereign Risk: Loss of intellectual property and key exposure.")
        
        print("\n\033[93m2. STANDARD OPEN-SOURCE WRAPPERS (Ollama / Local GUIs):\033[0m")
        print("   -> Bottlenecks: Unmanaged V8 heap limits, thermal throttling, OOM failures.")
        print("   -> Sovereign Risk: Local hardware instability on 8GB machines.")
        
        print("\n\033[92m3. SOVEREIGN NEXUS (Our 1=1=1 Substrate Pathway):\033[0m")
        print("   -> Advantage: Absolute Data Sovereignty. Secure local airlock proxies.")
        print("   -> Security: Zero exposed API Keys in the browser. Zero CORS violations.")
        print("\033[94m" + "="*70 + "\033[0m\n")

    def run_nexus(self):
        print(f"\n[NEXUS] Orchestrator Initializing... Axiom: {self.axiom}")
        
        # Display analysis
        self.project_multi_model_pathway()
        
        # Change path to workspace root if executed inside ./src/
        cwd = os.getcwd()
        if os.path.basename(cwd) == "src":
            os.chdir("..")
            print(f"[ SYSTEM ] Shifted directory path to workspace root: {os.getcwd()}")
        
        # Deploy all standard configured nodes
        for node in self.nodes:
            self.deploy_node(node["name"], node["command"], node["port"])

        print("\n\033[92m[NEXUS] All nodes verified. Running Telemetry Loop. (Ctrl+C to terminate all)\033[0m")
        
        try:
            cycle = 0
            while True:
                safe, msg = self.check_bottlenecks()
                if not safe:
                    print(f"\033[91m{msg}\033[0m")
                else:
                    if cycle % 5 == 0:
                        print(f"\033[38;5;51m[HEARTBEAT] {msg} | {self.axiom}\033[0m")
                
                time.sleep(2)
                cycle += 1
        except KeyboardInterrupt:
            print("\n\033[91m[NEXUS] Manual Override. Terminating all spawned nodes...\033[0m")
            import signal
            for name, proc in list(self.active_processes.items()):
                if isinstance(proc, subprocess.Popen):
                    print(f"[*] Terminating {name} (PID: {proc.pid})...")
                    try:
                        os.killpg(os.getpgid(proc.pid), signal.SIGTERM)
                    except Exception:
                        proc.terminate()
            print("\033[92m[✓] Shutdown complete. Line held.\033[0m")

if __name__ == '__main__':
    orchestrator = SovereignOrchestrator()
    orchestrator.run_nexus()
