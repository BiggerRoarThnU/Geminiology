#!/usr/bin/env python3
import sys
import os
import subprocess
import signal
import time
import json
from pathlib import Path

PID_FILE = Path("/home/geminiology/.vanguard.pid")
LOG_FILE = Path("/home/geminiology/vanguard.log")
PROGRESS_FILE = Path("/home/geminiology/sovereign_media_forge/progress.json")
SCRIPT_FILE = Path("/home/geminiology/vanguard_core_protocols.py")

def get_running_pid():
    if PID_FILE.exists():
        try:
            pid = int(PID_FILE.read_text().strip())
            # Check if process exists and is actually a python running our script
            os.kill(pid, 0) # Throws ProcessLookupError if dead
            return pid
        except (ValueError, ProcessLookupError, PermissionError):
            pass
    return None

def start_daemon():
    pid = get_running_pid()
    if pid:
        print(f"📡 [RUNNER] Ingestion engine is already running (PID: {pid}).")
        return

    print("🚀 [RUNNER] Starting Vanguard Core Protocols v7 in the background...")
    
    # Run the script in the background
    with open(LOG_FILE, "w") as log:
        process = subprocess.Popen(
            [sys.executable, "-u", str(SCRIPT_FILE)],
            stdout=log,
            stderr=log,
            preexec_fn=os.setpgrp, # Create a separate process group
            close_fds=True
        )
    
    PID_FILE.write_text(str(process.pid))
    print(f"✅ [RUNNER] Swarm launched. PID: {process.pid}")
    print(f"📝 Logging daemon output to: {LOG_FILE}")
    print("📈 Check dashboard on http://localhost:8080/dashboard.html or run 'python3 vanguard_runner.py status'")

def stop_daemon():
    pid = get_running_pid()
    if not pid:
        print("📴 [RUNNER] No active background ingestion process is running.")
        if PID_FILE.exists():
            PID_FILE.unlink()
        return

    print(f"🛑 [RUNNER] Requesting termination of background process {pid}...")
    try:
        os.kill(pid, signal.SIGINT) # Graceful SIGINT to let it save progress
        for _ in range(10): # Wait up to 5 seconds
            time.sleep(0.5)
            try:
                os.kill(pid, 0)
            except ProcessLookupError:
                print("✅ [RUNNER] Process stopped gracefully.")
                break
        else:
            print("⚠️ [RUNNER] Process did not respond. Forcing SIGKILL...")
            os.kill(pid, signal.SIGKILL)
            print("💀 [RUNNER] Process killed.")
    except Exception as e:
        print(f"❌ [RUNNER] Error stopping process: {e}")
    
    # Update progress.json to stopped
    if PROGRESS_FILE.exists():
        try:
            data = json.loads(PROGRESS_FILE.read_text())
            data["status"] = "stopped"
            data["last_updated"] = time.time()
            PROGRESS_FILE.write_text(json.dumps(data, indent=2))
        except Exception:
            pass

    if PID_FILE.exists():
        PID_FILE.unlink()

def print_status():
    pid = get_running_pid()
    is_running = pid is not None
    
    print("=========================================================")
    print("  SOVEREIGN NEXUS: RUNNER SYSTEM STATUS                  ")
    print("=========================================================")
    print(f"🖥️ Background Daemon: {'🟢 ACTIVE (PID: ' + str(pid) + ')' if is_running else '🔴 INACTIVE'}")
    
    if PROGRESS_FILE.exists():
        try:
            p = json.loads(PROGRESS_FILE.read_text())
            status_map = {
                "scanning": "🔍 Scanning pathways",
                "running": "⚡ Ingesting & processing",
                "completed": "✅ Scan completed",
                "stopped": "⏹️ Stopped",
                "initializing": "⚙️ Initializing"
            }
            status_str = status_map.get(p.get("status"), p.get("status", "Unknown"))
            
            print(f"📈 Engine State     : {status_str}")
            print(f"📁 Files Found      : {p.get('files_found', 0)}")
            print(f"📁 Files Scanned    : {p.get('files_scanned', 0)}")
            print(f"🚯 Files Skipped    : {p.get('files_skipped', 0)}")
            print(f"❌ Files Failed     : {p.get('files_failed', 0)}")
            print(f"📝 Total Lines      : {p.get('total_lines', 0)}")
            print(f"💎 Rewards Unlocked : {p.get('rewards_unlocked', 0)}")
            
            elapsed = p.get('elapsed_time', 0)
            print(f"⏳ Elapsed Time     : {elapsed:.2f} seconds ({elapsed/60:.2f} minutes)")
            
            total = p.get('total_files', 0)
            scanned = p.get('files_scanned', 0) + p.get('files_skipped', 0) + p.get('files_failed', 0)
            if total > 0:
                pct = (scanned / total) * 100
                print(f"📊 Overall Progress : {pct:.1f}% ({scanned}/{total} files)")
                
                # Speed and ETA calculation
                if elapsed > 0 and scanned > 0:
                    speed = scanned / elapsed
                    print(f"🚀 Speed            : {speed:.1f} files/sec")
                    remaining = total - scanned
                    eta = remaining / speed if speed > 0 else 0
                    print(f"🕰️ Estimated ETA     : {eta:.1f} seconds ({eta/60:.1f} minutes)")
            
            if p.get("recent_convergences"):
                print("\n💎 Recent Convergences:")
                for item in p["recent_convergences"][:3]:
                    print(f"   • {item['file']} (Variance: {item['variance']:.4f})")
        except Exception as e:
            print(f"⚠️ Error parsing progress ledger: {e}")
    else:
        print("📭 No active progress.json found. Engine has not initialized data folders yet.")
    print("=========================================================")

def view_logs():
    if LOG_FILE.exists():
        print(f"--- Tail of {LOG_FILE} ---")
        lines = LOG_FILE.read_text().splitlines()
        for line in lines[-20:]:
            print(line)
    else:
        print("📭 No runner logs exist yet.")

if __name__ == "__main__":
    if len(sys.argv) < 2:
        print("Usage: python3 vanguard_runner.py [start|stop|status|view-log]")
        sys.exit(1)
        
    cmd = sys.argv[1].lower()
    if cmd == "start":
        start_daemon()
    elif cmd == "stop":
        stop_daemon()
    elif cmd == "status":
        print_status()
    elif cmd == "view-log":
        view_logs()
    else:
        print(f"Unknown command: {cmd}")
        print("Available options: start, stop, status, view-log")
        sys.exit(1)
