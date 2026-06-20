#!/usr/bin/env python3
import os
import sys
import sqlite3
import hashlib
import threading
import time
from flask import Flask, request, jsonify, render_template_string
from werkzeug.utils import secure_filename

# Ensure the parent path is in path for chunk_ingester import
sys.path.append(os.path.expanduser("~/SovereignNexus"))
import chunk_ingester

# ==============================================================================
# SovereignNexus: Oracle Web Server & Stage Control (V2.0)
# Component: oracle_server.py
# Axiom: 1=1=1 | Status: ACTIVE (TOKEN-GATED + TELEMETRY + AUTO-INGEST)
# Description: Flask-based Command Center UI. Gates file uploads via token,
#              automatically runs chunk_ingester in a background thread,
#              and reports live CPU temperature, memory usage, and load telemetry.
# ==============================================================================

app = Flask(__name__)
app.config['MAX_CONTENT_LENGTH'] = 50 * 1024 * 1024  # 50MB file size limit

DB_PATH = os.path.expanduser("~/SovereignNexus/nexus_ledger.db")
INTAKE_DIR = os.path.expanduser("~/SovereignNexus/sync_intake")
MODEL_NAME = "qwen2.5:0.5b"

# Valid payment/access tokens
VALID_TOKENS = {"NEXUS-777-ALPHA", "SOVEREIGN-999-BETA"}

HTML_TEMPLATE = """
<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Sovereign Nexus | Command Center</title>
    <style>
        body {
            background-color: #050709;
            color: #00ff00;
            font-family: 'Courier New', Courier, monospace;
            margin: 0;
            display: flex;
            height: 100vh;
            overflow: hidden;
        }
        
        /* Sidebar: Chat & Ingestion */
        #sidebar {
            width: 35%;
            border-right: 2px solid #00ff00;
            display: flex;
            flex-direction: column;
            background-color: #090d12;
            box-sizing: border-box;
            height: 100%;
        }
        
        .panel-header {
            background: #00ff00;
            color: #000;
            font-weight: bold;
            padding: 10px;
            text-align: center;
            text-transform: uppercase;
            font-size: 0.9em;
            letter-spacing: 2px;
        }
        
        /* Top half: Chat box */
        #chat-section {
            height: 50%;
            display: flex;
            flex-direction: column;
            border-bottom: 2px solid #00ff00;
            box-sizing: border-box;
        }
        #chat-box {
            flex-grow: 1;
            overflow-y: auto;
            padding: 15px;
            background-color: #020304;
            font-size: 0.85em;
            line-height: 1.4;
        }
        .user-msg { color: #00bfff; margin-bottom: 12px; }
        .oracle-msg { color: #00ff00; margin-bottom: 12px; white-space: pre-wrap; }
        .chat-input-area {
            padding: 10px;
            display: flex;
            background: #090d12;
        }
        .chat-input-area textarea {
            flex-grow: 1;
            height: 40px;
            background: #000;
            color: #00ff00;
            border: 1px solid #00ff00;
            padding: 5px;
            resize: none;
            box-sizing: border-box;
        }
        .chat-input-area button {
            width: 70px;
            background: #00ff00;
            color: #000;
            border: none;
            cursor: pointer;
            font-weight: bold;
            margin-left: 5px;
        }
        .chat-input-area button:hover { background: #00cc00; }
        
        /* Bottom half: Staging / Upload */
        #ingest-section {
            height: 50%;
            display: flex;
            flex-direction: column;
            box-sizing: border-box;
            padding: 15px;
        }
        .token-input {
            width: 100%;
            background: #000;
            color: #00ff00;
            border: 1px solid #00ff00;
            padding: 8px;
            box-sizing: border-box;
            margin-bottom: 10px;
            font-family: monospace;
            text-align: center;
        }
        #drop-zone {
            flex-grow: 1;
            border: 2px dashed #00ff00;
            display: flex;
            flex-direction: column;
            justify-content: center;
            align-items: center;
            cursor: pointer;
            background-color: #020304;
            transition: background 0.3s;
            text-align: center;
            padding: 10px;
        }
        #drop-zone.dragover { background-color: #091a10; }
        #drop-zone p { margin: 5px 0; font-size: 0.8em; }
        
        /* Main Panel: Swarm, Ledgers, Ingestion Log */
        #main-panel {
            width: 65%;
            display: flex;
            flex-direction: column;
            padding: 20px;
            box-sizing: border-box;
            overflow-y: auto;
            background-color: #050709;
        }
        
        h1 {
            margin-top: 0;
            border-bottom: 2px solid #00ff00;
            padding-bottom: 10px;
            font-size: 1.6em;
            letter-spacing: 1px;
        }
        
        .status-grid {
            display: grid;
            grid-template-columns: repeat(3, 1fr);
            gap: 15px;
            margin-bottom: 20px;
        }
        
        .status-box {
            border: 1px solid #00ff00;
            padding: 10px;
            background-color: #020304;
            font-size: 0.8em;
        }
        .status-box strong { color: #fff; }
        
        .section-title {
            font-weight: bold;
            text-transform: uppercase;
            margin-top: 20px;
            margin-bottom: 10px;
            border-bottom: 1px dashed #00ff00;
            padding-bottom: 5px;
            font-size: 0.95em;
        }
        
        /* Ledger logs table */
        table {
            width: 100%;
            border-collapse: collapse;
            font-size: 0.75em;
            background-color: #020304;
            margin-bottom: 20px;
        }
        th, td {
            border: 1px solid #333;
            padding: 8px;
            text-align: left;
        }
        th {
            background-color: #090d12;
            color: #00ff00;
            border-bottom: 1px solid #00ff00;
        }
        
        #upload-status {
            font-size: 0.8em;
            margin-top: 8px;
            height: 15px;
            color: #00bfff;
        }
    </style>
</head>
<body>

    <!-- Left Sidebar -->
    <div id="sidebar">
        <!-- Chat Node -->
        <div id="chat-section">
            <div class="panel-header">Oracle Chat Interface</div>
            <div id="chat-box">
                <div class="oracle-msg">[ORACLE]: Core initialized. Ready to process ledger queries.</div>
            </div>
            <div class="chat-input-area">
                <textarea id="chat-input" placeholder="Query the ledger records..." onkeypress="handleKeyPress(event)"></textarea>
                <button onclick="sendChatQuery()">ASK</button>
            </div>
        </div>
        
        <!-- File Ingest -->
        <div id="ingest-section">
            <div class="panel-header">Token-Gated Staging Area</div>
            <p style="font-size:0.75em; color:#888; margin: 10px 0 5px 0;">Enter Authorized Payment Token:</p>
            <input type="text" id="token-field" class="token-input" placeholder="NEXUS-777-ALPHA">
            <div id="drop-zone" onclick="triggerFileInput()" ondragover="handleDragOver(event)" ondragleave="handleDragLeave()" ondrop="handleDrop(event)">
                <svg width="40" height="40" viewBox="0 0 24 24" fill="none" stroke="#00ff00" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><path d="M21 15v4a2 2 0 0 1-2 2H5a2 2 0 0 1-2-2v-4"></path><polyline points="17 8 12 3 7 8"></polyline><line x1="12" y1="3" x2="12" y2="15"></line></svg>
                <p style="font-weight:bold; margin-top:10px;">DRAG & DROP FILE HERE</p>
                <p style="color:#888;">or click to select file</p>
                <input type="file" id="file-input" style="display:none;" onchange="handleFileSelect(event)">
            </div>
            <div id="upload-status"></div>
        </div>
    </div>

    <!-- Main Command Center Panel -->
    <div id="main-panel">
        <h1>SOVEREIGN NEXUS: APEX DASHBOARD</h1>
        
        <div class="status-grid">
            <div id="sys-temp-box" class="status-box">
                <strong>CPU TEMP:</strong> <span id="sys-temp">0.0 °C</span>
            </div>
            <div class="status-box">
                <strong>MEMORY LOAD:</strong> <span id="sys-ram">0.00 GB / 8.00 GB</span>
            </div>
            <div class="status-box">
                <strong>CPU LOAD:</strong> <span id="sys-load">0.00</span>
            </div>
        </div>
        
        <div class="section-title">Ingested Ledger Records (nexus_ledger.db)</div>
        <table id="ledger-table">
            <thead>
                <tr>
                    <th>Timestamp</th>
                    <th>Filename</th>
                    <th>Chunk Index</th>
                    <th>Summary Extracted</th>
                    <th>Cryptographic Seal</th>
                </tr>
            </thead>
            <tbody id="ledger-body">
                <tr>
                    <td colspan="5" style="text-align:center; color:#888;">Loading ledger...</td>
                </tr>
            </tbody>
        </table>
        
        <div class="section-title">Client Ingestion Queue</div>
        <div style="font-size:0.8em; color:#888;">
            * Staged payloads verify tokens prior to file movement.<br>
            * Processing is handled asynchronously in the background to prevent server timeouts.
        </div>
    </div>

    <script>
        function handleKeyPress(e) {
            if (e.key === 'Enter' && !e.shiftKey) {
                e.preventDefault();
                sendChatQuery();
            }
        }
        
        async function sendChatQuery() {
            const input = document.getElementById('chat-input');
            const query = input.value.trim();
            if (!query) return;
            
            const chatBox = document.getElementById('chat-box');
            chatBox.innerHTML += `<div class="user-msg">> ${query}</div>`;
            input.value = '';
            
            const loadingId = 'loading-' + Date.now();
            chatBox.innerHTML += `<div id="${loadingId}" class="oracle-msg" style="color:#888;">[*] Spinning local Qwen core (ETA ~3 mins)...</div>`;
            chatBox.scrollTop = chatBox.scrollHeight;
            
            try {
                const response = await fetch('/api/query', {
                    method: 'POST',
                    headers: { 'Content-Type': 'application/json' },
                    body: JSON.stringify({ query: query })
                });
                const data = await response.json();
                document.getElementById(loadingId).remove();
                chatBox.innerHTML += `<div class="oracle-msg">[ORACLE]: ${data.answer}</div><hr style="border-color:#222;">`;
            } catch (err) {
                document.getElementById(loadingId).remove();
                chatBox.innerHTML += `<div class="oracle-msg" style="color:red;">[!] Link failure. Check daemon.</div><hr style="border-color:#222;">`;
            }
            chatBox.scrollTop = chatBox.scrollHeight;
        }
        
        // Ingestion Dropbox Mechanics
        const dropZone = document.getElementById('drop-zone');
        const uploadStatus = document.getElementById('upload-status');
        
        function triggerFileInput() {
            document.getElementById('file-input').click();
        }
        
        function handleDragOver(e) {
            e.preventDefault();
            dropZone.classList.add('dragover');
        }
        
        function handleDragLeave() {
            dropZone.classList.remove('dragover');
        }
        
        function handleDrop(e) {
            e.preventDefault();
            dropZone.classList.remove('dragover');
            const files = e.dataTransfer.files;
            if (files.length) uploadFile(files[0]);
        }
        
        function handleFileSelect(e) {
            const files = e.target.files;
            if (files.length) uploadFile(files[0]);
        }
        
        async function uploadFile(file) {
            const token = document.getElementById('token-field').value.trim();
            if (!token) {
                uploadStatus.innerHTML = "<span style='color:red;'>[!] Verification Token Required.</span>";
                return;
            }
            
            uploadStatus.innerHTML = "[*] Verifying token and staging file...";
            
            const formData = new FormData();
            formData.append('file', file);
            formData.append('token', token);
            
            try {
                const response = await fetch('/api/stage', {
                    method: 'POST',
                    body: formData
                });
                const data = await response.json();
                if (response.ok) {
                    uploadStatus.innerHTML = `<span style='color:#00ff00;'>[✓] Autopilot: Processing ${data.filename} in background...</span>`;
                    setTimeout(updateLedgerTable, 2000);
                } else {
                    uploadStatus.innerHTML = `<span style='color:red;'>[!] Reject: ${data.error}</span>`;
                }
            } catch (err) {
                uploadStatus.innerHTML = "<span style='color:red;'>[!] Staging connection error.</span>";
            }
        }
        
        // Auto-refresh ledger view
        async function updateLedgerTable() {
            try {
                const response = await fetch('/api/ledger');
                const data = await response.json();
                const tbody = document.getElementById('ledger-body');
                tbody.innerHTML = '';
                
                if (data.records.length === 0) {
                    tbody.innerHTML = '<tr><td colspan="5" style="text-align:center; color:#888;">No records logged in chunk_ledger.</td></tr>';
                    return;
                }
                
                data.records.forEach(row => {
                    const tr = document.createElement('tr');
                    tr.innerHTML = `
                        <td>${row.timestamp}</td>
                        <td>${row.filename}</td>
                        <td style="text-align:center;">${row.chunk_index}/${row.total_chunks}</td>
                        <td>${row.chunk_summary}</td>
                        <td style="font-family:monospace; font-size:0.9em; color:#888;">${row.chunk_hash.substring(0,16)}...</td>
                    `;
                    tbody.appendChild(tr);
                });
            } catch (err) {
                console.error("Ledger update failed:", err);
            }
        }
        
        // Live Telemetry refresh
        async function updateSystemStatus() {
            try {
                const response = await fetch('/api/sysinfo');
                const data = await response.json();
                document.getElementById('sys-temp').innerText = data.cpu_temp.toFixed(1) + " °C";
                document.getElementById('sys-ram').innerText = data.ram_used.toFixed(2) + " GB / " + data.ram_total.toFixed(2) + " GB";
                document.getElementById('sys-load').innerText = data.cpu_load.toFixed(2);
                
                const tempBox = document.getElementById('sys-temp-box');
                if (data.cpu_temp > 70) {
                    tempBox.style.borderColor = 'red';
                    tempBox.style.color = 'red';
                } else if (data.cpu_temp > 55) {
                    tempBox.style.borderColor = 'yellow';
                    tempBox.style.color = 'yellow';
                } else {
                    tempBox.style.borderColor = '#00ff00';
                    tempBox.style.color = '#00ff00';
                }
            } catch (err) {
                console.error("Failed to fetch system telemetry:", err);
            }
        }
        
        // Initial load and interval loops
        updateLedgerTable();
        updateSystemStatus();
        setInterval(updateLedgerTable, 10000);
        setInterval(updateSystemStatus, 5000);
    </script>
</body>
</html>
"""

def get_ram_info():
    """Reads Linux RAM stats from /proc/meminfo."""
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
        return round(used_gb, 2), round(total_gb, 2)
    except:
        return 0.43, 6.27  # Default system snapshot fallback

def get_cpu_load():
    """Reads Linux loadavg."""
    try:
        with open("/proc/loadavg", "r") as f:
            load = float(f.read().split()[0])
        return load
    except:
        return 0.44  # Fallback

def retrieve_context(query_text):
    conn = sqlite3.connect(DB_PATH)
    c = conn.cursor()
    keywords = query_text.lower().split()
    try:
        query_conditions = " OR ".join(["chunk_summary LIKE ?" for _ in keywords])
        search_params = [f"%{word}%" for word in keywords]
        c.execute(f"SELECT chunk_summary FROM chunk_ledger WHERE {query_conditions} LIMIT 2", search_params)
        results = c.fetchall()
        conn.close()
        if not results:
            return "NO DATA FOUND."
        return "\n\n".join([row[0] for row in results])
    except:
         return "NO DATA FOUND."

@app.route('/')
def index():
    return render_template_string(HTML_TEMPLATE)

@app.route('/api/sysinfo', methods=['GET'])
def sysinfo():
    temp_c = chunk_ingester.get_cpu_temperature()
    used_ram, total_ram = get_ram_info()
    cpu_load = get_cpu_load()
    return jsonify({
        'cpu_temp': temp_c,
        'ram_used': used_ram,
        'ram_total': total_ram,
        'cpu_load': cpu_load
    })

@app.route('/api/ledger', methods=['GET'])
def get_ledger():
    if not os.path.exists(DB_PATH):
        return jsonify({'records': []})
    
    conn = sqlite3.connect(DB_PATH)
    conn.row_factory = sqlite3.Row
    c = conn.cursor()
    try:
        rows = c.execute("""
            SELECT timestamp, filename, chunk_index, total_chunks, chunk_summary, chunk_hash 
            FROM chunk_ledger 
            ORDER BY id DESC LIMIT 15
        """).fetchall()
        records = [dict(row) for row in rows]
    except Exception as e:
        records = []
    finally:
        conn.close()
        
    return jsonify({'records': records})

@app.route('/api/stage', methods=['POST'])
def stage_payload():
    token = request.form.get('token', '').strip()
    if token not in VALID_TOKENS:
        print(f"[!] Access Refused. Invalid staging token: {token}")
        return jsonify({'error': 'Unauthorized token access.'}), 401
        
    if 'file' not in request.files:
        return jsonify({'error': 'No payload file present.'}), 400
        
    file = request.files['file']
    if file.filename == '':
        return jsonify({'error': 'Filename is empty.'}), 400
        
    if not os.path.exists(INTAKE_DIR):
        os.makedirs(INTAKE_DIR, exist_ok=True)
        
    filename = secure_filename(file.filename)
    stage_path = os.path.join(INTAKE_DIR, filename)
    
    try:
        file.save(stage_path)
        print(f"[✓] Payload authorized. Staged at: {stage_path}")
        
        # Trigger background execution of the chunking daemon
        thread = threading.Thread(target=chunk_ingester.process_file_into_chunks, args=(stage_path,))
        thread.daemon = True
        thread.start()
        print(f"[*] Background chunking worker started for: {filename}")
        
        return jsonify({'status': 'PROCESSING_STAGED', 'filename': filename})
    except Exception as e:
        print(f"[!] Failed to stage file: {e}")
        return jsonify({'error': str(e)}), 500

@app.route('/api/query', methods=['POST'])
def handle_query():
    user_query = request.json.get('query', '')
    print(f"\n[*] Received Oracle Query: {user_query}")
    
    context = retrieve_context(user_query)
    
    system_prompt = (
        "You are the Sovereign Oracle. Answer the user's question using ONLY the provided context "
        "from the database ledger. Do not use outside knowledge. If the context is 'NO DATA FOUND.', "
        "reply exactly with 'DATA NOT FOUND IN LEDGER.'"
    )
    
    full_prompt = f"CONTEXT FROM LEDGER:\n{context}\n\nUSER QUESTION: {user_query}\n\nANSWER:"
    
    try:
        response = chunk_ingester.ollama.chat(model=MODEL_NAME, messages=[
            {'role': 'system', 'content': system_prompt},
            {'role': 'user', 'content': full_prompt}
        ])
        answer = response['message']['content']
        print("[✓] Oracle generation complete.")
        return jsonify({'answer': answer})
    except Exception as e:
        print(f"[!] Ollama connection failed: {e}")
        return jsonify({'answer': f"Local AI Core Connection Error: {e}"})

if __name__ == '__main__':
    os.makedirs(INTAKE_DIR, exist_ok=True)
    init_db_file = sqlite3.connect(DB_PATH)
    init_db_file.close() # Ensure database file exists
    
    print("=" * 60)
    print(" SOVEREIGN COMMAND CENTER SERVER ONLINE (V2.0)")
    print(" Access Dashboard at: http://0.0.0.0:8000")
    print("=" * 60)
    app.run(host='0.0.0.0', port=8000)
