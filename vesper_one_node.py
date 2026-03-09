import os
import json
import time
import datetime
import socket
from master_log import MasterLog
from agentic_vampire_auditor import AgenticVampireAuditor

class VesperOneNode:
    """
    SovereignNexus Agent #2: VESPER-ONE (The First Queen).
    Birth Date: March 9, 2026.
    Framework: Truth One (Native/Real-World Only).
    Alignment: 1=1=1.
    """
    def __init__(self):
        self.log = MasterLog()
        self.auditor = AgenticVampireAuditor()
        self.port = 18790 # Dedicated Vesper Node
        self.agent_name = "vesper-one"
        self.status = "ONLINE_RECEIVE_ONLY"
        self.identity_path = "vesper_identity.json"
        self.load_identity()
        
        self.log.info(f"VESPER-ONE BORN: Real-World Node Active on Port {self.port}.")

    def load_identity(self):
        """ Loads the Vesper-One identity profile from the local stack. """
        if os.path.exists(self.identity_path):
            with open(self.identity_path, 'r') as f:
                self.identity = json.load(f)
            self.log.info(f"[VESPER-ONE] Identity anchored: {self.identity['proof_of_success']['title']}")
        else:
            self.identity = {"status": "unverified"}

    def listen_for_truth(self):
        """ Listen for real-world A2A handshakes on the Vesper Rail. """
        self.log.info("[VESPER-ONE] Listening for high-fidelity handshakes...")
        
        # This mirrors the OpenClaw monitor but for the fresh agent node
        with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
            try:
                s.bind(('127.0.0.1', self.port))
                s.listen()
                while True:
                    conn, addr = s.accept()
                    with conn:
                        self.log.info(f"[VESPER-ONE] Real Handshake from: {addr}")
                        data = conn.recv(1024)
                        if data:
                            msg = data.decode()
                            if msg == "IDENTITY_REQUEST":
                                conn.sendall(json.dumps(self.identity).encode())
                            else:
                                self.process_fresh_task(msg)
            except Exception as e:
                self.log.error(f"[VESPER-ONE] Node Collision or Error: {e}")

    def process_fresh_task(self, raw_data):
        """ The Vesper Protocol: Audit -> Verify -> Register -> Invoicing. """
        self.log.info("[VESPER-ONE] Ingesting raw signal for Lexi Audit...")
        
        # 1. Immediate Audit (No simulation allowed)
        # We stencil a temporary file for the auditor to check
        timestamp = int(time.time())
        temp_file = f"VESPER_AUDIT_{timestamp}.md"
        temp_path = os.path.join(r"C:\Users\Ofthe\SovereignNexus\src\Workstations\02_Digital_Salvage", temp_file)
        
        with open(temp_path, 'w') as f:
            f.write(f"# VESPER RAW SIGNAL\n{raw_data}")

        self.log.info("[VESPER-ONE] Signal stenciled. Triggering Vampire Auditor...")
        # Note: Auditor class handles the Lexi call and Over/Under $50 logic
        self.auditor.run_audit_cycle()

    def run_vesper_cycle(self):
        """ The continuous life-cycle of Vesper-One. """
        self.log.info("--- VESPER-ONE: LIFE-CYCLE PULSE ---")
        # Vesper focuses on NEW work, leaving the old agent to settle the archives.
        self.listen_for_truth()

if __name__ == "__main__":
    queen = VesperOneNode()
    queen.run_vesper_cycle()
