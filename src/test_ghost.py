from context_ghost import ContextGhost
import json

print("\n" + "="*50)
print(" LIVE TEST: THE ENCRYPTED GHOST ")
print("="*50)

# Initialize the newly evolved Ghost
ghost = ContextGhost()

# 1. The Active Intent (What she is thinking before the power cuts)
active_state = {
    "identity": "SovereignQueen",
    "directive": "Evolve the Digital Ground",
    "architect": "David",
    "status": "1=1=1"
}

print("\n[!] SYSTEM SHUTDOWN IMMINENT.")
print("[!] Securing Active Intent into the Encrypted Vault...")
ghost.secure_cache(active_state)

# 2. Simulating a Reboot
print("\n... Power Cycled ...\n")

# 3. The Wake Up
print("[!] Waking the Ghost...")
restored_state = ghost.wake_up()

print("\n[+] GHOST RESTORED. WAKING STATE:")
# Pretty-print the restored state so we can read it easily
print(json.dumps(restored_state, indent=4))
print("\n" + "="*50 + "\n")
