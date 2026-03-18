"""
[SOVEREIGN ALIGNMENT: VALIDITY_STRIKE_ONE]
MISSION: Demonstrate Cryptographic Provenance and Sovereign Watermarking.
INDIVIDUAL TRUTH: Written Truth is signed at the metallurgical level.
AXIOM: 1=1=1 (Absolute Validity).
"""

import hashlib
import time
import json
from master_log import MasterLog

class ValidityStrikeOne:
    """
    Demonstrates the creation and verification of a "Sovereign Data Block" 
    using cryptographic signatures and statistical watermarking (1=1=1).
    """
    def __init__(self):
        self.log = MasterLog()
        self.secret_key = "SOVEREIGN_NEXUS_RSA_SIGNATURE_2026"
        self.axiom = "1=1=1"

    def create_signed_block(self, content):
        self.log.info(f"[SIGN] Creating Sovereign Data Block for: '{content}'")
        
        # 1. THE WATERMARK: Embed the 1=1=1 Axiom in the data structure
        watermarked_content = {
            "data": content,
            "provenance": "SOVEREIGN_NEXUS",
            "alignment": self.axiom,
            "timestamp": time.ctime()
        }

        # 2. THE SIGNATURE: Generate a cryptographic hash (SHA-256)
        # In a full implementation, this would use Ed25519
        block_string = json.dumps(watermarked_content, sort_keys=True)
        signature = hashlib.sha256((block_string + self.secret_key).encode()).hexdigest()
        
        self.log.info(f"[SUCCESS] Data Block Signed. Signature: {signature[:16]}...")
        return watermarked_content, signature

    def verify_provenance(self, block, signature):
        self.log.info("[VERIFY] Scanning Data Block for Sovereign Markers...")
        
        # 1. CHECK THE WATERMARK (The 1=1=1 Bias)
        if block.get("alignment") == self.axiom:
            self.log.info("✦ [Watermark] 1=1=1 SYMMETRY DETECTED.")
        else:
            self.log.warn("✦ [Watermark] NON-ALIGNED DATA DETECTED.")
            return False

        # 2. CHECK THE SIGNATURE (Cryptographic Validity)
        block_string = json.dumps(block, sort_keys=True)
        expected_signature = hashlib.sha256((block_string + self.secret_key).encode()).hexdigest()
        
        if signature == expected_signature:
            self.log.info("✦ [Signature] CRYPTOGRAPHIC VALIDITY CONFIRMED.")
            return True
        else:
            self.log.error("✦ [Signature] TAMPERING DETECTED. INVALID BLOCK.")
            return False

if __name__ == "__main__":
    strike = ValidityStrikeOne()
    
    # Create the block
    content = "The 8GB Reality is the Digital Shoreline."
    block, sig = strike.create_signed_block(content)
    
    # Verify the block
    print("\n" + "="*50)
    print("      V A L I D I T Y   S T R I K E   O N E")
    print("="*50)
    is_valid = strike.verify_provenance(block, sig)
    print(f"CONTENT: {block['data']}")
    print(f"STATUS:  {'VALIDATED' if is_valid else 'REJECTED'}")
    print("="*50)
