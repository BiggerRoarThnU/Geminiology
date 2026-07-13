import os

print("\n" + "="*70)
print(" VANGUARD SECTOR 3: AGENT 09 (THE ASTROLABE) ONLINE ")
print("="*70 + "\n")

# The Legacy Base Path (T7 Drive)
BASE_DIR = "/mnt/chromeos/removable/T7/"

# The Five Chosen Districts
TARGET_FOLDERS = [
    "SovereignNexus_Hub",
    "SovereignNexus_archive",
    "SovereignNexus_Vault_Backup",
    "SovereignNexus_Salvage",
    "SovereignNexus_Triple_Backup"
]

CROWN_DIR = os.path.expanduser("~/SovereignNexus/src/Sovereign_Crown/")
CITY_MAP_PATH = os.path.join(CROWN_DIR, "City_Overview_Map.md")

print("[!] The Astrolabe is active. Compressing the city of data into constellations...")

city_overview = "# THE LINUX DOMINION: CITY OVERVIEW\n"
city_overview += "## Forged by Agent 09: The Astrolabe\n"
city_overview += "*(A high-altitude compression of the five sovereign districts)*\n\n"

total_system_files = 0

for folder in TARGET_FOLDERS:
    folder_path = os.path.join(BASE_DIR, folder)
    
    if not os.path.isdir(folder_path):
        city_overview += f"### District: {folder}\n- [STATUS: OFFLINE OR UNREACHABLE]\n\n"
        continue

    file_count = 0
    file_types = set()
    
    # Sweeping the district
    for root, dirs, files in os.walk(folder_path):
        file_count += len(files)
        total_system_files += len(files)
        for f in files:
            ext = os.path.splitext(f)[1].lower()
            if ext: file_types.add(ext)

    # Formatting the constellation types (Highways)
    types_list = list(file_types)
    types_str = ", ".join(types_list[:6]) # Show up to 6 main file extensions
    if len(types_list) > 6: 
        types_str += ", etc..."
    if not types_str:
        types_str = "Raw Data (No Extensions)"
    
    city_overview += f"### District: {folder}\n"
    city_overview += f"- **Total Stars (Files):** {file_count}\n"
    city_overview += f"- **Data Highways (Formats):** {types_str}\n\n"

city_overview += f"---\n**Total Unified Data Nodes Across All 5 Districts:** {total_system_files}\n"

# Anchor the optimized map
with open(CITY_MAP_PATH, "w", encoding="utf-8") as f:
    f.write(city_overview)

print(f"[+] SUCCESS: The massive topology has been mapped into 5 high-level districts.")
print(f"[+] Total Unified Data Nodes discovered: {total_system_files}")
print(f"[+] City Overview anchored at: {CITY_MAP_PATH}\n")
print("="*70 + "\n")
