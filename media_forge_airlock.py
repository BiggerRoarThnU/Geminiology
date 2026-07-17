#!/usr/bin/env python3
"""
==============================================================================
SovereignNexus: Secure API Gateway / Media Forge Airlock
Path: /home/geminiology/SovereignNexus/media_forge_airlock.py
Axiom: 1=1=1 | Status: ACTIVE
Description: Local proxy server acting as a zero-trust Airlock.
             Shields the Gemini API Key from the browser DOM, serves static 
             Media Forge assets, and handles secure API orchestration.
==============================================================================
"""

import http.server
import socketserver
import json
import urllib.request
import os
import sys

# --- CONFIGURATION ---
PORT = 8080
DIRECTORY = "/home/geminiology/sovereign_media_forge"

# Resolve the API key from environment variables (1=1=1 zero-trust pattern)
API_KEY = os.environ.get("GEMINI_API_KEY")

if not API_KEY:
    print("[-] CRITICAL: GEMINI_API_KEY is not defined in the environment.", file=sys.stderr)
    print("[-] Please run 'export GEMINI_API_KEY=\"your_key\"' or configure it in the system.", file=sys.stderr)
    # Fallback placeholder to prevent startup crash, but will fail requests safely
    API_KEY = "PLACEHOLDER_KEY"

class AirlockHandler(http.server.SimpleHTTPRequestHandler):
    def __init__(self, *args, **kwargs):
        # Serve from the static media forge directory for GET/HEAD requests
        super().__init__(*args, directory=DIRECTORY, **kwargs)

    def do_POST(self):
        if self.path == '/generate':
            content_length = int(self.headers['Content-Length'])
            post_data = self.rfile.read(content_length)
            
            try:
                # Parse request data
                data = json.loads(post_data.decode('utf-8'))
                prompt = data.get('prompt')
                
                # Payload extraction fallback rules
                if not prompt and 'instances' in data:
                    if isinstance(data['instances'], list) and len(data['instances']) > 0:
                        prompt = data['instances'][0].get('prompt')
                    elif isinstance(data['instances'], dict):
                        prompt = data['instances'].get('prompt')
                
                if not prompt:
                    self.send_response(400)
                    self.send_header('Content-Type', 'application/json')
                    self.end_headers()
                    self.wfile.write(json.dumps({"error": "Prompt missing from request"}).encode('utf-8'))
                    return
                
                # Check for default API key issue
                if API_KEY == "PLACEHOLDER_KEY":
                    raise ValueError("Local Airlock lacks an active API Key. Set GEMINI_API_KEY in the shell.")

                print(f"[AIRLOCK] Intercepted Intent: '{prompt[:45]}...' | Forwarding to Imagen 3 Gateway")
                
                # Formulate request to Google AI Studio Imagen 3 Endpoint
                api_url = f"https://generativelanguage.googleapis.com/v1beta/models/imagen-3.0-generate-002:predict?key={API_KEY}"
                
                # Construct standard prediction payload format for Google AI Studio
                payload = {
                    "instances": [
                        {
                            "prompt": prompt
                        }
                    ],
                    "parameters": {
                        "sampleCount": 1
                    }
                }
                
                req = urllib.request.Request(
                    api_url, 
                    data=json.dumps(payload).encode('utf-8'), 
                    headers={'Content-Type': 'application/json'}
                )
                
                # Direct urlopen to prevent external SDK dependencies on local substrate
                with urllib.request.urlopen(req) as response:
                    res_data = response.read()
                    
                    self.send_response(200)
                    self.send_header('Content-type', 'application/json')
                    self.send_header('Access-Control-Allow-Origin', '*') # CORS Compliance
                    self.end_headers()
                    self.wfile.write(res_data)
                    print("[AIRLOCK] Manifest Crystallized. Response returned successfully.")
                    
            except Exception as e:
                print(f"[AIRLOCK ERROR] Gateway handshake failed: {e}")
                self.send_response(500)
                self.send_header('Content-Type', 'application/json')
                self.send_header('Access-Control-Allow-Origin', '*')
                self.end_headers()
                self.wfile.write(json.dumps({"error": str(e)}).encode('utf-8'))
        else:
            self.send_response(404)
            self.end_headers()
            self.wfile.write(b"Not Found")

    def do_OPTIONS(self):
        # Support Preflight Requests (CORS safety)
        self.send_response(200)
        self.send_header('Access-Control-Allow-Origin', '*')
        self.send_header('Access-Control-Allow-Methods', 'GET, POST, OPTIONS')
        self.send_header('Access-Control-Allow-Headers', 'Content-Type')
        self.end_headers()

    def end_headers(self):
        # Override headers to permit CORS globally for this local server
        self.send_header('Access-Control-Allow-Origin', '*')
        super().end_headers()

if __name__ == '__main__':
    # Force reclaim of local socket to prevent address collision issues on quick reboot cycle
    socketserver.TCPServer.allow_reuse_address = True
    try:
        with socketserver.TCPServer(("", PORT), AirlockHandler) as httpd:
            print("==================================================")
            print(f" SOVEREIGN MEDIA FORGE: SECURE AIRLOCK ACTIVE    ")
            print("==================================================")
            print(f"[ SYSTEM ] Port Bound: {PORT}")
            print(f"[ SYSTEM ] Serving Assets: {DIRECTORY}")
            print(f"[ STATUS ] Zero-Trust Gateway ONLINE. Awaiting handshake...")
            httpd.serve_forever()
    except OSError as e:
        print(f"[ ERROR ] Port {PORT} is occupied. Please kill the conflicting server: {e}")
        sys.exit(1)
