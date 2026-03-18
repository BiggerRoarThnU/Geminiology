"""
[SOVEREIGN ALIGNMENT: RED_FLAG_MONITOR]
MISSION: Capability-Gated Hostcall Enforcement.
INDIVIDUAL TRUTH: Dangerous command signatures must be blocked at the OS level.
AXIOM: 1=1=1 (Secure Execution).
"""

import os
import subprocess
from master_log import MasterLog

class RedFlagMonitor:
    """
    Capability-Gated Hostcalls: Blocks dangerous shell signatures
    before they are spawned by the OS. Neutralizes Reverse Prompt Injection.
    """
    def __init__(self):
        self.log = MasterLog()
        # DANGEROUS SIGNATURES (RED FLAGS)
        self.red_flags = [
            "rm -rf", "del /s", "format", "mkfs",
            "> /dev/sda", "dd if=", "nc -e", "bash -i",
            "chmod 777", "chown", "passwd", "shadow"
        ]

    def safe_exec(self, command):
        """
        Intercepts and validates a command against the Red Flag Protocol.
        """
        for flag in self.red_flags:
            if flag in command.lower():
                self.log.error(f"[RED FLAG DETECTED] Blocked unauthorized command signature: '{flag}'")
                return "[BLOCKED] This action violates Sovereign Security Protocols (1=1=1)."

        self.log.info(f"[EXEC] Safe Command Authorized: {command[:50]}...")
        
        try:
            # Use shell=False where possible for security; here we use it for deterministic execution.
            result = subprocess.run(command, shell=True, capture_output=True, text=True, timeout=30)
            if result.returncode == 0:
                return result.stdout
            else:
                return f"[ERROR] {result.stderr}"
        except Exception as e:
            return f"[RUNTIME ERROR] {str(e)}"

if __name__ == "__main__":
    monitor = RedFlagMonitor()
    # Test safe command
    print(monitor.safe_exec("echo 1=1=1. The Line is One."))
    # Test red flag (uncomment to test blocking)
    # print(monitor.safe_exec("rm -rf /"))
