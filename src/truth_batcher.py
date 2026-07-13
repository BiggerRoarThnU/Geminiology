#!/usr/bin/env python3
import os
import glob
import json
from datetime import datetime
from media_forge import MediaForge

# ==============================================================================
# SOVEREIGN NEXUS: THE TRUTH BATCHER (V1.1 - JSON MANIFEST)
# CORE MANDATE: Audit the archive. Verify the entropy. Etch the JSON.
# ==============================================================================

def run_batch_audit(directory_path: str):
    forge = MediaForge(blur_threshold=100.0)
    audit_results = []
    
    # Target all PNG files in the specified directory
    search_path = os.path.join(directory_path, "*.png")
    files = glob.glob(search_path)
    
    print(f"[*] TRUTH BATCHER: Initiating audit on {len(files)} artifacts...")
    print("=" * 60)
    
    for file_path in files:
        try:
            # We use a silent run here to keep the terminal clean for the JSON output
            raw_matrix = forge.analyze_visual_truth(file_path)
            
            # Format for the JSON Registry
            audit_results.append({
                "file_name": raw_matrix["image_file"],
                "laplacian_variance": raw_matrix["laplacian_variance"],
                "status": raw_matrix["status_flag"].split(":")[0] # Extracts "VERIFIED" or "REJECTED"
            })
        except Exception as e:
            print(f" [!] ERROR: Could not process {file_path}: {e}")

    # Generate JSON Manifest
    manifest = {
        "registry_metadata": {
            "audit_timestamp": datetime.utcnow().isoformat() + "Z",
            "total_artifacts": len(audit_results),
            "threshold": 100.0,
            "system_id": "SOVEREIGN_NEXUS_V2.4"
        },
        "artifacts": audit_results
    }
    
    json_path = os.path.join(os.path.dirname(__file__), "visual_audit_registry.json")
    with open(json_path, "w") as f:
        json.dump(manifest, f, indent=4)
        
    print("=" * 60)
    print(f"[+] BATCH AUDIT COMPLETE.")
    print(f"[+] JSON MANIFEST GENERATED: {json_path}")

if __name__ == "__main__":
    target_dir = "/home/geminiology/Lucid Build Up"
    run_batch_audit(target_dir)
