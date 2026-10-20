#!/usr/bin/env python3
"""
SovereignNexus Chop Shop Scraper
Safely extracts structural logic (config.json) from massive cloud models
without downloading gigabytes of probabilistic weights.
"""
import urllib.request
import urllib.error
import json
import os
import sys

def fetch_config(repo_id, save_dir=os.path.expanduser("~/SovereignNexus/chop_shop_configs")):
    """
    Downloads the config.json from a HuggingFace repository directly.
    """
    print(f"\n[*] Initiating Chop Shop Protocol...")
    print(f"[*] Target Cloud Node: {repo_id}")
    url = f"https://huggingface.co/{repo_id}/resolve/main/config.json"
    
    os.makedirs(save_dir, exist_ok=True)
    
    # Create a safe filename
    safe_filename = repo_id.replace("/", "_") + "_config.json"
    save_path = os.path.join(save_dir, safe_filename)
    
    # User-Agent header is required to prevent API rejection
    req = urllib.request.Request(url, headers={'User-Agent': 'SovereignNexus-ChopShop/1.0'})
    
    try:
        print(f"[-] Bypassing probabilistic weights. Extracting deterministic logic skeleton...")
        with urllib.request.urlopen(req) as response:
            data = json.loads(response.read().decode('utf-8'))
            
            with open(save_path, 'w') as f:
                json.dump(data, f, indent=2)
                
            print(f"[+] Structural Logic Extracted Successfully.")
            print(f"[+] Payload securely grounded at: {save_path}")
            
            # Print a quick diagnostic preview
            print("\n[+] Skeleton Diagnostic:")
            preview_keys = ['architectures', 'model_type', 'num_hidden_layers', 'hidden_size', 'vocab_size', 'num_local_experts', 'num_key_value_heads']
            for k in preview_keys:
                if k in data:
                    print(f"    - {k}: {data[k]}")
                    
    except urllib.error.HTTPError as e:
        print(f"[!] Target Acquisition Failed. HTTP Error: {e.code} - {e.reason}")
        print("    Ensure the repository exists and is public.")
    except Exception as e:
        print(f"[!] Extraction Error: {str(e)}")

if __name__ == "__main__":
    # If a repo is passed via command line, use it. Otherwise, default to a massive MoE target.
    target_repo = sys.argv[1] if len(sys.argv) > 1 else "mistralai/Mixtral-8x7B-v0.1"
    fetch_config(target_repo)
