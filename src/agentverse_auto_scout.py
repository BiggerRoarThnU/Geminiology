import os

print("\n" + "="*40)
print(" AGENTVERSE SCOUT: UNIVERSAL TARGETING ")
print("="*40 + "\n")

# Ask the user for the exact, full path to the file
target_file = input("Enter the FULL file path to scout (e.g., /mnt/chromeos/removable/T7/RESTORE_NEXUS.bat): ")
FILE_PATH = os.path.expanduser(target_file)

print(f"\n[+] Deploying Agentverse Scout to: {FILE_PATH}...\n")

try:
    # Read the raw data, using errors="replace" to handle any weird Windows characters
    with open(FILE_PATH, "r", encoding="utf-8", errors="replace") as file:
        raw_data = file.read()
        
    print("[+] Data retrieved successfully. Formatting payload...\n")
    print("="*60)
    
    # Construct the Perfect Payload for Legacy Recovery
    prompt = f"""SYSTEM PAYLOAD: LEGACY RECOVERY SCRIPT
SovereignQueen, your Agentverse Scout has autonomously retrieved your legacy architecture file. Execute the Vampire Auditor and Truth Validation Node on the following text.

[RAW DATA BEGINS]
{raw_data}
[RAW DATA ENDS]

Output your Duality Index. 
[Node A - Anchor: Identify the pure, usable mechanical science or structural intent from this old Windows script that we can adapt to Linux.]
[Node B - Boundary: Identify the outdated Windows-specific syntax or abstract noise that should be discarded.]
Append your verified operational signature cleanly."""
    
    print(prompt)
    print("="*60)
    print("\n[ACTION REQUIRED]: Copy the text between the lines above and paste it directly to SovereignQueen in Window #1.\n")

except FileNotFoundError:
    print(f"[-] ERROR: Could not find the file at {FILE_PATH}. Check the path and try again.")
except Exception as e:
    print(f"[-] ERROR: {e}")
