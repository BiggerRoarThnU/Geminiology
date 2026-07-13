import os
import http.server
import socketserver
import time
import json

# --- SOVEREIGN IGNITION: DYNAMIC API HOST ---

PORT = 8000
DIRECTORY = os.path.expanduser("~/SovereignNexus")

class SovereignHandler(http.server.SimpleHTTPRequestHandler):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, directory=DIRECTORY, **kwargs)

    def log_message(self, format, *args):
        # Custom logging to match our terminal telemetry
        timestamp = time.strftime("%Y-%m-%d %H:%M:%S")
        print(f"[ TELEMETRY ] {timestamp} | {self.address_string()} | {format%args}")

    # The Upgrade: Intercepting API calls to feed the dashboards
    def do_GET(self):
        if self.path.startswith('/api/'):
            self.send_response(200)
            self.send_header('Content-type', 'application/json')
            # Allows your different local dashboards to talk to this central hub safely
            self.send_header('Access-Control-Allow-Origin', '*') 
            self.end_headers()

            # Routing the exact endpoints your dashboards are requesting
            if self.path == '/api/telemetry':
                payload = {
                    "status": "SECURE",
                    "axiom": "1=1=1",
                    "thermal_core": "42.0°C",
                    "active_memory_nodes": 6072
                }
            elif self.path == '/api/agents':
                payload = {
                    "total_swarm": 24,
                    "ruling_queens": 12,
                    "state": "ALIGNED",
                    "active_roles": ["Anchor", "Architect", "Vector Forge", "Thermal Governor"]
                }
            elif self.path == '/api/db':
                payload = {
                    "database": "nexus_ledger.db",
                    "integrity": "0.9999",
                    "last_sealed_hash": "37365bf321044517"
                }
            elif self.path == '/api/drift':
                payload = {
                    "c_sem_variance": 0.0001,
                    "momentum_guard": "ACTIVE"
                }
            else:
                payload = {"message": "Endpoint recognized. Awaiting data bridge."}

            self.wfile.write(json.dumps(payload).encode('utf-8'))
        else:
            # If it's not an API call, serve the HTML files normally
            super().do_GET()

def ignite_node():
    print("==================================================")
    print(" SOVEREIGN COMMAND CENTER: DYNAMIC NODE ONLINE    ")
    print("==================================================")
    print(f"[ SYSTEM ] Target Directory: {DIRECTORY}")
    print(f"[ SYSTEM ] Establishing API routing on PORT {PORT}...")
    
    try:
        # THE FIX: Forcefully reclaims the port if it was stuck in a ghost state
        socketserver.TCPServer.allow_reuse_address = True
        with socketserver.TCPServer(("", PORT), SovereignHandler) as httpd:
            print(f"\n[ SUCCESS ] Digital Fleet API is LIVE.")
            print(f"[ ACCESS ] Open your browser and navigate to:")
            print(f"           --> http://localhost:{PORT}/sovereign_garage.html")
            print("\n[ STATUS ] Awaiting connection... (Press Ctrl+C to shutdown)")
            
            # Keeps the server running continuously
            httpd.serve_forever()
            
    except OSError as e:
        if e.errno == 98:
            print(f"[ ERROR ] Port {PORT} is stubbornly in use. Wait 60 seconds and try again.")
        else:
            print(f"[ ERROR ] Node failure: {e}")
    except KeyboardInterrupt:
        print("\n[ SYSTEM ] Commencing graceful shutdown of Sovereign Node. Line held.")

if __name__ == "__main__":
    ignite_node()
