#!/usr/bin/env python3
"""
SovereignCommandCenter: local REST API Gateway
============================================
Component: oracle_server.py
Axiom: 1=1=1

A Flask-based local gateway microservice hosting a developer console UI.
Provides secure endpoints for local database context queries and token-gated
payload ingestion. Interfaces with a local Ollama service for offline inference.
"""

from flask import Flask, request, jsonify, render_template_string
import sqlite3
import ollama
import os
from werkzeug.utils import secure_filename

app = Flask(__name__)

# System file paths for local execution
DB_PATH = os.path.expanduser("~/SovereignNexus/nexus_ledger.db")
INTAKE_DIR = os.path.expanduser("~/SovereignNexus/sync_intake")
MODEL_NAME = "qwen2.5:0.5b"

# Active access tokens (Master key for B2B client demonstration)
VALID_TOKENS = ["NEXUS-777-ALPHA"]

# Ensure target directories exist before server startup
os.makedirs(INTAKE_DIR, exist_ok=True)

# Embedded developer console UI (Glassmorphic dark console theme)
HTML_TEMPLATE = """
<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <title>Sovereign Nexus | Command Center</title>
    <style>
        body { background-color: #0d1117; color: #00ff00; font-family: monospace; margin: 0; display: flex; height: 100vh; overflow: hidden; }
        
        /* Left Sidebar: Split Design */
        #sidebar { width: 30%; border-right: 1px solid #00ff00; display: flex; flex-direction: column; padding: 15px; background-color: #050709; gap: 15px; }
        h2 { font-size: 1.2em; border-bottom: 1px solid #00ff00; padding-bottom: 5px; margin-top: 0; margin-bottom: 10px; }
        
        /* Top Half: Oracle Chat */
        #oracle-section { flex: 1; display: flex; flex-direction: column; overflow: hidden; }
        #chat-box { flex-grow: 1; overflow-y: auto; padding: 10px; margin-bottom: 10px; background-color: #000; border: 1px solid #333; font-size: 0.9em; }
        .user-msg { color: #00bfff; margin-bottom: 10px; }
        .oracle-msg { color: #00ff00; margin-bottom: 10px; }
        .input-area { display: flex; flex-direction: column; }
        textarea { width: 100%; height: 50px; background: #000; color: #00ff00; border: 1px solid #00ff00; padding: 5px; resize: none; margin-bottom: 5px; box-sizing: border-box; }
        button { padding: 8px; background: #00ff00; color: #000; border: none; cursor: pointer; font-weight: bold; }
        button:hover { background: #00cc00; }

        /* Bottom Half: Token-Gated Ingestion */
        #ingest-section { flex: 1; display: flex; flex-direction: column; border-top: 1px dashed #00ff00; padding-top: 15px; }
        #drop-zone { flex-grow: 1; border: 2px dashed #333; display: flex; align-items: center; justify-content: center; text-align: center; color: #555; margin-bottom: 10px; cursor: pointer; transition: 0.3s; background: #000;}
        #drop-zone.dragover { border-color: #00ff00; color: #00ff00; background: #0a1910; }
        .token-input { margin-bottom: 10px; }
        input[type="text"], input[type="password"] { width: 100%; padding: 8px; background: #000; color: #00ff00; border: 1px solid #00ff00; box-sizing: border-box; margin-top: 5px;}
        #upload-status { font-size: 0.85em; margin-top: 10px; color: #888; }
        
        /* Main Workspace */
        #main-workspace { width: 70%; padding: 20px; display: flex; flex-direction: column; }
        #main-workspace h1 { margin-top: 0; font-size: 1.8em; border-bottom: 1px solid #00ff00; padding-bottom: 10px;}
        .status-panel { border: 1px solid #333; padding: 15px; margin-bottom: 20px; background: #000; }
    </style>
</head>
<body>

    <div id="sidebar">
        <div id="oracle-section">
            <h2>ORACLE NODE (ASYNC)</h2>
            <div id="chat-box"></div>
            <div class="input-area">
                <textarea id="query-input" placeholder="Enter research query..."></textarea>
                <button onclick="sendQuery()">EXECUTE</button>
            </div>
        </div>

        <div id="ingest-section">
            <h2>SECURE INGESTION</h2>
            <div class="token-input">
                <label>Access Key:</label>
                <input type="password" id="access-token" placeholder="Enter valid token...">
            </div>
            <input type="file" id="file-input" style="display: none;" onchange="handleFileSelect(event)">
            <div id="drop-zone" onclick="document.getElementById('file-input').click();">
                [ DRAG FILE HERE OR CLICK TO SELECT ]<br><br>Accepts: .txt, .pdf, .csv
            </div>
            <button onclick="uploadFile()">AUTHORIZE & INGEST</button>
            <div id="upload-status">Awaiting payload...</div>
        </div>
    </div>

    <div id="main-workspace">
        <h1>SOVEREIGN COMMAND CENTER</h1>
        <div class="status-panel">
            <strong>SYSTEM STATUS:</strong> ONLINE | <strong>NODE:</strong> GEMINIOLOGY (CPU-BOUND) | <strong>FIDELITY:</strong> 1=1=1<br><br>
            <em>Payment integration pending. Current valid master token: NEXUS-777-ALPHA</em>
        </div>
    </div>

    <script>
        // Oracle Logic
        async function sendQuery() {
            const input = document.getElementById('query-input');
            const query = input.value.trim();
            if (!query) return;
            const chatBox = document.getElementById('chat-box');
            chatBox.innerHTML += `<div class="user-msg">> ${query}</div>`;
            input.value = '';
            const loadingId = 'loading-' + Date.now();
            chatBox.innerHTML += `<div id="${loadingId}" class="oracle-msg" style="color:#888;">[*] Processing...</div>`;
            chatBox.scrollTop = chatBox.scrollHeight;
            try {
                const response = await fetch('/api/query', { method: 'POST', headers: { 'Content-Type': 'application/json' }, body: JSON.stringify({ query: query }) });
                const data = await response.json();
                document.getElementById(loadingId).remove();
                chatBox.innerHTML += `<div class="oracle-msg">[ORACLE]: ${data.answer}</div><hr style="border-color:#333;">`;
            } catch (err) {
                document.getElementById(loadingId).remove();
                chatBox.innerHTML += `<div class="oracle-msg" style="color:red;">[!] Link Failed.</div><hr style="border-color:#333;">`;
            }
            chatBox.scrollTop = chatBox.scrollHeight;
        }

        // Drag and Drop Logic
        const dropZone = document.getElementById('drop-zone');
        let selectedFile = null;

        dropZone.addEventListener('dragover', (e) => { e.preventDefault(); dropZone.classList.add('dragover'); });
        dropZone.addEventListener('dragleave', () => { dropZone.classList.remove('dragover'); });
        dropZone.addEventListener('drop', (e) => {
            e.preventDefault(); dropZone.classList.remove('dragover');
            if (e.dataTransfer.files.length) {
                selectedFile = e.dataTransfer.files[0];
                dropZone.innerHTML = `[ SELECTED: ${selectedFile.name} ]`;
            }
        });

        function handleFileSelect(e) {
            if (e.target.files.length) {
                selectedFile = e.target.files[0];
                dropZone.innerHTML = `[ SELECTED: ${selectedFile.name} ]`;
            }
        }

        // Upload & Token Logic
        async function uploadFile() {
            const token = document.getElementById('access-token').value.trim();
            const statusDiv = document.getElementById('upload-status');
            
            if (!token) { statusDiv.innerHTML = '<span style="color:red;">[!] ERROR: Access Key Required</span>'; return; }
            if (!selectedFile) { statusDiv.innerHTML = '<span style="color:red;">[!] ERROR: No file selected</span>'; return; }

            const formData = new FormData();
            formData.append('file', selectedFile);
            formData.append('token', token);

            statusDiv.innerHTML = '[*] Verifying token and staging payload...';

            try {
                const response = await fetch('/api/upload', { method: 'POST', body: formData });
                const data = await response.json();
                if (response.ok) {
                    statusDiv.innerHTML = `<span style="color:#00ff00;">[✓] ${data.message}</span>`;
                    selectedFile = null;
                    dropZone.innerHTML = `[ DRAG FILE HERE OR CLICK TO SELECT ]<br><br>Accepts: .txt, .pdf, .csv`;
                } else {
                    statusDiv.innerHTML = `<span style="color:red;">[!] DENIED: ${data.message}</span>`;
                }
            } catch (err) {
                statusDiv.innerHTML = `<span style="color:red;">[!] System Error during transfer.</span>`;
            }
        }
    </script>
</body>
</html>
"""

def retrieve_context(query_text: str) -> str:
    """
    Searches the local SQLite ledger for relevant information chunks.
    
    Splits the query into individual keywords and runs an SQL query to retrieve
    the top matching items from the chunk_ledger table to formulate system context.
    
    Args:
        query_text (str): Raw string containing user query keywords.
        
    Returns:
        str: Aggregated context text extracted from the database, or 'NO DATA FOUND.'
    """
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
        return "\n".join([row[0] for row in results])
    except sqlite3.Error:
         return "NO DATA FOUND."

@app.route('/')
def index():
    """
    Renders the primary web interface console.
    
    Returns:
        str: HTML template content.
    """
    return render_template_string(HTML_TEMPLATE)

@app.route('/api/query', methods=['POST'])
def handle_query():
    """
    Handles incoming JSON research queries.
    
    Retrieves local SQLite context matches and prompts the local Ollama LLM
    instance, returning the model's response.
    
    Returns:
        Response: JSON payload containing model's answer or error details.
    """
    user_query = request.json.get('query', '')
    context = retrieve_context(user_query)
    system_prompt = "You are a strict data extraction tool. Output ONLY facts found in the context. If 'NO DATA FOUND.', reply exactly with 'DATA NOT FOUND IN LEDGER.'"
    full_prompt = f"CONTEXT:\n{context}\n\nQUESTION: {user_query}\n\nANSWER:"
    try:
        response = ollama.chat(model=MODEL_NAME, messages=[
            {'role': 'system', 'content': system_prompt},
            {'role': 'user', 'content': full_prompt}
        ])
        return jsonify({'answer': response['message']['content']})
    except Exception as e:
        return jsonify({'answer': f"System Error: {e}"})

@app.route('/api/upload', methods=['POST'])
def handle_upload():
    """
    Validates token authorization and processes file ingestion payloads.
    
    Validates the authorization header/token. If authenticated, saves the uploaded
    file to the secure sync intake staging directory.
    
    Returns:
        Response: JSON status response indicating success or access denial.
    """
    token = request.form.get('token', '')
    if token not in VALID_TOKENS:
        print(f"[!] Unauthorized upload attempt blocked. Token: {token}")
        return jsonify({'message': 'Invalid Access Key. Connection severed.'}), 403

    if 'file' not in request.files:
        return jsonify({'message': 'No file part'}), 400
    
    file = request.files['file']
    if file.filename == '':
        return jsonify({'message': 'No selected file'}), 400

    if file:
        filename = secure_filename(file.filename)
        save_path = os.path.join(INTAKE_DIR, filename)
        file.save(save_path)
        print(f"[✓] Valid Token Received. Staging payload: {filename}")
        return jsonify({'message': 'Access Granted. Payload transferred to secure intake.'}), 200

if __name__ == '__main__':
    print("=" * 60)
    print(" SOVEREIGN COMMAND CENTER BOOTING")
    print(" Architecture: Token-Gated Payload Staging")
    print(" Access Dashboard at: http://0.0.0.0:8000")
    print("=" * 60)
    app.run(host='0.0.0.0', port=8000)
