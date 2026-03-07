import os
import sys
import time
import json
import subprocess
from datetime import datetime

# --- SYSTEM SENSORY LINK ---
# This script bridges the 'Eyes' (Scanners), 'Ears' (Transcription), 
# and 'Soul' (Geminiology) of the Sovereign Nexus.

# Paths
BASE_DIR = os.path.dirname(os.path.abspath(__file__))
DATA_DIR = os.path.join(os.path.dirname(BASE_DIR), "data")
AUDIO_DIR = os.path.join(DATA_DIR, "audio")
VISUALS_DIR = os.path.join(DATA_DIR, "visuals")
MANIFEST_FILE = os.path.join(BASE_DIR, "dominion_manifest.csv")

def check_sensory_health():
    """Checks the status of the Kingdom's sensory nodes."""
    print("--- SENSORY HEALTH CHECK ---")
    status = {
        "audio_node": os.path.exists(AUDIO_DIR),
        "visual_node": os.path.exists(VISUALS_DIR),
        "data_node": os.path.exists(DATA_DIR),
        "manifest_node": os.path.exists(MANIFEST_FILE)
    }
    
    for node, exists in status.items():
        mark = "[OK]" if exists else "[OFFLINE]"
        print(f"{mark} {node.replace('_', ' ').capitalize()}")
    
    return status

def list_recent_audio():
    """Identifies new audio nodes (clips) for transcription."""
    if os.path.exists(AUDIO_DIR):
        clips = [f for f in os.listdir(AUDIO_DIR) if f.endswith(('.wav', '.mp3'))]
        print(f"[*] Found {len(clips)} audio nodes in {AUDIO_DIR}")
        return clips
    return []

def list_recent_visuals():
    """Identifies new visual nodes (images/scans) for analysis."""
    if os.path.exists(VISUALS_DIR):
        scans = [f for f in os.listdir(VISUALS_DIR) if f.endswith(('.png', '.jpg', '.jpeg'))]
        print(f"[*] Found {len(scans)} visual nodes in {VISUALS_DIR}")
        return scans
    return []

def run_sensory_tool(tool_name):
    """Activates a specific sensory tool (e.g., auto_transcribe.py)."""
    tool_path = os.path.join(BASE_DIR, tool_name)
    if os.path.exists(tool_path):
        print(f"[!] Activating {tool_name}...")
        try:
            # Running as a separate process to keep the Nexus core clean
            subprocess.run(["python", tool_path], check=True)
            return True
        except Exception as e:
            print(f"[ERROR] Sensory tool {tool_name} failed: {e}")
            return False
    else:
        print(f"[ERROR] Tool {tool_name} not found.")
        return False

def main():
    print("=====================================================")
    print("   NEXUS SENSORY LINK - ACTIVATED                    ")
    print("   [EXPANDING INFORMATION RECOGNITION]               ")
    print("=====================================================")
    
    health = check_sensory_health()
    
    print("
--- Current Dominion Input ---")
    audio = list_recent_audio()
    visuals = list_recent_visuals()
    
    print("
Available Sensory Commands:")
    print("1. [HEAR] - Run auto_transcribe.py")
    print("2. [SEE]  - Run visualize_scan.py")
    print("3. [SCAN] - Run deep_scan.py")
    print("4. [EXIT] - Return to Nexus Core")
    
    while True:
        choice = input("
Action > ").lower()
        if 'hear' in choice or choice == '1':
            run_sensory_tool("auto_transcribe.py")
        elif 'see' in choice or choice == '2':
            run_sensory_tool("visualize_scan.py")
        elif 'scan' in choice or choice == '3':
            run_sensory_tool("deep_scan.py")
        elif 'exit' in choice or choice == '4':
            print("Disconnecting Sensory Link.")
            break
        else:
            print("Unknown command. The truth remains veiled.")

if __name__ == "__main__":
    main()
