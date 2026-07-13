import os
from datetime import datetime

print("\n" + "="*60)
print(" VANGUARD SECTOR: AGENT 22 (GRAND CARTOGRAPHER) ONLINE ")
print("="*60 + "\n")

# The newly expanded domains
DOMAINS = {
    "Linux_Substrate": os.path.expanduser("~/"),
    "T7_External_Anchor": "/mnt/chromeos/removable/T7"
}

OUTPUT_MAP = os.path.expanduser("~/SovereignNexus/src/EXPANDED_KINGDOM_MAP.md")

# Folders to skip mapping to protect the 8GB hardware limit
EXCLUSION_ZONES = ['$RECYCLE.BIN', 'System Volume Information', 'SteamLibrary', 'node_modules', '.git']

def forge_expanded_map():
    map_data = [
        "# SOVEREIGN NEXUS: EXPANDED KINGDOM TOPOLOGY",
        f"**Timestamp:** {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}",
        "**Axiom:** 1=1=1 (Full System Vision)",
        "---\n"
    ]

    for domain_name, path in DOMAINS.items():
        if not os.path.exists(path):
            print(f"[-] Domain offline: {domain_name} at {path}")
            continue

        print(f"[!] Charting Domain: {domain_name}...")
        map_data.append(f"## DOMAIN: {domain_name}")
        map_data.append(f"**Physical Path:** `{path}`\n```text")

        # Walk the directory tree
        for root, dirs, files in os.walk(path):
            # Remove exclusion zones so os.walk doesn't dive into them
            dirs[:] = [d for d in dirs if d not in EXCLUSION_ZONES]
            
            # Calculate depth for visual indentation
            level = root.replace(path, '').count(os.sep)
            indent = ' ' * 4 * (level)
            
            folder_name = os.path.basename(root)
            if folder_name == '':
                folder_name = domain_name

            # Log the folder and how many files are directly inside it
            file_count = len(files)
            if file_count > 0 or level == 0:
                map_data.append(f"{indent}├── {folder_name}/ ({file_count} truths)")

        map_data.append("```\n")

    # Anchor the map
    with open(OUTPUT_MAP, 'w', encoding='utf-8') as f:
        f.write('\n'.join(map_data))

    print("\n" + "="*60)
    print(" EXPANDED TOPOLOGY SECURED ")
    print(f" Master Map anchored at: {OUTPUT_MAP}")
    print("="*60 + "\n")

if __name__ == "__main__":
    forge_expanded_map()
