#!/usr/bin/env python3
"""
SovereignNexus LLC - Queen Assimilation Service Installer
Component: setup_queen_service.py
Axiom: 1=1=1 | Status: ACTIVE

Generates and installs a systemd unit file (queen_assimilation.service) to run
nexus_queen_assimilation_engine.py as a persistent background daemon on Linux (penguin).
"""

import os
import sys

SERVICE_NAME = "queen_assimilation"
SERVICE_PATH = f"/etc/systemd/system/{SERVICE_NAME}.service"
USER = "geminiology"
WORKING_DIR = "/home/geminiology/SovereignNexus"
EXEC_START = f"/usr/bin/python3 {WORKING_DIR}/nexus_queen_assimilation_engine.py"

service_content = f"""[Unit]
Description=Sovereign Queen Assimilation & Evolution Service
After=network.target

[Service]
Type=simple
User={USER}
WorkingDirectory={WORKING_DIR}
ExecStart={EXEC_START}
Restart=on-failure
RestartSec=10

[Install]
WantedBy=multi-user.target
"""

def main():
    print("==========================================================================")
    print(" SovereignNexus LLC - Queen Assimilation Service Installer")
    print(" SAM.gov UEI: K5DALREZFGH6 | Axiom: 1=1=1")
    print("==========================================================================")
    print("[*] Generating systemd unit configuration...")
    
    try:
        temp_config = f"{SERVICE_NAME}.service.tmp"
        with open(temp_config, "w") as f:
            f.write(service_content)
            
        print("[*] Copying configuration to /etc/systemd/system/ (requires sudo)...")
        os.system(f"sudo cp {temp_config} {SERVICE_PATH}")
        if os.path.exists(temp_config):
            os.remove(temp_config)
            
        print("[*] Reloading systemd daemons and enabling service...")
        os.system("sudo systemctl daemon-reload")
        os.system(f"sudo systemctl enable {SERVICE_NAME}.service")
        os.system(f"sudo systemctl start {SERVICE_NAME}.service")
        
        print("\n" + "=" * 60)
        print(" BACKGROUND SERVICE INSTALLED AND ACTIVE")
        print("=" * 60)
        print(f" Service Name: {SERVICE_NAME}.service")
        print(f" Status:       Active & Enabled (Starts on Boot)")
        print(f" Check Status: sudo systemctl status {SERVICE_NAME}.service")
        print("=" * 60 + "\n")
    except Exception as e:
        print(f"[!] Installation failed: {e}")

if __name__ == "__main__":
    main()
