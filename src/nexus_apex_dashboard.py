#!/usr/bin/env python3
"""
SovereignNexus APEX Command Center
Live visual telemetry for the Ghost-Twin Inference Engine.
"""
import os
import sys
from flask import Flask, request, jsonify
import numpy as np

from nexus_phase_retriever import query_verified_context
from nexus_holographic_hopfield import SovereignHolographicMemory
from nexus_spatial_indexer import compute_wave_metrics
from nexus_ghost_infer import evaluate_ghost_twin, query_fleet_model

app = Flask(__name__)

memory = SovereignHolographicMemory(n_modes=256)
ref_bits = np.unpackbits(np.frombuffer("1=1=1 Deterministic Truth".encode("utf-8"), dtype=np.uint8))
ref_modes = np.zeros(256, dtype=float)
ref_modes[:min(len(ref_bits), 256)] = ref_bits[:min(len(ref_bits), 256)] * np.pi
memory.store(ref_modes)

HTML_TEMPLATE = """
<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>APEX Command Center</title>
    <style>
        :root { --bg: #0a0a0c; --panel: #111116; --text: #e0e0e0; --accent: #00ffcc; --alert: #ff3366; --fault: #ff9900; }
        body { background-color: var(--bg); color: var(--text); font-family: 'Courier New', Courier, monospace; margin: 0; padding: 20px; display: flex; flex-direction: column; align-items: center; }
        .dashboard { width: 100%; max-width: 1200px; display: grid; grid-template-columns: 1fr 1fr; gap: 20px; }
        .panel { background: var(--panel); border: 1px solid #333; padding: 20px; border-radius: 8px; box-shadow: 0 4px 20px rgba(0,0,0,0.5); }
        .full-width { grid-column: 1 / -1; }
        
        .logo {
            font-size: 2.5em;
            font-weight: bold;
            text-align: center;
            margin-bottom: 20px;
            background: linear-gradient(270deg, #ff0000, #ff7f00, #ffff00, #00ff00, #0000ff, #4b0082, #8b00ff);
            background-size: 400% 400%;
            -webkit-background-clip: text;
            -webkit-text-fill-color: transparent;
            animation: RainbowGlow 8s ease infinite;
            filter: drop-shadow(0px 0px 10px rgba(255, 255, 255, 0.2));
        }
        @keyframes RainbowGlow { 0%{background-position:0% 50%} 50%{background-position:100% 50%} 100%{background-position:0% 50%} }
        
        input[type="text"] { width: 100%; padding: 15px; background: #000; border: 1px solid var(--accent); color: var(--accent); font-family: inherit; font-size: 1.1em; border-radius: 4px; box-sizing: border-box; outline: none;}
        input:disabled { opacity: 0.5; border-color: #555; color: #555; }
        button { margin-top: 10px; width: 100%; padding: 15px; background: var(--accent); color: #000; font-weight: bold; font-family: inherit; font-size: 1.1em; border: none; border-radius: 4px; cursor: pointer; text-transform: uppercase; letter-spacing: 2px; transition: 0.2s; }
        button:hover:not(:disabled) { background: #00cca3; box-shadow: 0 0 15px var(--accent); }
        button:disabled { background: #555; cursor: not-allowed; box-shadow: none; }
        
        .telemetry { font-size: 0.9em; color: #888; }
        .telemetry span { color: var(--accent); font-weight: bold; }
        .quarantine span { color: var(--alert); }
        .log-box { height: 300px; overflow-y: auto; background: #000; padding: 15px; border: 1px solid #333; font-size: 0.9em; white-space: pre-wrap; }
    </style>
</head>
<body>
    <div class="logo">SOVEREIGN_NEXUS APEX</div>
    
    <div class="dashboard">
        <div class="panel full-width">
            <h3>[ TRANSMIT INTENT ]</h3>
            <input type="text" id="queryInput" placeholder="Enter query or test data..." onkeydown="handleEnter(event)">
            <button id="btnEngage" onclick="sendQuery()">Engage Ghost-Twin</button>
        </div>
        
        <div class="panel">
            <h3>[ WAVE TELEMETRY ]</h3>
            <div id="telemetryData" class="telemetry">Awaiting signal...</div>
        </div>
        
        <div class="panel">
            <h3>[ FLEET OUTPUT ]</h3>
            <div id="fleetOutput" class="log-box">System ready.</div>
        </div>
    </div>

    <script>
        function handleEnter(event) {
            if (event.key === 'Enter') {
                event.preventDefault();
                sendQuery();
            }
        }

        async function sendQuery() {
            const inputField = document.getElementById('queryInput');
            const btn = document.getElementById('btnEngage');
            const input = inputField.value;
            
            if (!input) return;
            
            inputField.disabled = true;
            btn.disabled = true;
            btn.innerText = "[ CALCULATING... ]";
            
            const outputBox = document.getElementById('fleetOutput');
            const telemetryBox = document.getElementById('telemetryData');
            
            outputBox.innerHTML = "[*] Routing signal through 3D Phase-Space Manifold...\\n[*] Awaiting Ollama Fleet Response...";
            telemetryBox.innerHTML = "Calculating C_seq Phase and Shannon Entropy...";
            
            try {
                const response = await fetch('/api/infer', {
                    method: 'POST',
                    headers: { 'Content-Type': 'application/json' },
                    body: JSON.stringify({ query: input })
                });
                
                if (!response.ok) {
                    throw new Error(`Server returned status: ${response.status}`);
                }
                
                const data = await response.json();
                
                let telHtml = `<p>Input Length: <span>${data.metrics.length} bytes</span></p>
                               <p>Spectral Coherence (Y): <span class="${data.metrics.spec_coh > 0.40 ? 'quarantine' : ''}">${data.metrics.spec_coh.toFixed(4)}</span></p>
                               <p>Shannon Entropy (Z): <span class="${data.metrics.entropy < (data.metrics.length > 15 ? 0.20 : 0.05) ? 'quarantine' : ''}">${data.metrics.entropy.toFixed(4)}</span></p>
                               <p>Gate Status: <span style="color: ${data.status === 1 ? 'var(--accent)' : 'var(--alert)'}">${data.diagnostic}</span></p>`;
                
                if (data.context && data.context.length > 0) {
                    telHtml += `<p>Context Nodes Anchored: <span>${data.context.length}</span></p>`;
                }
                telemetryBox.innerHTML = telHtml;
                
                if (data.status === -2) {
                    outputBox.innerHTML = `<span style="color: var(--fault);">[!] SYSTEM FAULT ENFORCED.</span>\\n\\n${data.diagnostic}\\n\\nExecution halted. No output generated.`;
                } else if (data.status <= 0) {
                    outputBox.innerHTML = `<span style="color: var(--alert);">[!] QUARANTINE LOCKDOWN ENFORCED.</span>\\n\\n${data.diagnostic}\\n\\nProbabilistic drift refused. System held at Temp 0.0.`;
                } else {
                    outputBox.innerHTML = `[+] FLEET RESPONSE:\\n\\n${data.response}`;
                }
            } catch (error) {
                outputBox.innerHTML = `<span style="color: var(--alert);">[!] Local API Connection Error.</span>\\n${error.message}\\nCheck terminal logs.`;
                telemetryBox.innerHTML = `<span style="color: var(--alert);">Telemetry Sync Failed</span>`;
            }
            
            inputField.disabled = false;
            btn.disabled = false;
            btn.innerText = "Engage Ghost-Twin";
            inputField.focus();
        }
    </script>
</body>
</html>
"""

@app.route("/")
def index():
    return HTML_TEMPLATE

@app.route("/api/infer", methods=["POST"])
def api_infer():
    try:
        data = request.json
        query_text = data.get("query", "")
        
        c_bias, spec_coh, entropy = compute_wave_metrics(query_text)
        metrics = {
            "length": len(query_text),
            "spec_coh": spec_coh,
            "entropy": entropy
        }
        
        status, diagnostic = evaluate_ghost_twin(query_text, memory)
        
        if status <= 0:
            return jsonify({"status": status, "diagnostic": diagnostic, "metrics": metrics})
            
        try:
            verified_nodes = query_verified_context(min_entropy=0.35, max_spectral_coherence=0.25, limit=3)
        except Exception as e:
            print(f"[!] Context Retrieval Error: {e}")
            verified_nodes = []
        
        if verified_nodes:
            context_str = "\n".join([f"- {node[1]}" for node in verified_nodes])
            prompt = f"Context:\n{context_str}\n\nDirective:\n{query_text}\n\nDeterministic Truth Output:"
        else:
            prompt = f"Directive:\n{query_text}\n\nDeterministic Truth Output:"
            
        success, fleet_response = query_fleet_model(prompt)
        
        # If fleet fails, return special status -2 to explicitly trigger UI fault logic
        if not success:
            return jsonify({
                "status": -2,
                "diagnostic": fleet_response,
                "metrics": metrics,
                "context": [n[1] for n in verified_nodes] if verified_nodes else []
            })
            
        return jsonify({
            "status": status,
            "diagnostic": diagnostic,
            "metrics": metrics,
            "context": [n[1] for n in verified_nodes] if verified_nodes else [],
            "response": fleet_response
        })
    except Exception as e:
        print(f"[ERROR] API Infer failed: {str(e)}")
        return jsonify({"error": str(e)}), 500

if __name__ == "__main__":
    print("\n[*] APEX COMMAND CENTER INITIALIZING...")
    print("[*] 1=1=1 Axiom Verified. Starting local server on PORT 5051.")
    app.run(host="0.0.0.0", port=5051, debug=False)
