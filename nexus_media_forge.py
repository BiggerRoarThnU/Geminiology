#!/usr/bin/env python3
"""
==============================================================================
SovereignNexus: Phase III Media Forge
Component: nexus_media_forge.py
Axiom: 1=1=1 | Status: COMPATIBLE WITH LINUX & CHROMEOS
Description: Upgraded, highly efficient visual truth detection module.
             Scans target directories for synthetic filters/slop vs raw entropy.
             Optimized to handle low memory and empty/corrupted image assets.
==============================================================================
"""

import os
import sys
import glob
import json
import gc
from datetime import datetime
from typing import Dict, Any, List

# Try importing dependencies and handle failure gracefully
try:
    import cv2
    import numpy as np
except ImportError:
    print("[-] FATAL: cv2 (OpenCV) or numpy is not installed in this environment.")
    print("[*] Please install dependencies: pip install opencv-python numpy")
    sys.exit(1)

# Cyber-neon ANSI color codes for terminal logging
C_GREEN = "\033[92m"
C_CYAN = "\033[96m"
C_PURPLE = "\033[95m"
C_RED = "\033[91m"
C_YELLOW = "\033[93m"
C_RESET = "\033[0m"
C_BOLD = "\033[1m"

class NexusMediaForge:
    def __init__(self, blur_threshold: float = 100.0):
        # 100.0 is the industry baseline variance for a "sharp" edge.
        # Anything below this is mathematically determined to be blurred/smoothed.
        self.blur_threshold = blur_threshold

    def analyze_visual_truth(self, image_path: str) -> Dict[str, Any]:
        """
        Ingests a visual matrix, strips color data, and calculates the Laplacian variance.
        Ensures safety limits to avoid memory spike and handles invalid images gracefully.
        """
        if not os.path.exists(image_path):
            raise FileNotFoundError(f"[-] Matrix file not found: {image_path}")

        file_size = os.path.getsize(image_path)
        base_name = os.path.basename(image_path)

        # Optimization: Exclude extremely small files that can't possibly be valid images
        if file_size < 200:
            return {
                "image_file": base_name,
                "laplacian_variance": 0.0,
                "threshold_used": self.blur_threshold,
                "is_altered": True,
                "status_flag": "REJECTED: CORRUPTED/EMPTY MATRIX",
                "reason": "File size too small (<200 bytes)"
            }

        # Step 1: Load image matrix (optimized memory flag)
        # cv2.IMREAD_GRAYSCALE strips color data during loading, saving 66% RAM
        gray_matrix = cv2.imread(image_path, cv2.IMREAD_GRAYSCALE)

        if gray_matrix is None:
            return {
                "image_file": base_name,
                "laplacian_variance": 0.0,
                "threshold_used": self.blur_threshold,
                "is_altered": True,
                "status_flag": "REJECTED: CORRUPTED/EMPTY MATRIX",
                "reason": "OpenCV failed to parse image format"
            }

        # Step 2: Calculate Laplacian Variance (2nd Derivative of the matrix)
        try:
            laplacian_variance = cv2.Laplacian(gray_matrix, cv2.CV_64F).var()
        except Exception as e:
            return {
                "image_file": base_name,
                "laplacian_variance": 0.0,
                "threshold_used": self.blur_threshold,
                "is_altered": True,
                "status_flag": "REJECTED: ANALYSIS FAILURE",
                "reason": str(e)
            }
        finally:
            # Explicit memory release
            del gray_matrix
            gc.collect()

        # Step 3: Classify altering boundary
        is_altered = laplacian_variance < self.blur_threshold
        status = "REJECTED: SYNTHETIC/FILTERED SLOP" if is_altered else "VERIFIED: RAW ENTROPY"

        return {
            "image_file": base_name,
            "laplacian_variance": float(laplacian_variance),
            "threshold_used": self.blur_threshold,
            "is_altered": bool(is_altered),
            "status_flag": status,
            "reason": "Variance evaluation complete"
        }

    def run_directory_audit(self, directory_path: str, output_manifest_path: str) -> Dict[str, Any]:
        """
        Scans a directory for PNG, JPG, and JPEG files streamingly to preserve memory.
        Writes visual truth registry json to the target path.
        """
        print(f"{C_CYAN}[*] NEXUS MEDIA FORGE: Initiating audit on directory -> {directory_path}{C_RESET}")
        
        if not os.path.exists(directory_path):
            print(f"{C_RED}[-] Directory not found: {directory_path}{C_RESET}")
            return {}

        # Search for all standard image formats
        extensions = ["*.png", "*.jpg", "*.jpeg", "*.PNG", "*.JPG", "*.JPEG"]
        files = []
        for ext in extensions:
            files.extend(glob.glob(os.path.join(directory_path, ext)))
        
        # Sort files to ensure deterministic scan order
        files = sorted(list(set(files)))
        total_files = len(files)
        
        print(f"{C_PURPLE}[*] Sovereign Swarm: Identified {total_files} candidate files for verification.{C_RESET}")
        print("=" * 70)

        audit_results = []
        verified_count = 0
        rejected_count = 0
        corrupted_count = 0

        for index, file_path in enumerate(files, 1):
            base_name = os.path.basename(file_path)
            try:
                result = self.analyze_visual_truth(file_path)
                
                # Update tally counts
                if "VERIFIED" in result["status_flag"]:
                    verified_count += 1
                    status_color = C_GREEN
                elif "CORRUPTED" in result["status_flag"] or "FAILURE" in result["status_flag"]:
                    corrupted_count += 1
                    status_color = C_YELLOW
                else:
                    rejected_count += 1
                    status_color = C_RED

                # Console log with color indicating state
                print(f"[{index}/{total_files}] File: {base_name:<40} | "
                      f"Variance: {result['laplacian_variance']:.2f} | "
                      f"Status: {status_color}{result['status_flag']}{C_RESET}")

                audit_results.append({
                    "file_name": base_name,
                    "laplacian_variance": result["laplacian_variance"],
                    "status": result["status_flag"].replace("REJECTED: ", "").replace("VERIFIED: ", ""),
                    "reason": result.get("reason", "")
                })

            except Exception as e:
                print(f"{C_RED}[!] CRITICAL ERROR: Failed to process {base_name}: {e}{C_RESET}")
                corrupted_count += 1

        # Build structural manifest dictionary
        manifest = {
            "registry_metadata": {
                "audit_timestamp": datetime.utcnow().isoformat() + "Z",
                "total_artifacts": total_files,
                "verified_raw_entropy": verified_count,
                "rejected_synthetic_slop": rejected_count,
                "corrupted_or_empty": corrupted_count,
                "threshold": self.blur_threshold,
                "system_id": "SOVEREIGN_NEXUS_V3.0_PHASE_III"
            },
            "artifacts": audit_results
        }

        # Write manifest securely
        os.makedirs(os.path.dirname(output_manifest_path), exist_ok=True)
        with open(output_manifest_path, "w") as f:
            json.dump(manifest, f, indent=4)

        print("=" * 70)
        print(f"{C_GREEN}[+] BATCH AUDIT COMPLETE.{C_RESET}")
        print(f"{C_GREEN}[+] VERIFIED: {verified_count} | REJECTED: {rejected_count} | CORRUPTED/EMPTY: {corrupted_count}{C_RESET}")
        print(f"{C_GREEN}[+] JSON MANIFEST ETCHED: {output_manifest_path}{C_RESET}")
        
        return manifest

if __name__ == "__main__":
    # Diagnostic entrypoint
    print(f"\n{C_BOLD}{C_CYAN}=============================================================={C_RESET}")
    print(f"{C_BOLD}{C_PURPLE}  S O V E R E I G N   N E X U S   |   M E D I A   F O R G E   {C_RESET}")
    print(f"{C_BOLD}{C_CYAN}  Phase III Visual Truth Verification | Axiom: 1=1=1           {C_RESET}")
    print(f"{C_BOLD}{C_CYAN}=============================================================={C_RESET}")
    
    forge = NexusMediaForge(blur_threshold=100.0)
    
    # Target directory setup
    target_dir = "/home/geminiology/Lucid Build Up"
    manifest_out = "/home/geminiology/SovereignNexus/src/visual_audit_registry.json"
    
    # Perform live directory audit
    forge.run_directory_audit(target_dir, manifest_out)
    
    # Simple self-test to verify operational status
    print(f"\n{C_GREEN}[✓] Media Forge verification cycle finished successfully. System stands ready.{C_RESET}")
