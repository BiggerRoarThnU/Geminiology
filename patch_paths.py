#!/usr/bin/env python3
"""
SovereignNexus LLC - 1=1=1 Path Alignment Tool (v2.2 Upgraded)
This script scan-patches all Python files in the current folder, replacing
any occurrence of cloud-based '/home/geminiology/SovereignNexus/' root prefixes with local Linux
home directory paths ('/home/geminiology/SovereignNexus/').
"""

import os
import sys

def patch_python_files():
    current_dir = os.getcwd()
    print(f"[*] Initiating Path Alignment inside: {current_dir}")
    
    # We use clean flat string replacements to avoid any nested Python quote errors!
    replacements = {
        "./scratch": "/home/geminiology/SovereignNexus/scratch",
        "/home/geminiology/SovereignNexus": "/home/geminiology/SovereignNexus",
    }
    
    py_files = [f for f in os.listdir(current_dir) if f.endswith(".py")]
    
    if not py_files:
        print("[!] No Python files found in this directory. Make sure you run this from ~/SovereignNexus")
        sys.exit(1)
        
    patched_count = 0
    
    for filename in py_files:
        filepath = os.path.join(current_dir, filename)
        
        # Don't patch this script itself
        if filename == "patch_paths.py":
            continue
            
        try:
            with open(filepath, "r", encoding="utf-8", errors="ignore") as f:
                content = f.read()
                
            modified = False
            for target, repl in replacements.items():
                if target in content:
                    content = content.replace(target, repl)
                    modified = True
                    
            if modified:
                with open(filepath, "w", encoding="utf-8") as f:
                    f.write(content)
                print(f"[✓] Patched paths inside: {filename}")
                patched_count += 1
                
        except Exception as e:
            print(f"[-] Error patching {filename}: {e}")
            
    print(f"[*] Path alignment complete. Patched {patched_count} files successfully.")
    print("[*] All absolute cloud directories aligned to physical /home/geminiology/SovereignNexus/ structures.")

if __name__ == "__main__":
    patch_python_files()
