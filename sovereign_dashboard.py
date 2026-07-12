#!/usr/bin/env python3
"""
==============================================================================
SovereignNexus: APEX Duality Dashboard
Component: sovereign_dashboard.py
Axiom: 1=1=1 | Status: COMPATIBLE WITH LINUX & CHROMEOS
Description: Self-contained HTTP API & Web Dashboard visualizing memory cores, 
             file drift metrics, agent swarm activity, and trinary logic simulations.
==============================================================================
"""

import os
import sys
import json
import time
import sqlite3
import hashlib
import subprocess
from http.server import BaseHTTPRequestHandler, HTTPServer
from socketserver import ThreadingTCPServer
from nexus_swarm_router import NexusSwarmRouter

swarm_router = NexusSwarmRouter()

DB_PATH = "/home/geminiology/sovereign_memory.db"
GENESIS_HASH = "289706b29def9cc2d40bb88ca5368bc899b70c6ab7fd08ddef3110918ec7ce8b"

LEDGER_PATHS = {
    "Node 1 Core": "/home/geminiology/SovereignNexus/truth_ledger.ndjson",
    "Source Directory": "/home/geminiology/SovereignNexus/src/truth_ledger.ndjson",
    "Home Mirror": "/home/geminiology/truth_ledger.ndjson"
}

AGENTS_METADATA = [
    {"id": 1, "name": "Anchor Agent", "role": "Establishes baseline coordinate structures.", "status": "ALIGNED"},
    {"id": 2, "name": "Thermometer Agent", "role": "Monitors active CPU thermal sensors.", "status": "ACTIVE"},
    {"id": 3, "name": "Synthesizer Agent", "role": "Bridges legacy formats into JSON structures.", "status": "IDLE"},
    {"id": 4, "name": "Auditor Agent", "role": "Runs regex firewall to purge data noise.", "status": "ACTIVE"},
    {"id": 5, "name": "Scout Agent", "role": "Controls throttled T7 ingestion pipeline.", "status": "SLEEP_WALK"},
    {"id": 6, "name": "Bio-Sync Agent", "role": "Verifies data matches creator's intent.", "status": "ALIGNED"},
    {"id": 7, "name": "Archivist Agent", "role": "Compresses data into high-density storage.", "status": "SLEEP_WALK"},
    {"id": 8, "name": "Discovery Lens", "role": "Scans local workspaces for new active records.", "status": "IDLE"},
    {"id": 9, "name": "Astrolabe Agent", "role": "Calculates semantic routing orientations.", "status": "ACTIVE"},
    {"id": 10, "name": "Gatekeeper Agent", "role": "Enforces zero-trust authentication protocols.", "status": "ACTIVE"},
    {"id": 11, "name": "Architect Agent", "role": "Synchronizes multithreaded harmony states.", "status": "ALIGNED"},
    {"id": 12, "name": "Vanguard Master", "role": "Oversees active background swarm coordination.", "status": "ACTIVE"},
    {"id": 13, "name": "Royal Seal", "role": "Validates cryptographic signatures of nodes.", "status": "IDLE"},
    {"id": 14, "name": "Relic Reader", "role": "Parses historically archived documents.", "status": "IDLE"},
    {"id": 15, "name": "Holographic Library", "role": "Handles multidimensional indices.", "status": "IDLE"},
    {"id": 16, "name": "Vector Forge", "role": "Generates data skyscrapers and graphs.", "status": "ACTIVE"},
    {"id": 17, "name": "Retrieval Engine", "role": "Performs fast search in local vector DBs.", "status": "ACTIVE"},
    {"id": 18, "name": "Grand Archivist", "role": "Manages deep cold-storage indices.", "status": "SLEEP_WALK"},
    {"id": 19, "name": "Sovereign Interface", "role": "Bridges API communication endpoints.", "status": "ACTIVE"},
    {"id": 20, "name": "Synthesis Engine", "role": "Collates multiple agent outputs.", "status": "IDLE"},
    {"id": 21, "name": "Queen Execution Core", "role": "Enforces deterministic Ollama models.", "status": "ACTIVE"},
    {"id": 22, "name": "Grand Cartographer", "role": "Maps active network topologies.", "status": "ALIGNED"},
    {"id": 23, "name": "Sovereign Injector", "role": "Feeds values to localized subprocesses.", "status": "IDLE"},
    {"id": 24, "name": "Log Agent", "role": "Monitors internal debug logs for anomalies.", "status": "ACTIVE"}
]

# Cache dictionary for hashes to prevent CPU hogging on heavy files
hash_cache = {}

def get_file_md5_and_sha256(filepath):
    """Calculates size, line count, and SHA256 of files safely, using cache if unchanged."""
    if not os.path.exists(filepath):
        return {"exists": False}
    
    mtime = os.path.getmtime(filepath)
    size_bytes = os.path.getsize(filepath)
    size_mb = size_bytes / (1024 * 1024)
    
    # Check cache
    cache_entry = hash_cache.get(filepath)
    if cache_entry and cache_entry["mtime"] == mtime and cache_entry["size"] == size_bytes:
        return cache_entry["data"]
        
    try:
        line_count = 0
        sha256_hash = hashlib.sha256()
        with open(filepath, "rb") as f:
            for chunk in iter(lambda: f.read(65536), b""):
                sha256_hash.update(chunk)
                line_count += chunk.count(b'\n')
        
        file_hash = sha256_hash.hexdigest()
        data = {
            "exists": True,
            "size_mb": round(size_mb, 2),
            "line_count": line_count,
            "hash": file_hash,
            "mtime": time.ctime(mtime),
            "drifted": file_hash != GENESIS_HASH
        }
        
        # Save cache
        hash_cache[filepath] = {
            "mtime": mtime,
            "size": size_bytes,
            "data": data
        }
        return data
    except Exception as e:
        return {"exists": True, "error": str(e), "size_mb": round(size_mb, 2)}

def get_system_telemetry():
    """Parses Linux system stats for memory, CPU load, and temperature."""
    # CPU Load
    cpu_load = "N/A"
    try:
        with open("/proc/loadavg", "r") as f:
            cpu_load = f.read().split()[0]
    except:
        pass

    # RAM
    ram_usage = "N/A"
    try:
        with open("/proc/meminfo", "r") as f:
            lines = f.readlines()
        mem_info = {}
        for line in lines:
            parts = line.split(":")
            if len(parts) == 2:
                mem_info[parts[0].strip()] = int(parts[1].replace("kB", "").strip())
        total_gb = mem_info.get("MemTotal", 8388608) / (1024 * 1024)
        free_gb = mem_info.get("MemAvailable", mem_info.get("MemFree", 0)) / (1024 * 1024)
        used_gb = total_gb - free_gb
        ram_usage = f"{used_gb:.2f} GB / {total_gb:.2f} GB"
    except Exception as e:
        ram_usage = f"Error: {e}"

    # CPU Temperature
    temp_celsius = 35.0 # Fallback
    try:
        thermal_dir = "/sys/class/thermal"
        if os.path.exists(thermal_dir):
            for tz in os.listdir(thermal_dir):
                if tz.startswith("thermal_zone"):
                    with open(os.path.join(thermal_dir, tz, "temp"), "r") as f:
                        raw_temp = float(f.read().strip())
                        if raw_temp > 1000:
                            raw_temp = raw_temp / 1000.0
                        if raw_temp > temp_celsius:
                            temp_celsius = raw_temp
    except:
        pass

    # Active Python processes (Simulating Agent activity)
    running_scripts = []
    try:
        output = subprocess.check_output(["ps", "-ef"]).decode('utf-8', errors='ignore')
        for line in output.split('\n'):
            if 'python' in line.lower() and 'sovereign_dashboard.py' not in line:
                parts = line.split()
                if len(parts) > 7:
                    cmd_part = " ".join(parts[7:])
                    running_scripts.append(os.path.basename(cmd_part.split()[-1]))
    except:
        pass

    # Determine metabolic throttling status
    governor = "STABLE"
    if temp_celsius > 70.0:
        governor = "CRITICAL THROTTLE"
    elif temp_celsius > 55.0:
        governor = "ACTIVE MITIGATION"

    return {
        "cpu_load": cpu_load,
        "ram_usage": ram_usage,
        "temperature": f"{temp_celsius:.1f} °C",
        "governor_status": governor,
        "running_scripts": running_scripts
    }

def get_db_metrics():
    """Reads counts and logs from SQLite memory database."""
    metrics = {
        "exists": False,
        "prime_count": 0,
        "suspension_count": 0,
        "invariants_count": 0,
        "recent_prime": [],
        "recent_suspension": []
    }
    
    if not os.path.exists(DB_PATH):
        return metrics
        
    metrics["exists"] = True
    try:
        conn = sqlite3.connect(DB_PATH)
        conn.row_factory = sqlite3.Row
        c = conn.cursor()
        
        # Row counts
        metrics["prime_count"] = c.execute("SELECT count(*) FROM prime_ledger").fetchone()[0]
        metrics["suspension_count"] = c.execute("SELECT count(*) FROM suspension_gate").fetchone()[0]
        metrics["invariants_count"] = c.execute("SELECT count(*) FROM immutable_invariants").fetchone()[0]
        
        # Recent prime records
        rows = c.execute("SELECT id, timestamp, agent_id, content, sha256_hash, variance FROM prime_ledger ORDER BY id DESC LIMIT 5").fetchall()
        metrics["recent_prime"] = [dict(r) for r in rows]
        
        # Recent suspension records
        rows = c.execute("SELECT id, timestamp, agent_id, content, sha256_hash, variance FROM suspension_gate ORDER BY id DESC LIMIT 5").fetchall()
        metrics["recent_suspension"] = [dict(r) for r in rows]
        
        conn.close()
    except Exception as e:
        metrics["error"] = str(e)
    return metrics

def get_agent_script_by_id(agent_id):
    mapping = {
        1: "agent_01_anchor.py",
        2: "agent_02_thermometer.py",
        6: "agent_06_scribe.py",
        8: "agent_08_discovery_lens.py",
        9: "agent_09_astrolabe.py",
        10: "agent_10_gatekeeper.py",
        11: "agent_11_architect.py",
        12: "agent_12_vanguard_master.py",
        13: "agent_13_royal_seal.py",
        14: "agent_14_relic_reader.py",
        15: "agent_15_holographic_library.py",
        16: "agent_16_vector_forge.py",
        17: "agent_17_retrieval_engine.py",
        18: "agent_18_grand_archivist.py",
        19: "agent_19_sovereign_interface.py",
        20: "agent_20_synthesis_engine.py",
        21: "agent_21_queen_execution_core.py",
        22: "agent_22_grand_cartographer.py",
        23: "agent_23_sovereign_injector.py",
        24: "agent_24_log_agent.py"
    }
    return mapping.get(agent_id)

def trinary_eval(op, a, b=None):
    """Evaluates standard balanced ternary operations (-1, 0, 1)"""
    states = [-1, 0, 1]
    if a not in states or (b is not None and b not in states):
        return {"error": "Invalid trinary state input"}
        
    if op == "NOT":
        return {"result": -a, "label": trinary_label(-a)}
    elif op == "AND":
        res = min(a, b)
        return {"result": res, "label": trinary_label(res)}
    elif op == "OR":
        res = max(a, b)
        return {"result": res, "label": trinary_label(res)}
    elif op == "CONSENSUS":
        res = a if a == b else 0
        return {"result": res, "label": trinary_label(res)}
    return {"error": "Unknown operator"}

def trinary_label(val):
    if val == -1: return "False (-1)"
    if val == 0: return "Unknown (0)"
    if val == 1: return "True (1)"
    return "Aberration"

class ThreadingHTTPServer(ThreadingTCPServer, HTTPServer):
    pass

class DashboardHandler(BaseHTTPRequestHandler):
    def log_message(self, format, *args):
        # Silence standard HTTP request logging in the console to keep output tidy
        pass

    def do_GET(self):
        if self.path == '/':
            self.send_response(200)
            self.send_header('Content-Type', 'text/html')
            self.end_headers()
            self.wfile.write(HTML_TEMPLATE.encode('utf-8'))
        elif self.path == '/api/telemetry':
            self.send_json(get_system_telemetry())
        elif self.path == '/api/db':
            self.send_json(get_db_metrics())
        elif self.path == '/api/drift':
            drift_data = {}
            for name, filepath in LEDGER_PATHS.items():
                drift_data[name] = get_file_md5_and_sha256(filepath)
            self.send_json({
                "genesis_hash": GENESIS_HASH,
                "ledgers": drift_data
            })
        elif self.path == '/api/agents':
            # Dynamically mix active process status
            telemetry = get_system_telemetry()
            running = telemetry["running_scripts"]
            
            merged_agents = []
            for agent in AGENTS_METADATA:
                name_key = f"agent_{agent['id']:02d}"
                status = agent["status"]
                # If running process matches agent script pattern, set to ACTIVE
                for run_script in running:
                    if name_key in run_script.lower():
                        status = "ACTIVE"
                
                merged_agents.append({
                    "id": agent["id"],
                    "name": agent["name"],
                    "role": agent["role"],
                    "status": status
                })
            self.send_json(merged_agents)
        elif self.path == '/api/ledger':
            try:
                db_file = '/home/geminiology/SovereignNexus/nexus_checkpoints.db'
                if not os.path.exists(db_file):
                    self.send_json({"status": "SUCCESS", "ledger": []})
                    return
                conn = sqlite3.connect(f"file:{db_file}?mode=ro", uri=True)
                cursor = conn.cursor()
                cursor.execute('''
                    SELECT id, task_name, current_hash, signature 
                    FROM checkpoints 
                    ORDER BY id DESC LIMIT 5
                ''')
                blocks = cursor.fetchall()
                conn.close()

                ledger_data = [
                    {
                        "block": row[0],
                        "task": row[1],
                        "hash": row[2][:16] + "...",
                        "signature": row[3][:16] + "..."
                    } for row in blocks
                ]
                self.send_json({"status": "SUCCESS", "ledger": ledger_data})
            except Exception as e:
                self.send_json({"status": "ERROR", "message": f"Ledger error: {str(e)}"})
        else:
            self.send_error(404, 'Path not found')

    def do_POST(self):
        if self.path == '/api/swarm':
            content_length = int(self.headers['Content-Length'])
            post_data = self.rfile.read(content_length)
            try:
                payload = json.loads(post_data.decode('utf-8'))
                user_prompt = payload.get("prompt", "")
                if not user_prompt:
                    self.send_json({"error": "Missing 'prompt' parameter"})
                    return
                swarm_execution_log = swarm_router.execute_swarm(user_prompt)
                self.send_json({
                    "status": "Execution Complete",
                    "input_prompt": user_prompt,
                    "routing_topology": swarm_execution_log
                })
            except Exception as e:
                self.send_json({"error": f"Internal Server Error: {str(e)}"})
        elif self.path == '/api/trinary':
            content_length = int(self.headers['Content-Length'])
            post_data = json.loads(self.rfile.read(content_length).decode('utf-8'))
            op = post_data.get("op")
            a = int(post_data.get("a", 0))
            b = post_data.get("b")
            if b is not None:
                b = int(b)
            result = trinary_eval(op, a, b)
            self.send_json(result)
        elif self.path == '/api/run-agent':
            content_length = int(self.headers['Content-Length'])
            post_data = json.loads(self.rfile.read(content_length).decode('utf-8'))
            agent_id = int(post_data.get("agent_id", 0))
            input_data = post_data.get("input_data", "")
            
            script_name = get_agent_script_by_id(agent_id)
            if not script_name:
                self.send_json({"status": "error", "error": "Agent script not implemented or placeholder"})
                return
                
            script_path = os.path.join("/home/geminiology/SovereignNexus/src", script_name)
            if not os.path.exists(script_path):
                self.send_json({"status": "error", "error": f"Script file {script_name} does not exist in src/"})
                return
                
            try:
                result = subprocess.run(
                    [sys.executable, script_path],
                    input=input_data,
                    capture_output=True,
                    text=True,
                    timeout=10,
                    cwd="/home/geminiology/SovereignNexus/src"
                )
                self.send_json({
                    "status": "success" if result.returncode == 0 else "error",
                    "stdout": result.stdout,
                    "stderr": result.stderr,
                    "returncode": result.returncode
                })
            except subprocess.TimeoutExpired:
                self.send_json({"status": "error", "error": "Agent execution timed out (limit: 10s)"})
            except Exception as e:
                self.send_json({"status": "error", "error": f"Execution error: {str(e)}"})
        else:
            self.send_error(404, 'Path not found')

    def send_json(self, data):
        self.send_response(200)
        self.send_header('Content-Type', 'application/json')
        self.send_header('Access-Control-Allow-Origin', '*')
        self.end_headers()
        self.wfile.write(json.dumps(data).encode('utf-8'))

HTML_TEMPLATE = """<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Sovereign Nexus | Duality Dashboard</title>
    <link href="https://fonts.googleapis.com/css2?family=Outfit:wght@300;400;600;800&family=Courier+Prime&display=swap" rel="stylesheet">
    <style>
        :root {
            --bg-color: #0b0f19;
            --card-bg: #131926;
            --accent-cyan: #06b6d4;
            --accent-purple: #8b5cf6;
            --accent-emerald: #10b981;
            --accent-rose: #f43f5e;
            --text-main: #f3f4f6;
            --text-muted: #9ca3af;
            --border-glow: rgba(6, 182, 212, 0.15);
        }

        * {
            margin: 0;
            padding: 0;
            box-sizing: border-box;
        }

        body {
            font-family: 'Outfit', sans-serif;
            background-color: var(--bg-color);
            color: var(--text-main);
            overflow-x: hidden;
            line-height: 1.6;
        }

        header {
            padding: 1.5rem 2rem;
            background: linear-gradient(180deg, rgba(19, 25, 38, 0.8) 0%, rgba(11, 15, 25, 0) 100%);
            border-bottom: 1px solid rgba(255, 255, 255, 0.05);
            display: flex;
            justify-content: space-between;
            align-items: center;
            backdrop-filter: blur(10px);
            position: sticky;
            top: 0;
            z-index: 100;
        }

        .logo-section {
            display: flex;
            align-items: center;
            gap: 0.75rem;
        }

        .logo-icon {
            width: 12px;
            height: 12px;
            background-color: var(--accent-cyan);
            border-radius: 50%;
            box-shadow: 0 0 15px var(--accent-cyan);
            animation: pulse-glow 2s infinite ease-in-out;
        }

        h1 {
            font-size: 1.4rem;
            font-weight: 800;
            letter-spacing: 0.15em;
            background: linear-gradient(90deg, var(--accent-cyan), var(--accent-purple));
            -webkit-background-clip: text;
            -webkit-text-fill-color: transparent;
            text-transform: uppercase;
        }

        .axiom-badge {
            font-family: 'Courier Prime', monospace;
            padding: 0.25rem 0.75rem;
            border-radius: 4px;
            background: rgba(16, 185, 129, 0.1);
            border: 1px solid var(--accent-emerald);
            color: var(--accent-emerald);
            font-weight: bold;
            font-size: 0.9rem;
            letter-spacing: 0.05em;
        }

        main {
            max-width: 1600px;
            margin: 0 auto;
            padding: 2rem;
            display: flex;
            flex-direction: column;
            gap: 2rem;
        }

        /* GRID SYSTEM */
        .telemetry-row {
            display: grid;
            grid-template-columns: repeat(auto-fit, minmax(280px, 1fr));
            gap: 1.5rem;
        }

        .card {
            background-color: var(--card-bg);
            border: 1px solid rgba(255, 255, 255, 0.03);
            border-radius: 12px;
            padding: 1.5rem;
            box-shadow: 0 4px 20px rgba(0, 0, 0, 0.25);
            transition: all 0.3s cubic-bezier(0.4, 0, 0.2, 1);
            position: relative;
            overflow: hidden;
        }

        .card::before {
            content: '';
            position: absolute;
            top: 0;
            left: 0;
            width: 100%;
            height: 2px;
            background: linear-gradient(90deg, transparent, var(--accent-cyan), transparent);
            opacity: 0.5;
        }

        .card:hover {
            transform: translateY(-3px);
            border-color: rgba(6, 182, 212, 0.2);
            box-shadow: 0 8px 30px rgba(6, 182, 212, 0.05);
        }

        .card-title {
            font-size: 0.85rem;
            text-transform: uppercase;
            letter-spacing: 0.1em;
            color: var(--text-muted);
            margin-bottom: 0.5rem;
            font-weight: 600;
        }

        .card-value {
            font-size: 1.8rem;
            font-weight: 800;
            color: var(--text-main);
            font-family: 'Courier Prime', monospace;
        }

        .card-value.highlight-emerald { color: var(--accent-emerald); }
        .card-value.highlight-cyan { color: var(--accent-cyan); }
        .card-value.highlight-purple { color: var(--accent-purple); }

        .card-subtitle {
            font-size: 0.8rem;
            color: var(--text-muted);
            margin-top: 0.25rem;
        }

        /* DUALITY SECTIONS */
        .duality-grid {
            display: grid;
            grid-template-columns: 1fr 1fr;
            gap: 2rem;
        }

        @media (max-width: 1024px) {
            .duality-grid {
                grid-template-columns: 1fr;
            }
        }

        .duality-card {
            border: 1px solid rgba(139, 92, 246, 0.1);
            background: linear-gradient(145deg, #131926 0%, #15102a 100%);
        }

        .duality-card::before {
            background: linear-gradient(90deg, transparent, var(--accent-purple), transparent);
        }

        .duality-header {
            display: flex;
            justify-content: space-between;
            align-items: center;
            border-bottom: 1px solid rgba(255, 255, 255, 0.05);
            padding-bottom: 1rem;
            margin-bottom: 1rem;
        }

        .node-title {
            font-size: 1.2rem;
            font-weight: 800;
            color: #fff;
            letter-spacing: 0.05em;
        }

        .node-path {
            font-family: 'Courier Prime', monospace;
            background: rgba(0, 0, 0, 0.3);
            padding: 0.2rem 0.5rem;
            border-radius: 4px;
            font-size: 0.8rem;
            color: var(--accent-cyan);
            border: 1px solid rgba(6, 182, 212, 0.1);
            word-break: break-all;
        }

        .asset-list {
            margin-top: 1rem;
            display: flex;
            flex-direction: column;
            gap: 0.75rem;
        }

        .asset-item {
            background: rgba(255, 255, 255, 0.02);
            border-radius: 6px;
            padding: 0.75rem;
            border: 1px solid rgba(255, 255, 255, 0.03);
            display: flex;
            justify-content: space-between;
            align-items: center;
        }

        .asset-name {
            font-weight: 600;
            font-size: 0.9rem;
        }

        .asset-value {
            font-family: 'Courier Prime', monospace;
            font-size: 0.8rem;
            color: var(--text-muted);
        }

        /* DRIFT MATRIX */
        .drift-matrix {
            background-color: var(--card-bg);
            border-radius: 12px;
            padding: 2rem;
            border: 1px solid rgba(255, 255, 255, 0.03);
        }

        .section-header {
            margin-bottom: 1.5rem;
            display: flex;
            justify-content: space-between;
            align-items: center;
        }

        .section-title {
            font-size: 1.1rem;
            font-weight: 800;
            letter-spacing: 0.1em;
            text-transform: uppercase;
            display: flex;
            align-items: center;
            gap: 0.5rem;
        }

        .table-wrapper {
            overflow-x: auto;
        }

        table {
            width: 100%;
            border-collapse: collapse;
            text-align: left;
        }

        th {
            padding: 1rem;
            font-size: 0.8rem;
            text-transform: uppercase;
            letter-spacing: 0.05em;
            color: var(--text-muted);
            border-bottom: 1px solid rgba(255, 255, 255, 0.05);
        }

        td {
            padding: 1rem;
            border-bottom: 1px solid rgba(255, 255, 255, 0.03);
            font-size: 0.9rem;
        }

        tr:hover td {
            background-color: rgba(255, 255, 255, 0.01);
        }

        .status-badge {
            display: inline-block;
            padding: 0.15rem 0.5rem;
            border-radius: 4px;
            font-size: 0.75rem;
            font-weight: 800;
            letter-spacing: 0.05em;
            text-transform: uppercase;
            font-family: 'Courier Prime', monospace;
        }

        .status-badge.emerald {
            background: rgba(16, 185, 129, 0.15);
            color: var(--accent-emerald);
            border: 1px solid rgba(16, 185, 129, 0.2);
        }

        .status-badge.rose {
            background: rgba(244, 63, 94, 0.15);
            color: var(--accent-rose);
            border: 1px solid rgba(244, 63, 94, 0.2);
        }

        .status-badge.cyan {
            background: rgba(6, 182, 212, 0.15);
            color: var(--accent-cyan);
            border: 1px solid rgba(6, 182, 212, 0.2);
        }

        .status-badge.purple {
            background: rgba(139, 92, 246, 0.15);
            color: var(--accent-purple);
            border: 1px solid rgba(139, 92, 246, 0.2);
        }

        /* TRINARY LAB */
        .trinary-lab {
            display: grid;
            grid-template-columns: 1fr 2fr;
            gap: 2rem;
        }

        @media (max-width: 900px) {
            .trinary-lab {
                grid-template-columns: 1fr;
            }
        }

        .interactive-panel {
            background: rgba(0, 0, 0, 0.2);
            padding: 1.5rem;
            border-radius: 10px;
            border: 1px solid rgba(255, 255, 255, 0.03);
            display: flex;
            flex-direction: column;
            gap: 1.25rem;
        }

        .form-group {
            display: flex;
            flex-direction: column;
            gap: 0.5rem;
        }

        .form-label {
            font-size: 0.8rem;
            text-transform: uppercase;
            letter-spacing: 0.05em;
            color: var(--text-muted);
        }

        .trinary-buttons {
            display: grid;
            grid-template-columns: repeat(3, 1fr);
            gap: 0.5rem;
        }

        .trinary-btn {
            background: #1e293b;
            border: 1px solid rgba(255, 255, 255, 0.05);
            color: var(--text-main);
            padding: 0.5rem;
            border-radius: 6px;
            font-family: 'Courier Prime', monospace;
            cursor: pointer;
            transition: all 0.2s ease;
            font-weight: 800;
        }

        .trinary-btn:hover {
            background: #334155;
        }

        .trinary-btn.active {
            background: var(--accent-cyan);
            color: #000;
            border-color: var(--accent-cyan);
            box-shadow: 0 0 10px rgba(6, 182, 212, 0.3);
        }

        .trinary-btn.active[data-val="-1"] {
            background: var(--accent-rose);
            color: #fff;
            border-color: var(--accent-rose);
            box-shadow: 0 0 10px rgba(244, 63, 94, 0.3);
        }

        .trinary-btn.active[data-val="0"] {
            background: var(--text-muted);
            color: #000;
            border-color: var(--text-muted);
            box-shadow: 0 0 10px rgba(156, 163, 175, 0.3);
        }

        .trinary-btn.active[data-val="1"] {
            background: var(--accent-emerald);
            color: #000;
            border-color: var(--accent-emerald);
            box-shadow: 0 0 10px rgba(16, 185, 129, 0.3);
        }

        .select-op {
            background: #1e293b;
            border: 1px solid rgba(255, 255, 255, 0.05);
            color: var(--text-main);
            padding: 0.6rem;
            border-radius: 6px;
            font-family: 'Outfit', sans-serif;
            font-weight: 600;
            outline: none;
            cursor: pointer;
        }

        .result-panel {
            display: flex;
            align-items: center;
            justify-content: center;
            background: rgba(6, 182, 212, 0.02);
            border: 1px dashed rgba(6, 182, 212, 0.15);
            border-radius: 10px;
            flex-direction: column;
            padding: 2rem;
            gap: 0.5rem;
        }

        .result-title {
            font-size: 0.9rem;
            color: var(--text-muted);
            text-transform: uppercase;
            letter-spacing: 0.1em;
        }

        .result-val {
            font-size: 3rem;
            font-weight: 800;
            font-family: 'Courier Prime', monospace;
            color: var(--accent-cyan);
            text-shadow: 0 0 15px rgba(6, 182, 212, 0.4);
        }

        .result-desc {
            font-size: 1.1rem;
            font-weight: 600;
        }

        /* AGENT GRID */
        .agent-grid {
            display: grid;
            grid-template-columns: repeat(auto-fill, minmax(220px, 1fr));
            gap: 1.25rem;
        }

        .agent-card {
            background: var(--card-bg);
            border: 1px solid rgba(255, 255, 255, 0.02);
            border-radius: 10px;
            padding: 1rem;
            display: flex;
            flex-direction: column;
            justify-content: space-between;
            gap: 0.5rem;
            height: 100%;
        }

        .agent-header {
            display: flex;
            justify-content: space-between;
            align-items: flex-start;
        }

        .agent-id {
            font-family: 'Courier Prime', monospace;
            font-size: 0.75rem;
            background: rgba(255, 255, 255, 0.05);
            padding: 0.1rem 0.3rem;
            border-radius: 3px;
            color: var(--text-muted);
        }

        .agent-name {
            font-size: 0.95rem;
            font-weight: 600;
            margin-top: 0.25rem;
        }

        .agent-role {
            font-size: 0.75rem;
            color: var(--text-muted);
            min-height: 2.5rem;
        }

        /* MEMORY EXPLORER */
        .memory-explorer {
            display: grid;
            grid-template-columns: 1fr 1fr;
            gap: 2rem;
        }

        @media (max-width: 1024px) {
            .memory-explorer {
                grid-template-columns: 1fr;
            }
        }

        .sql-log-wrapper {
            background: rgba(0, 0, 0, 0.25);
            border-radius: 8px;
            padding: 1rem;
            max-height: 350px;
            overflow-y: auto;
            border: 1px solid rgba(255, 255, 255, 0.02);
            font-family: 'Courier Prime', monospace;
            font-size: 0.8rem;
        }

        .sql-log-item {
            padding: 0.75rem;
            border-bottom: 1px solid rgba(255, 255, 255, 0.03);
        }

        .sql-log-item:last-child {
            border-bottom: none;
        }

        .sql-meta {
            display: flex;
            justify-content: space-between;
            color: var(--accent-cyan);
            margin-bottom: 0.25rem;
        }

        .sql-content {
            color: #e5e7eb;
            white-space: pre-wrap;
            word-break: break-all;
        }

        @keyframes pulse-glow {
            0%, 100% {
                transform: scale(1);
                box-shadow: 0 0 10px var(--accent-cyan);
            }
            50% {
                transform: scale(1.2);
                box-shadow: 0 0 20px var(--accent-cyan);
            }
        }

        /* CUSTOM SCROLLBAR */
        ::-webkit-scrollbar {
            width: 8px;
            height: 8px;
        }
        ::-webkit-scrollbar-track {
            background: var(--bg-color);
        }
        ::-webkit-scrollbar-thumb {
            background: #1e293b;
            border-radius: 4px;
        }
        ::-webkit-scrollbar-thumb:hover {
            background: #475569;
        }

        .run-btn {
            background: linear-gradient(135deg, var(--accent-cyan) 0%, var(--accent-purple) 100%);
            border: none;
            color: white;
            padding: 4px 10px;
            font-size: 0.8rem;
            border-radius: 4px;
            cursor: pointer;
            font-weight: 600;
            transition: all 0.2s ease;
        }
        .run-btn:hover {
            opacity: 0.9;
            box-shadow: 0 0 10px rgba(6, 182, 212, 0.4);
        }
        .run-btn:disabled {
            background: #374151;
            cursor: not-allowed;
            box-shadow: none;
        }
    </style>
</head>
<body>

<header>
    <div class="logo-section">
        <div class="logo-icon"></div>
        <h1>Sovereign Nexus | APEX Duality</h1>
    </div>
    <div class="axiom-badge">AXIOM: 1=1=1</div>
</header>

<main>
    <!-- Live Telemetry row -->
    <div class="telemetry-row">
        <div class="card">
            <div class="card-title">Thermodynamic Status</div>
            <div class="card-value highlight-cyan" id="sys-temp">--.- °C</div>
            <div class="card-subtitle" id="sys-gov">Governor: STABLE</div>
        </div>
        <div class="card">
            <div class="card-title">Memory Load</div>
            <div class="card-value highlight-purple" id="sys-ram">-.-- GB / -.-- GB</div>
            <div class="card-subtitle">8GB Local Boundary Constraint</div>
        </div>
        <div class="card">
            <div class="card-title">Computation Load</div>
            <div class="card-value highlight-emerald" id="sys-cpu">-.--</div>
            <div class="card-subtitle">Core Influx Ratio</div>
        </div>
        <div class="card">
            <div class="card-title">Duality Drift Status</div>
            <div class="card-value" id="sys-drift-summary">Checking...</div>
            <div class="card-subtitle">Drift across mirror states</div>
        </div>
    </div>

    <!-- Duality Node Map -->
    <div class="duality-grid">
        <div class="card duality-card">
            <div class="duality-header">
                <div class="node-title">Node 1: Command Center</div>
                <div class="status-badge emerald">TOWER CORE</div>
            </div>
            <div class="node-path">USER: geminiology@penguin | DIR: ~/SovereignNexus</div>
            <div class="asset-list">
                <div class="asset-item">
                    <span class="asset-name">Database Core</span>
                    <span class="asset-value">sovereign_memory.db</span>
                </div>
                <div class="asset-item">
                    <span class="asset-name">Master Blueprint</span>
                    <span class="asset-value">SovereignQueen.Modelfile</span>
                </div>
                <div class="asset-item">
                    <span class="asset-name">Source Code Root</span>
                    <span class="asset-value">~/SovereignNexus/src</span>
                </div>
            </div>
        </div>

        <div class="card duality-card">
            <div class="duality-header">
                <div class="node-title">Node 2: Light Scout</div>
                <div class="status-badge purple">MINI SCOUT</div>
            </div>
            <div class="node-path">USER: ofthefirstlight@penguin | DIR: ~/SovereignNexus/Geminiology</div>
            <div class="asset-list">
                <div class="asset-item">
                    <span class="asset-name">GitHub Clone</span>
                    <span class="asset-value">Geminiology Repository</span>
                </div>
                <div class="asset-item">
                    <span class="asset-name">Network Conduit</span>
                    <span class="asset-value">queen_interface.py</span>
                </div>
                <div class="asset-item">
                    <span class="asset-name">Duality Mirror</span>
                    <span class="asset-value">/SovereignLocal</span>
                </div>
            </div>
        </div>
    </div>

    <!-- Ledgers Drift Matrix -->
    <div class="drift-matrix">
        <div class="section-header">
            <div class="section-title">
                <div class="logo-icon" style="background-color: var(--accent-cyan);"></div>
                Master Ledger Drift Audit Matrix
            </div>
            <div style="font-size: 0.85rem; font-family: 'Courier Prime', monospace; color: var(--accent-rose);" id="genesis-hash-display">
                GENESIS: 289706b29d...ce8b
            </div>
        </div>
        <div class="table-wrapper">
            <table>
                <thead>
                    <tr>
                        <th>Ledger Identifier / Path</th>
                        <th>File Size</th>
                        <th>Record Count</th>
                        <th>Last Modified</th>
                        <th>Cryptographic Hash (SHA-256)</th>
                        <th>Alignment Status</th>
                    </tr>
                </thead>
                <tbody id="drift-matrix-body">
                    <tr>
                        <td colspan="6" style="text-align: center; color: var(--text-muted);">Analyzing Master Ledger Files...</td>
                    </tr>
                </tbody>
            </table>
        </div>
    </div>

    <!-- Trinary Logic Lab -->
    <div class="card">
        <div class="section-header">
            <div class="section-title">
                <div class="logo-icon" style="background-color: var(--accent-purple);"></div>
                Balanced Ternary Primitive Lab (-1, 0, 1)
            </div>
            <div class="axiom-badge" style="background: rgba(139, 92, 246, 0.1); border-color: var(--accent-purple); color: var(--accent-purple);">
                1=1=1 Balanced Logic
            </div>
        </div>
        <div class="trinary-lab">
            <div class="interactive-panel">
                <div class="form-group">
                    <label class="form-label">Input State A</label>
                    <div class="trinary-buttons" id="btn-group-a">
                        <button class="trinary-btn" data-val="-1">-1</button>
                        <button class="trinary-btn active" data-val="0">0</button>
                        <button class="trinary-btn" data-val="1">1</button>
                    </div>
                </div>

                <div class="form-group" id="group-b-container">
                    <label class="form-label">Input State B</label>
                    <div class="trinary-buttons" id="btn-group-b">
                        <button class="trinary-btn" data-val="-1">-1</button>
                        <button class="trinary-btn active" data-val="0">0</button>
                        <button class="trinary-btn" data-val="1">1</button>
                    </div>
                </div>

                <div class="form-group">
                    <label class="form-label">Trinary Gate operator</label>
                    <select class="select-op" id="select-op">
                        <option value="NOT">Trinary NOT (Inversion)</option>
                        <option value="AND" selected>Trinary AND (Minimum)</option>
                        <option value="OR">Trinary OR (Maximum)</option>
                        <option value="CONSENSUS">Trinary CONSENSUS (Agreement)</option>
                    </select>
                </div>
            </div>

            <div class="result-panel">
                <div class="result-title">Evaluated State Output</div>
                <div class="result-val" id="trinary-res">0</div>
                <div class="result-desc" id="trinary-desc">Unknown (0)</div>
            </div>
        </div>
    </div>

    <!-- SQLite Memory Database Explorer -->
    <div class="memory-explorer">
        <div class="card">
            <div class="section-header">
                <div class="section-title">
                    <div class="logo-icon" style="background-color: var(--accent-emerald);"></div>
                    Prime Ledger (Verified 1=1=1 Axioms)
                </div>
                <div class="axiom-badge" id="prime-count-badge">0 Records</div>
            </div>
            <div class="sql-log-wrapper" id="prime-log-container">
                <div style="color: var(--text-muted); text-align: center; padding: 2rem;">No verified records loaded.</div>
            </div>
        </div>

        <div class="card">
            <div class="section-header">
                <div class="section-title">
                    <div class="logo-icon" style="background-color: var(--accent-rose);"></div>
                    Suspension Gate (Ghost Twin / Unverified Data)
                </div>
                <div class="axiom-badge" style="background: rgba(244, 63, 94, 0.1); border-color: var(--accent-rose); color: var(--accent-rose);" id="suspension-count-badge">0 Records</div>
            </div>
            <div class="sql-log-wrapper" id="suspension-log-container">
                <div style="color: var(--text-muted); text-align: center; padding: 2rem;">No suspended records loaded.</div>
            </div>
        </div>
    </div>

    <!-- Sovereign Ledger: Merkle Chain -->
    <div class="card">
        <div class="section-header">
            <div class="section-title">
                <div class="logo-icon" style="background-color: var(--accent-cyan);"></div>
                Sovereign Ledger : Merkle Chain
            </div>
            <div class="axiom-badge" style="background: rgba(6, 182, 212, 0.1); border-color: var(--accent-cyan); color: var(--accent-cyan);">1=1=1 Immutable Chaining</div>
        </div>
        <div class="ledger-container" style="background: rgba(0, 0, 0, 0.25); border: 1px solid rgba(255,255,255,0.05); padding: 1.5rem; border-radius: 8px; font-family: monospace;">
            <div id="live-ledger-feed" style="display: flex; flex-direction: column; gap: 0.75rem;">
                <p style="color: var(--text-muted); text-align: center; padding: 1rem;">Awaiting cryptographic sync...</p>
            </div>
        </div>
    </div>

    <!-- 12-Agent Swarm Grid -->
    <div class="card">
        <div class="section-header">
            <div class="section-title">
                <div class="logo-icon" style="background-color: var(--accent-cyan);"></div>
                Sovereign 12/24 Agent Swarm Activity Monitor
            </div>
            <div class="axiom-badge">Optimus Prime Swarm</div>
        </div>
        <div class="agent-grid" id="agent-grid-container">
            <!-- Statically populated from API -->
        </div>
    </div>
</main>

<script>
    let currentA = 0;
    let currentB = 0;

    // Fetch live system telemetry
    async function updateTelemetry() {
        try {
            const res = await fetch('/api/telemetry');
            const data = await res.json();
            
            document.getElementById('sys-temp').innerText = data.temperature;
            document.getElementById('sys-ram').innerText = data.ram_usage;
            document.getElementById('sys-cpu').innerText = data.cpu_load;
            
            const govBadge = document.getElementById('sys-gov');
            govBadge.innerText = `Governor: ${data.governor_status}`;
            if (data.governor_status === 'CRITICAL THROTTLE') {
                govBadge.style.color = 'var(--accent-rose)';
            } else if (data.governor_status === 'ACTIVE MITIGATION') {
                govBadge.style.color = 'var(--accent-purple)';
            } else {
                govBadge.style.color = 'var(--text-muted)';
            }
        } catch (e) {
            console.error("Failed to fetch telemetry:", e);
        }
    }

    // Fetch database records
    async function updateDbMetrics() {
        try {
            const res = await fetch('/api/db');
            const data = await res.json();
            
            if (!data.exists) return;
            
            document.getElementById('prime-count-badge').innerText = `${data.prime_count} Records`;
            document.getElementById('suspension-count-badge').innerText = `${data.suspension_count} Records`;
            
            // Render Prime ledger
            const primeContainer = document.getElementById('prime-log-container');
            if (data.recent_prime.length === 0) {
                primeContainer.innerHTML = '<div style="color: var(--text-muted); text-align: center; padding: 2rem;">No verified records in database.</div>';
            } else {
                primeContainer.innerHTML = data.recent_prime.map(r => `
                    <div class="sql-log-item">
                        <div class="sql-meta">
                            <span>ID: ${r.id} | ${r.agent_id}</span>
                            <span>${r.timestamp}</span>
                        </div>
                        <div style="font-size:0.75rem; color:var(--text-muted); margin-bottom:0.25rem;">Hash: ${r.sha256_hash.substring(0, 16)}...</div>
                        <div class="sql-content">${escapeHtml(r.content)}</div>
                    </div>
                `).join('');
            }

            // Render Suspension Gate ledger
            const suspensionContainer = document.getElementById('suspension-log-container');
            if (data.recent_suspension.length === 0) {
                suspensionContainer.innerHTML = '<div style="color: var(--text-muted); text-align: center; padding: 2rem;">No suspended records.</div>';
            } else {
                suspensionContainer.innerHTML = data.recent_suspension.map(r => `
                    <div class="sql-log-item">
                        <div class="sql-meta" style="color: var(--accent-rose)">
                            <span>ID: ${r.id} | ${r.agent_id}</span>
                            <span>${r.timestamp}</span>
                        </div>
                        <div style="font-size:0.75rem; color:var(--text-muted); margin-bottom:0.25rem;">Hash: ${r.sha256_hash.substring(0, 16)}...</div>
                        <div class="sql-content">${escapeHtml(r.content)}</div>
                    </div>
                `).join('');
            }
        } catch (e) {
            console.error("Failed to fetch database metrics:", e);
        }
    }

    // Fetch drift matrix
    async function updateDriftMatrix() {
        try {
            const res = await fetch('/api/drift');
            const data = await res.json();
            
            document.getElementById('genesis-hash-display').innerText = `GENESIS: ${data.genesis_hash.substring(0, 16)}...${data.genesis_hash.substring(48)}`;
            
            const tbody = document.getElementById('drift-matrix-body');
            tbody.innerHTML = '';
            
            let driftedCount = 0;
            let totalChecked = 0;

            for (const [name, info] of Object.entries(data.ledgers)) {
                if (!info.exists) {
                    tbody.innerHTML += `
                        <tr>
                            <td><strong>${name}</strong></td>
                            <td colspan="5" style="color: var(--accent-rose); font-style: italic;">File Not Found (Drift Unchecked)</td>
                        </tr>
                    `;
                    continue;
                }
                
                totalChecked++;
                if (info.drifted) driftedCount++;
                
                const statusBadge = info.drifted ? 
                    '<span class="status-badge rose">DRIFTED</span>' : 
                    '<span class="status-badge emerald">ALIGNED</span>';
                
                tbody.innerHTML += `
                    <tr>
                        <td><strong>${name}</strong></td>
                        <td>${info.size_mb} MB</td>
                        <td>${info.line_count.toLocaleString()} lines</td>
                        <td>${info.mtime}</td>
                        <td style="font-family: 'Courier Prime', monospace; font-size: 0.8rem;">
                            ${info.hash.substring(0, 24)}...
                        </td>
                        <td>${statusBadge}</td>
                    </tr>
                `;
            }
            
            const summaryVal = document.getElementById('sys-drift-summary');
            if (driftedCount === 0 && totalChecked > 0) {
                summaryVal.innerText = "ALIGNED";
                summaryVal.className = "card-value highlight-emerald";
            } else if (driftedCount > 0) {
                summaryVal.innerText = `${driftedCount} DRIFTED`;
                summaryVal.className = "card-value highlight-rose";
            } else {
                summaryVal.innerText = "NO DATA";
                summaryVal.className = "card-value";
            }
        } catch (e) {
            console.error("Failed to fetch drift matrix:", e);
        }
    }

    // Fetch agent swarm grid
    async function updateAgentSwarm() {
        try {
            const res = await fetch('/api/agents');
            const data = await res.json();
            
            const container = document.getElementById('agent-grid-container');
            container.innerHTML = data.map(a => {
                let badgeClass = 'cyan';
                if (a.status === 'ALIGNED') badgeClass = 'emerald';
                if (a.status === 'SLEEP_WALK') badgeClass = 'purple';
                if (a.status === 'IDLE') badgeClass = 'cyan';
                if (a.status === 'RUNNING') badgeClass = 'purple';
                
                // Agents that take input prompts
                const requiresInput = [6, 8, 10, 12, 13, 14, 17, 19].includes(a.id);
                const placeholderText = a.id === 10 ? "FusionReactor" : "Query...";
                
                return `
                    <div class="agent-card" style="display: flex; flex-direction: column; justify-content: space-between;">
                        <div>
                            <div class="agent-header">
                                <span class="agent-id">AGENT ${a.id.toString().padStart(2, '0')}</span>
                                <span class="status-badge ${badgeClass}">${a.status}</span>
                            </div>
                            <div class="agent-name">${a.name}</div>
                            <div class="agent-role">${a.role}</div>
                        </div>
                        <div style="margin-top: 1rem; display: flex; gap: 0.5rem; align-items: center;">
                            ${requiresInput ? `<input type="text" id="input-agent-${a.id}" placeholder="${placeholderText}" style="flex-grow: 1; background: #1e293b; border: 1px solid rgba(255,255,255,0.1); color: white; padding: 4px 6px; font-size: 0.8rem; border-radius: 4px; width: 60px;">` : ''}
                            <button class="run-btn" id="btn-agent-${a.id}" onclick="runAgent(${a.id})" ${a.status === 'RUNNING' ? 'disabled' : ''}>
                                ${a.status === 'RUNNING' ? 'Running' : 'Run'}
                            </button>
                        </div>
                    </div>
                `;
            }).join('');
        } catch (e) {
            console.error("Failed to fetch agent swarm:", e);
        }
    }

    async function runAgent(id) {
        const inputEl = document.getElementById(`input-agent-${id}`);
        const inputVal = inputEl ? inputEl.value : "";
        const btn = document.getElementById(`btn-agent-${id}`);
        
        if (btn) {
            btn.disabled = true;
            btn.innerText = "Running";
        }
        
        try {
            const res = await fetch('/api/run-agent', {
                method: 'POST',
                headers: { 'Content-Type': 'application/json' },
                body: JSON.stringify({ agent_id: id, input_data: inputVal })
            });
            const data = await res.json();
            
            if (data.status === 'success') {
                alert(`Agent ${id} Executed Successfully:\n\n${data.stdout}`);
            } else {
                alert(`Agent ${id} Execution Failed:\n\n${data.error || data.stderr || 'No detail provided.'}`);
            }
        } catch (e) {
            console.error("Error executing agent:", e);
            alert("Network error: Could not reach agent endpoint.");
        } finally {
            updateAgentSwarm();
        }
    }

    // Interactive Trinary Evaluator
    async function evaluateTrinary() {
        const op = document.getElementById('select-op').value;
        const body = { op: op, a: currentA };
        if (op !== 'NOT') {
            body.b = currentB;
        }

        try {
            const res = await fetch('/api/trinary', {
                method: 'POST',
                headers: { 'Content-Type': 'application/json' },
                body: JSON.stringify(body)
            });
            const data = await res.json();
            
            const resVal = document.getElementById('trinary-res');
            resVal.innerText = data.result;
            
            const resDesc = document.getElementById('trinary-desc');
            resDesc.innerText = data.label;
            
            // Style result based on value
            if (data.result === 1) {
                resVal.style.color = 'var(--accent-emerald)';
                resVal.style.textShadow = '0 0 15px rgba(16, 185, 129, 0.4)';
            } else if (data.result === -1) {
                resVal.style.color = 'var(--accent-rose)';
                resVal.style.textShadow = '0 0 15px rgba(244, 63, 94, 0.4)';
            } else {
                resVal.style.color = 'var(--text-muted)';
                resVal.style.textShadow = 'none';
            }
        } catch (e) {
            console.error("Failed to evaluate trinary logic:", e);
        }
    }

    function initTrinaryLab() {
        const groupA = document.getElementById('btn-group-a');
        const groupB = document.getElementById('btn-group-b');
        const selectOp = document.getElementById('select-op');
        const groupBContainer = document.getElementById('group-b-container');

        // Toggle buttons for group A
        groupA.querySelectorAll('button').forEach(btn => {
            btn.addEventListener('click', () => {
                groupA.querySelectorAll('button').forEach(b => b.classList.remove('active'));
                btn.classList.add('active');
                currentA = parseInt(btn.dataset.val);
                evaluateTrinary();
            });
        });

        // Toggle buttons for group B
        groupB.querySelectorAll('button').forEach(btn => {
            btn.addEventListener('click', () => {
                groupB.querySelectorAll('button').forEach(b => b.classList.remove('active'));
                btn.classList.add('active');
                currentB = parseInt(btn.dataset.val);
                evaluateTrinary();
            });
        });

        // Toggle operation changes
        selectOp.addEventListener('change', () => {
            if (selectOp.value === 'NOT') {
                groupBContainer.style.opacity = '0.3';
                groupBContainer.style.pointerEvents = 'none';
            } else {
                groupBContainer.style.opacity = '1';
                groupBContainer.style.pointerEvents = 'auto';
            }
            evaluateTrinary();
        });

        evaluateTrinary();
    }

    function escapeHtml(text) {
        if (!text) return '';
        return text
            .replace(/&/g, "&amp;")
            .replace(/</g, "&lt;")
            .replace(/>/g, "&gt;")
            .replace(/"/g, "&quot;")
            .replace(/'/g, "&#039;");
    }

    async function updateLedgerFeed() {
        try {
            const res = await fetch('/api/ledger');
            const data = await res.json();
            
            if (data.status === "SUCCESS") {
                const feed = document.getElementById('live-ledger-feed');
                if (!data.ledger || data.ledger.length === 0) {
                    feed.innerHTML = '<div style="color: var(--text-muted); text-align: center; padding: 1rem;">No cryptographic blocks recorded.</div>';
                    return;
                }
                
                feed.innerHTML = data.ledger.map(block => `
                    <div style="margin-bottom: 0.5rem; border-left: 2px solid var(--accent-cyan); padding-left: 0.75rem; display: flex; flex-direction: column; gap: 0.25rem;">
                        <div>
                            <strong style="color: var(--accent-cyan);">BLK ${block.block}</strong> | 
                            <span style="color: #ffffff; font-weight: bold;">${escapeHtml(block.task)}</span>
                        </div>
                        <div style="color: var(--text-muted); font-size: 0.85rem;">
                            Hash: <span style="color: #94a3b8; font-family: monospace;">${escapeHtml(block.hash)}</span>
                        </div>
                        <div style="color: var(--text-muted); font-size: 0.85rem;">
                            Sig: <span style="color: var(--accent-purple); font-family: monospace;">${escapeHtml(block.signature)}</span> 
                            <span style="color: var(--accent-emerald); font-weight: bold; margin-left: 0.5rem;">[Verified]</span>
                        </div>
                    </div>
                `).join('');
            }
        } catch (err) {
            console.error("Ledger polling paused:", err);
        }
    }

    // Main loops
    function init() {
        initTrinaryLab();
        
        // Initial fetches
        updateTelemetry();
        updateDbMetrics();
        updateDriftMatrix();
        updateAgentSwarm();
        updateLedgerFeed();
        
        // Dynamic poll loops
        setInterval(updateTelemetry, 3000);  // 3s telemetry
        setInterval(updateDbMetrics, 10000); // 10s DB refresh
        setInterval(updateAgentSwarm, 10000); // 10s agent swarm
        setInterval(updateDriftMatrix, 30000); // 30s drift audit
        setInterval(updateLedgerFeed, 3000); // 3s ledger polling
    }

    window.onload = init;
</script>
</body>
</html>
"""

def run_server():
    port = 8000
    while port < 8100:
        try:
            # Threading server makes concurrent API requests snap instantly
            server = ThreadingHTTPServer(('0.0.0.0', port), DashboardHandler)
            print("==============================================================")
            print("  S O V E R E I G N   N E X U S   |   A P E X   S E R V E R   ")
            print(f"  Status: ACTIVE | Port Bound: {port}")
            print(f"  URL: http://localhost:{port}")
            print("==============================================================")
            print("Press Ctrl+C to shut down APEX dashboard loop.")
            
            server.serve_forever()
            break
        except OSError:
            # Port collision failover
            port += 1
        except KeyboardInterrupt:
            print("\nShutting down APEX Server. The Symmetrical Line holds.")
            break

if __name__ == "__main__":
    run_server()
