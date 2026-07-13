#!/usr/bin/env python3
import cv2
import numpy as np
import os
from typing import Dict, Any

# ==============================================================================
# SOVEREIGN NEXUS: THE MEDIA FORGE (V1.0 - VISUAL TRUTH DETECTION)
# CORE MANDATE: Strip visual noise, calculate pixel entropy, expose the Slop.
# ==============================================================================

class MediaForge:
    def __init__(self, blur_threshold: float = 100.0):
        # 100.0 is the industry baseline variance for a "sharp" edge. 
        # Anything below this is mathematically determined to be blurred/smoothed.
        self.blur_threshold = blur_threshold

    def analyze_visual_truth(self, image_path: str) -> Dict[str, Any]:
        """
        Ingests a visual matrix, strips color data, and calculates the Laplacian variance
        to determine if the image entropy has been artificially smoothed (filtered).
        """
        print(f"[*] MEDIA FORGE: Ingesting target matrix -> {image_path}")
        
        if not os.path.exists(image_path):
            raise FileNotFoundError(f"[-] FATAL: Image matrix not found at {image_path}")

        # Step 1: Load image and strip color data (Grayscale)
        raw_image = cv2.imread(image_path)
        gray_matrix = cv2.cvtColor(raw_image, cv2.COLOR_BGR2GRAY)

        # Step 2: The Laplacian Strike (Calculate the 2nd Derivative of the matrix)
        laplacian_variance = cv2.Laplacian(gray_matrix, cv2.CV_64F).var()
        
        # Step 3: Determine the Truth Boundary
        is_altered = laplacian_variance < self.blur_threshold
        status = "REJECTED: SYNTHETIC/FILTERED SLOP" if is_altered else "VERIFIED: RAW ENTROPY"

        print(f"[+] Variance Score: {laplacian_variance:.2f}")
        print(f"[+] Status: {status}")

        # Return a strictly typed dictionary ready for Vampire Engine ingestion
        return {
            "image_file": os.path.basename(image_path),
            "laplacian_variance": float(laplacian_variance),
            "threshold_used": self.blur_threshold,
            "is_altered": bool(is_altered),
            "status_flag": status
        }

if __name__ == "__main__":
    # Diagnostic test of the Media Forge blade
    forge = MediaForge()
    print("--- Simulating Media Forge Diagnostic ---")
    print("To run a live test, provide a valid image path.")
    # Example usage:
    # result = forge.analyze_visual_truth("test_selfie.jpg")
    # print(result)
