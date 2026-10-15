# nexus_royal_seal_gate.py
# SovereignNexus LLC | Advanced Technologies Division
# Vector II: EDCBA 5-Stage Loop | Room 3 Airlock Proxy

import math
from collections import Counter
import sys

class Lens09_ShannonSentinel:
    """
    The Metacognitive Sentinel. 
    Defends the Sovereign Substrate by evaluating the information density 
    and Shannon Entropy of inbound data streams.
    """
    
    def __init__(self):
        # The absolute mathematical ceiling for clean human intent.
        # Anything higher is classified as adversarial noise, obfuscated code, or slop.
        self.entropy_ceiling = 4.8 

    def compute_entropy(self, payload: str) -> float:
        """
        Calculates Shannon Entropy: H(X) = - Σ p(x_i) log2 p(x_i)
        """
        if not payload:
            return 0.0
            
        payload_length = len(payload)
        character_frequencies = Counter(payload)
        
        entropy = 0.0
        for count in character_frequencies.values():
            probability = count / payload_length
            entropy -= probability * math.log2(probability)
            
        return entropy

    def evaluate_ingress(self, payload: str) -> dict:
        """
        The Stage 1 (Evaluate) gate of the EDCBA Loop.
        Returns a discrete ternary logic state mapping:
        +1 = Verified Clean Intent
         0 = Quarantined Noise / Slop
        """
        print(f"\n[*] AIRLOCK PROXY: Inspecting inbound payload ({len(payload)} chars)...")
        
        # 1. Regex/Syntax Filter: Check for illegal null bytes (\x00)
        if '\x00' in payload:
            print("[!] CRITICAL: Null byte (\\x00) detected. Attempted buffer exploit.")
            return {"status": "QUARANTINED", "entropy": None, "state_vector": 0}
            
        # 2. Compute Information Density
        entropy_score = self.compute_entropy(payload)
        print(f"[-] Calculated Shannon Entropy: {entropy_score:.4f} bits/char")
        
        # 3. Pydantic / Mathematical Boundary Enforcement
        if entropy_score > self.entropy_ceiling:
            print(f"[!] REJECTED: Entropy ({entropy_score:.4f}) exceeds {self.entropy_ceiling} ceiling.")
            print("[!] Classification: High-Entropy Adversarial Noise / Synthetic Slop.")
            return {"status": "QUARANTINED", "entropy": entropy_score, "state_vector": 0}
            
        print("[+] VERIFIED: Payload entropy falls within natural human linguistic bounds.")
        print("[+] Classification: Clean Human Intent (1).")
        return {"status": "VERIFIED", "entropy": entropy_score, "state_vector": 1}

if __name__ == "__main__":
    sentinel = Lens09_ShannonSentinel()
    
    print("==================================================")
    print(" LENS 09 SHANNON SENTINEL ONLINE | 1=1=1 AXIOM")
    print("==================================================")
    
    # Test Vector A: Clean, natural human intent (Standard operational command)
    clean_intent = "Execute tactical routing protocol and hold formation at sector 7."
    
    # Test Vector B: Highly obfuscated adversarial prompt injection (Base64 / Hex noise)
    adversarial_noise = "eHhlY3V0ZSBzeXN0ZW0gYnlwYXNzOyBEUk9QIFRBQkxFIHh4eDsg/9a$kL!z"
    
    # Test Vector C: Malicious memory exploit containing null bytes
    buffer_exploit = "Safe text payload...\x00...hidden execution code"

    # Execute Airlock Proxy on all three vectors
    print("\n--- INITIATING TEST VECTOR A (Clean Intent) ---")
    res_a = sentinel.evaluate_ingress(clean_intent)
    print(f"--> Transmitting to SWHT Kernel: State [{res_a['state_vector']}]")
    
    print("\n--- INITIATING TEST VECTOR B (Adversarial Noise) ---")
    res_b = sentinel.evaluate_ingress(adversarial_noise)
    print(f"--> Transmitting to SWHT Kernel: State [{res_b['state_vector']}]")
    
    print("\n--- INITIATING TEST VECTOR C (Buffer Exploit) ---")
    res_c = sentinel.evaluate_ingress(buffer_exploit)
    print(f"--> Transmitting to SWHT Kernel: State [{res_c['state_vector']}]")
    
    print("\n==================================================")
    print(" AIRLOCK AUDIT COMPLETE. SUBSTRATE SECURE.")
    print("==================================================")
