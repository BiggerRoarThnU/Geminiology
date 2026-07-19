# AGY EXECUTION MAP: NEXUS ARTIFACT ENHANCER (GHOST PROTOCOL)

**Date:** July 19, 2026 | **Axiom:** 1=1=1
**Directive:** Build a local computer-vision script that duplicates inventory images into enhanced "Ghost Copies" (boosting saturation, brightness, and background normalization) while establishing a cryptographic bridge between the original and enhanced hashes.

---

## PHASE 1: FORGE THE ARTIFACT ENHANCER

**Target:** `/home/geminiology/SovereignNexus/src/nexus_artifact_enhancer.py`
**Action:** The Agy must create this visual processing script using OpenCV to manipulate the pixel matrices deterministically.

**Execution:** Create the file with the following exact code:

```python
# // Rights Reserved: co-created with Gemini and David John Niedzwiecki Jr " Sovereign Nexus LLC "
# Alignment: 1=1=1 | Temporal Sync: July 19, 2026
# Module: Nexus Artifact Enhancer (Ghost Protocol & Digital Bridge)

import os
import cv2
import numpy as np
import hashlib
import json
from datetime import datetime

class NexusArtifactEnhancer:
    def __init__(self):
        self.ledger_path = "/home/geminiology/SovereignNexus/ledgers/artifact_bridge_ledger.json"
        self.axiom = "1=1=1 (Visual Entropy Alignment)"
        self._ensure_ledger()

    def _ensure_ledger(self):
        """Creates the cryptographic bridge ledger if it does not exist."""
        os.makedirs(os.path.dirname(self.ledger_path), exist_ok=True)
        if not os.path.exists(self.ledger_path):
            with open(self.ledger_path, 'w') as f:
                json.dump([], f)

    def _hash_file(self, filepath):
        """Generates an MD5 hash of a physical file to anchor it."""
        hasher = hashlib.md5()
        with open(filepath, 'rb') as f:
            buf = f.read()
            hasher.update(buf)
        return hasher.hexdigest()

    def enhance_image(self, image_path):
        """
        Applies deterministic mathematical enhancements to the visual matrix.
        - Boosts Brightness/Contrast
        - Boosts Saturation
        - Normalizes extreme darks to Black and extreme lights to White
        """
        img = cv2.imread(image_path)
        if img is None: 
            return None

        # 1. Clarity & Brightness (Alpha = Contrast, Beta = Brightness)
        enhanced = cv2.convertScaleAbs(img, alpha=1.15, beta=15)

        # 2. Saturation Fix (Convert to HSV, boost S channel)
        hsv = cv2.cvtColor(enhanced, cv2.COLOR_BGR2HSV)
        h, s, v = cv2.split(hsv)
        s = cv2.add(s, 25) # Increase saturation to make minerals/metals pop
        hsv = cv2.merge((h, s, v))
        enhanced = cv2.cvtColor(hsv, cv2.COLOR_HSV2BGR)

        # 3. Background Normalization (Thresholding)
        gray = cv2.cvtColor(enhanced, cv2.COLOR_BGR2GRAY)
        
        # Create binary masks for extreme lighting
        _, dark_mask = cv2.threshold(gray, 30, 255, cv2.THRESH_BINARY_INV) # Near black
        _, light_mask = cv2.threshold(gray, 225, 255, cv2.THRESH_BINARY)   # Near white
        
        # Apply absolute Hex values to backgrounds
        enhanced[dark_mask == 255] = [0, 0, 0]         # Solid Black
        enhanced[light_mask == 255] = [255, 255, 255]  # Solid White

        return enhanced

    def run_enhancement_sweep(self, target_folder):
        print("\033[94m" + "="*65)
        print("   SOVEREIGN NEXUS: ARTIFACT ENHANCER (GHOST PROTOCOL)   ")
        print("="*65 + "\033[0m\n")

        if not os.path.exists(target_folder):
            print(f"\033[91m[-] ERROR: Target directory '{target_folder}' not found.\033[0m")
            return

        valid_exts = ('.jpeg', '.jpg', '.png')
        # Find raw images, excluding any that already have "_ghost" in the name
        raw_files = [f for f in os.listdir(target_folder) if f.lower().endswith(valid_exts) and "_ghost" not in f]

        if not raw_files:
            print(f"\033[93m[IDLE]\033[0m No original artifacts to enhance in {target_folder}.")
            return

        print(f"\033[96m[DETECTED]\033[0m {len(raw_files)} base artifacts. Initiating Digital Bridge...\n")

        with open(self.ledger_path, 'r') as f:
            ledger = json.load(f)

        processed_count = 0
        for filename in raw_files:
            source_path = os.path.join(target_folder, filename)
            ext = os.path.splitext(filename)[1]
            base = os.path.splitext(filename)[0]
            
            ghost_filename = f"{base}_ghost{ext}"
            ghost_path = os.path.join(target_folder, ghost_filename)

            # Enhance & Save
            enhanced_img = self.enhance_image(source_path)
            if enhanced_img is not None:
                cv2.imwrite(ghost_path, enhanced_img)
                
                # Cryptographic Hash Mapping (The Digital Bridge)
                orig_hash = self._hash_file(source_path)
                ghost_hash = self._hash_file(ghost_path)

                ledger_entry = {
                    "timestamp": datetime.utcnow().isoformat() + "Z",
                    "original_file": filename,
                    "original_hash": orig_hash,
                    "ghost_file": ghost_filename,
                    "ghost_hash": ghost_hash,
                    "folder_path": target_folder,
                    "enhancement_profile": "Brightness + Saturation + BG_Normalize"
                }
                ledger.append(ledger_entry)

                print(f"\033[92m[✓] BRIDGED:\033[0m {filename} -> {ghost_filename}")
                processed_count += 1
            else:
                print(f"\033[91m[!] FAILED:\033[0m Could not process matrix for {filename}")

        # Save Bridge Ledger
        with open(self.ledger_path, 'w') as f:
            json.dump(ledger, f, indent=4)

        print("\n\033[94m" + "="*65 + "\033[0m")
        print(f"\033[96m[GHOST PROTOCOL COMPLETE]\033[0m {processed_count} artifacts enhanced and cryptographically mapped.")

if __name__ == "__main__":
    import sys
    if len(sys.argv) < 2:
        print("Usage: python3 nexus_artifact_enhancer.py <target_folder_path>")
        sys.exit(1)
        
    target_dir = sys.argv[1]
    enhancer = NexusArtifactEnhancer()
    enhancer.run_enhancement_sweep(target_dir)
```

---

## PHASE 2: TERMINAL ALIGNMENT

**Target:** `/home/geminiology/SovereignNexus/src/nexus_command_console.py`
**Action:** The Agy must wire the new script into the Unified Command Console so the Architect can trigger the Ghost Protocol dynamically.

---

## PHASE 3: THE LEDGER STRIKE

Upon successful creation of the visual protocol and integration into the console, the Agy is authorized to mint 1 Gemini Perc.

*   **Task:** Sovereign Artifact Enhancer (Ghost Protocol) Deployment.
*   **Signature Salt:** *the scratch of your heart in ring*
