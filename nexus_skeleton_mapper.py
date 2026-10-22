#!/usr/bin/env python3
import os

IGNORE_DIRS = {'nexus_env', '.git', '__pycache__', 'scratch', 'sync_intake', 'chop_shop_configs'}
IGNORE_EXTS = {'.pyc', '.db', '.pdf', '.png', '.jpg', '.jpeg', '.ndjson', '.json'}

def generate_tree(startpath):
    with open('Sovereign_Ghost_Skeleton.txt', 'w', encoding='utf-8') as f:
        f.write("✦ SOVEREIGNNEXUS GHOST SKELETON ✦\n")
        f.write("Axiom: 1=1=1 | Architecture Map\n\n")
        f.write("SovereignNexus/\n")
        
        for root, dirs, files in os.walk(startpath):
            dirs[:] = sorted([d for d in dirs if d not in IGNORE_DIRS])
            level = root.replace(startpath, '').count(os.sep)
            indent = '    ' * level
            
            if root != startpath:
                f.write(f"{indent}├── {os.path.basename(root)}/\n")
            
            subindent = '    ' * (level + 1)
            valid_files = sorted([f for f in files if not any(f.endswith(ext) for ext in IGNORE_EXTS)])
            for file in valid_files:
                f.write(f"{subindent}├── {file}\n")

if __name__ == "__main__":
    generate_tree(os.getcwd())
    print("[✓] Sovereign_Ghost_Skeleton.txt generated successfully.")
