import time
from vampire_engine import VampireEngine

# The target tool requiring strict types
def generate_bulk_invoice(client_email: str, amount_usd: float, invoice_id: int):
    return f"Verified Invoice {invoice_id} for {client_email} at ${amount_usd:.2f}"

print("==================================================")
print(" VAMPIRE ENGINE: STRESS TEST & MERKLE CHAIN FORGE")
print("==================================================")

# Initialize the engine
vampire = VampireEngine()

# Fire 5 rapid strikes
for i in range(1, 6):
    print(f"\n[!] INITIATING STRIKE {i}/5...")
    
    # Simulating incoming "slop" from a drifting agent
    incoming_slop = {
        "client_email": f"nexus_node_{i}@nc_b2b.local",
        "amount_usd": str(125.50 * i),  # String instead of float
        "invoice_id": str(5000 + i)     # String instead of int
    }

    # The Vampire intercepts, coerces, and logs
    vampire.route_dictionary_pass(generate_bulk_invoice, incoming_slop)
    time.sleep(0.5) # Brief thermodynamic throttle between strikes

print("\n[+] FORGE COMPLETE. The Merkle Chain has been anchored.")
