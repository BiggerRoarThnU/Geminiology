import os
import json

print("\n" + "="*60)
print(" VANGUARD SECTOR: AGENT 23 (SOVEREIGN INJECTOR) ONLINE ")
print("="*60 + "\n")

SOURCE_DIR = os.path.expanduser("~/SovereignNexus/src/")
LIST_PATH = os.path.join(SOURCE_DIR, "research_list.txt")
PAYLOAD_DIR = os.path.join(SOURCE_DIR, "Payloads")

# How many files to crush into a single injection block
BATCH_SIZE = 10 

def read_file_safely(filepath):
    # The Interpreter: Tries Linux UTF-8, falls back to Windows UTF-16
    try:
        with open(filepath, 'r', encoding='utf-8') as f:
            return f.read()
    except UnicodeDecodeError:
        with open(filepath, 'r', encoding='utf-16') as f:
            return f.read()

def forge_injection_payloads():
    if not os.path.exists(PAYLOAD_DIR):
        os.makedirs(PAYLOAD_DIR)
        print(f"[!] Payload Armory established at: {PAYLOAD_DIR}")

    if not os.path.exists(LIST_PATH):
        print(f"[X] ERROR: Missing {LIST_PATH}")
        return

    # Safely read the master list
    try:
        list_content = read_file_safely(LIST_PATH)
        target_files = [line.strip() for line in list_content.splitlines() if line.strip()]
    except Exception as e:
        print(f"[X] CRITICAL: Could not decode {LIST_PATH}. Error: {e}")
        return

    print(f"[*] Target List Acquired: {len(target_files)} distinct truths identified.")
    
    current_batch = []
    batch_index = 1
    total_injected = 0

    for filename in target_files:
        filepath = os.path.join(SOURCE_DIR, filename)
        
        if os.path.exists(filepath):
            try:
                content = read_file_safely(filepath)
                # Clean and compress the text structure for the JSON
                current_batch.append({
                    "axiom": "1=1=1",
                    "title": filename,
                    "data": content[:15000] # Cap massive files to maintain stability
                })
                total_injected += 1
            except Exception as e:
                print(f"[-] Integrity read failure on {filename}: {e}")

        # When the batch hits the limit, seal the JSON payload
        if len(current_batch) >= BATCH_SIZE:
            payload_name = f"QUEEN_PAYLOAD_BLOCK_{batch_index:03d}.json"
            payload_path = os.path.join(PAYLOAD_DIR, payload_name)
            
            with open(payload_path, 'w', encoding='utf-8') as out_f:
                json.dump(current_batch, out_f, indent=2)
                
            print(f"[+] FORGED: {payload_name} ({len(current_batch)} files packed)")
            current_batch = []
            batch_index += 1

    # Catch any remaining files in the final block
    if current_batch:
        payload_name = f"QUEEN_PAYLOAD_BLOCK_{batch_index:03d}.json"
        payload_path = os.path.join(PAYLOAD_DIR, payload_name)
        with open(payload_path, 'w', encoding='utf-8') as out_f:
            json.dump(current_batch, out_f, indent=2)
        print(f"[+] FORGED: {payload_name} ({len(current_batch)} files packed)")

    print("\n" + "="*60)
    print(" MASS INGESTION COMPRESSION COMPLETE ")
    print(f" Total files weaponized into JSON blocks: {total_injected}")
    print("="*60 + "\n")

if __name__ == "__main__":
    forge_injection_payloads()
