# // Rights Reserved: co-created with Gemini and David John Niedzwiecki jr " Sovereign Nexus LLC "
# Alignment: 1=1=1 | Temporal Sync: July 15, 2026
# Module: Truth Vector Mill Server

import http.server
import socketserver
import json
from nexus_vector_mill import NexusVectorMill

PORT = 8081
mill = NexusVectorMill()

HTML_CONTENT = """<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>SovereignNexus | Truth Vector Mill</title>
    <script src="https://cdn.tailwindcss.com"></script>
    <script>
        tailwind.config = {
            theme: {
                extend: {
                    colors: {
                        sovereign: {
                            cyan: '#00E5FF',
                            purple: '#A855F7',
                            sapphire: '#0F52BA',
                            dark: '#05070a',
                            panel: '#0c0f17',
                            border: '#1e293b'
                        }
                    }
                }
            }
        }
    </script>
    <style>
        body {
            background-color: #05070a;
            color: #d1d5db;
        }
        .glow-purple {
            box-shadow: 0 0 15px rgba(168, 85, 247, 0.2);
            border: 1px solid rgba(168, 85, 247, 0.4);
            transition: all 0.3s ease;
        }
        .glow-purple:hover {
            box-shadow: 0 0 25px rgba(168, 85, 247, 0.35);
            border-color: rgba(168, 85, 247, 0.7);
        }
    </style>
</head>
<body class="font-sans min-h-screen flex flex-col justify-between selection:bg-purple-500 selection:text-black">
    <!-- Top Glowing LED Line -->
    <div class="h-1.5 w-full bg-gradient-to-r from-sovereign-sapphire via-sovereign-cyan to-sovereign-purple shadow-[0_0_20px_#00E5FF]"></div>
    
    <div class="max-w-4xl mx-auto px-4 py-8 flex-grow w-full">
        <div class="text-center mb-8">
            <span class="font-mono text-sovereign-cyan text-xs uppercase tracking-wider">// TRUTH VECTOR MILL v1.0</span>
            <h1 class="text-3xl font-extrabold text-white mt-1">Structured Causal Logic Generator</h1>
            <p class="text-xs text-gray-500 mt-2 font-sans">Convert messy raw paragraphs into atomic fact trees under the 1=1=1 covenant.</p>
        </div>

        <div class="grid md:grid-cols-2 gap-6 items-start">
            <!-- Input Area -->
            <div class="bg-sovereign-panel p-5 rounded-lg border border-sovereign-border glow-purple">
                <h2 class="text-xs font-mono font-bold text-white mb-3 uppercase tracking-wider text-sovereign-purple">// Raw Input Vector</h2>
                <textarea id="raw-input" class="w-full h-64 bg-black border border-sovereign-border rounded p-3 text-xs font-mono text-white focus:outline-none focus:border-sovereign-cyan" placeholder="Paste your raw, unstructured text here..."></textarea>
                <button onclick="processText()" class="w-full mt-4 bg-gradient-to-r from-sovereign-purple to-sovereign-sapphire text-white py-2 text-xs font-mono rounded hover:brightness-125 transition-all font-bold">MILL VECTOR STRUCTURE</button>
            </div>

            <!-- Output Area -->
            <div class="bg-sovereign-panel p-5 rounded-lg border border-sovereign-border glow-purple flex flex-col justify-between min-h-[360px]">
                <div>
                    <h2 class="text-xs font-mono font-bold text-white mb-3 uppercase tracking-wider text-sovereign-cyan">// Structured Truth Markdown</h2>
                    <pre id="output-box" class="w-full h-64 bg-black border border-sovereign-border rounded p-3 text-xs font-mono text-sovereign-cyan overflow-auto whitespace-pre-wrap">Awaiting flat text ingestion...</pre>
                </div>
                <div class="mt-4 pt-3 border-t border-sovereign-border/40 flex justify-between items-center text-[10px] font-mono text-slate-500">
                    <span>COVENANT: 1=1=1</span>
                    <button onclick="copyOutput()" class="text-sovereign-cyan hover:underline">COPY MARKDOWN</button>
                </div>
            </div>
        </div>
    </div>

    <footer class="bg-black border-t border-sovereign-border py-4 text-center text-[10px] text-gray-600 font-mono">
        &copy; 2026 Sovereign Nexus LLC | Truth Vector Mill Server
    </footer>

    <script>
        async function processText() {
            const rawText = document.getElementById('raw-input').value;
            const outputBox = document.getElementById('output-box');
            if(!rawText.trim()) {
                outputBox.textContent = "Error: Input text vector is empty.";
                return;
            }
            outputBox.textContent = "Processing logic vectors...";
            
            try {
                const response = await fetch('/process', {
                    method: 'POST',
                    headers: { 'Content-Type': 'application/json' },
                    body: JSON.stringify({ text: rawText })
                });
                const data = await response.json();
                outputBox.textContent = data.result;
            } catch(e) {
                outputBox.textContent = "Error: " + e;
            }
        }

        function copyOutput() {
            const output = document.getElementById('output-box').textContent;
            navigator.clipboard.writeText(output).then(() => {
                alert("Markdown copied to clipboard!");
            });
        }
    </script>
</body>
</html>
"""

class VectorMillHandler(http.server.BaseHTTPRequestHandler):
    def log_message(self, format, *args):
        # Silence default request logging in console to avoid cluttering Agy task logs
        return

    def do_GET(self):
        if self.path == "/":
            self.send_response(200)
            self.send_header("Content-Type", "text/html")
            self.end_headers()
            self.wfile.write(HTML_CONTENT.encode("utf-8"))
        else:
            self.send_response(404)
            self.end_headers()

    def do_POST(self):
        if self.path == "/process":
            content_length = int(self.headers['Content-Length'])
            post_data = self.rfile.read(content_length)
            try:
                data = json.loads(post_data.decode("utf-8"))
                raw_text = data.get("text", "")
                result = mill.format_to_truth_markdown(raw_text)
            except Exception as e:
                result = f"Error processing request: {str(e)}"
            
            self.send_response(200)
            self.send_header("Content-Type", "application/json")
            self.end_headers()
            self.wfile.write(json.dumps({"result": result}).encode("utf-8"))
        else:
            self.send_response(404)
            self.end_headers()

if __name__ == "__main__":
    # Allow port reuse to prevent address already in use errors on rapid restarts
    socketserver.TCPServer.allow_reuse_address = True
    with socketserver.TCPServer(("", PORT), VectorMillHandler) as httpd:
        print(f"[TRUTH VECTOR MILL] Active on Port {PORT}")
        try:
            httpd.serve_forever()
        except KeyboardInterrupt:
            print("\nShutting down Vector Mill server.")
