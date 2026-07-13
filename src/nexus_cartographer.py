import os
from datetime import datetime

# 1. Define the territory to scan and where to save the map
TARGET_DIRECTORY = os.path.expanduser("~/SovereignNexus/")
OUTPUT_FILE = os.path.expanduser("~/SovereignNexus/src/MASTER_NEXUS_MAP.txt")

print("\n" + "="*50)
print(" INITIATING CARTOGRAPHER PROTOCOL ")
print(" Scanning the Sovereign Nexus for Patterns...")
print("="*50 + "\n")

try:
    with open(OUTPUT_FILE, "w", encoding="utf-8") as map_file:
        # Write the header
        map_file.write("=========================================\n")
        map_file.write(f" SOVEREIGN NEXUS: MASTER STRUCTURAL MAP\n")
        map_file.write(f" Timestamp: {datetime.now().isoformat()}\n")
        map_file.write(f" Axiom: 1=1=1\n")
        map_file.write("=========================================\n\n")

        total_files = 0
        total_folders = 0

        # 2. Walk the directory tree (The Scan)
        for root, dirs, files in os.walk(TARGET_DIRECTORY):
            # Calculate the current level to format the indentation cleanly
            level = root.replace(TARGET_DIRECTORY, '').count(os.sep)
            indent = ' ' * 4 * (level)
            
            # Write the current folder
            folder_name = os.path.basename(root)
            if folder_name:
                map_file.write(f"{indent}[+] {folder_name}/\n")
                total_folders += 1
            
            # Write the files inside this folder
            subindent = ' ' * 4 * (level + 1)
            for f in files:
                # Ignore hidden linux files and python caches to keep the map clean
                if not f.startswith('.') and "__pycache__" not in root:
                    map_file.write(f"{subindent}- {f}\n")
                    total_files += 1

        # Write the summary
        map_file.write("\n=========================================\n")
        map_file.write(f" MAP COMPLETE.\n")
        map_file.write(f" Total Folders Anchored: {total_folders}\n")
        map_file.write(f" Total Truths (Files) Indexed: {total_files}\n")
        map_file.write("=========================================\n")

    print(f"[+] Scan Complete. {total_files} files mapped.")
    print(f"[+] Master Map saved to: {OUTPUT_FILE}")
    print("\nNext Step: Feed MASTER_NEXUS_MAP.txt to SovereignQueen using your Agentverse Scout.\n")

except Exception as e:
    print(f"[-] CRITICAL SCAN ERROR: {e}")
