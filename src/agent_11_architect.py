import os

print("\n" + "="*60)
print(" VANGUARD SECTOR 3: AGENT 11 (THE ARCHITECT) ONLINE ")
print("="*60 + "\n")

# The Dominion to Map
DOMINION_ROOT = os.path.expanduser("~/SovereignNexus/src/")
CROWN_DIR = os.path.expanduser("~/SovereignNexus/src/Sovereign_Crown/")
MAP_PATH = os.path.join(CROWN_DIR, "Dominion_Map.md")

print(f"[!] Agent 11 surveying topology of: {DOMINION_ROOT}")
print("[!] Forging the high-altitude Dominion Map...\n")

def generate_tree(dir_path, prefix=""):
    """Recursively builds an ASCII tree of the directory structure."""
    tree_str = ""
    try:
        # Sort directories first, then files
        entries = sorted(os.listdir(dir_path))
        entries = [e for e in entries if not e.startswith('.')] # Ignore hidden files/folders
        
        for i, entry in enumerate(entries):
            full_path = os.path.join(dir_path, entry)
            is_last = (i == len(entries) - 1)
            connector = "└── " if is_last else "├── "
            
            tree_str += prefix + connector + entry + "\n"
            
            if os.path.isdir(full_path):
                extension = "    " if is_last else "│   "
                tree_str += generate_tree(full_path, prefix + extension)
    except PermissionError:
        pass
    return tree_str

# Generate the topography
topology = f"# THE LINUX DOMINION: TOPOLOGICAL MAP\n"
topology += f"## Forged by Agent 11: The Architect\n\n"
topology += f"**Root:** `{DOMINION_ROOT}`\n\n```text\n"
topology += "SovereignNexus_Dominion/\n"
topology += generate_tree(DOMINION_ROOT)
topology += "```\n"

# Anchor the Map
with open(MAP_PATH, "w", encoding="utf-8") as f:
    f.write(topology)

print("="*60)
print(" THE ARCHITECT HAS SECURED THE TOPOLOGY ")
print(f" Dominion Map anchored at: {MAP_PATH}")
print("="*60 + "\n")
