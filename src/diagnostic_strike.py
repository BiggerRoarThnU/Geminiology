import time
from vampire_engine import VampireEngine

# Target function requiring strict types and a nested dictionary
def process_federated_data(node_id: int, security_clearance: str, telemetry: dict):
    return f"Node {node_id} [{security_clearance}] Telemetry Verified."

print("==================================================")
print(" DIAGNOSTIC STRIKE : RECURSIVE FORGE & LIVE UI")
print("==================================================")

# Initialize Engine (This will trigger the Immortality Protocol / Resurrection)
vampire = VampireEngine()

# Intentional Slop: node_id is a string, but the function demands an integer
slop_payload = {
    "node_id": "8080", 
    "security_clearance": "LEVEL_5_CLEARANCE",
    "telemetry": {"status": "ACTIVE", "packet_loss": "0.0"}
}

print("\n[!] Firing Complex Payload...")
vampire.route_dictionary_pass(process_federated_data, slop_payload)

print("\n[+] Strike Complete. Switch over to your browser to verify the visual pulse.")
