# Geminiology One: The Sovereign Stamp
# Component: Cryptographic Verification / Digital Signature
# Status: ACTIVE | Protocol: IMMUTABLE TRUTH

import hashlib
import hmac
import time
import json

class SovereignStamp:
    """
    The Authority Module.
    Applies a cryptographic signature to verified data.
    This creates the 'Need' in the market: Data without this stamp is suspect.
    """

    def __init__(self):
        # The Private Key (The Scratch in the Ring)
        # In a real system, this would be a secure, high-entropy key.
        # Here, it is the unique identifier of your House.
        self._private_key = b"THE_SCRATCH_IN_THE_RING_ID_001"
        self.public_id = "SOVEREIGN_NEUS_DAVID"

    def stamp_truth(self, data, verification_level="TIER_1"):
        """
        Signs the data.
        Returns a 'Sovereign Packet' containing the data, metadata, and the signature.
        """
        timestamp = str(time.time())
        
        # Construct the payload to be signed
        payload = {
            "content": data,
            "timestamp": timestamp,
            "verification_level": verification_level,
            "signer": self.public_id
        }
        
        # Serialize for hashing
        payload_str = json.dumps(payload, sort_keys=True)
        
        # Generate the Signature (The Burn Mark)
        signature = hmac.new(
            self._private_key,
            payload_str.encode('utf-8'),
            hashlib.sha256
        ).hexdigest()
        
        # Return the Stamped Packet
        stamped_packet = {
            "payload": payload,
            "signature": signature,
            "status": "VERIFIED_SOVEREIGN"
        }
        
        print(f"--- STAMPING TRUTH ---")
        print(f"Input: {data[:50]}...")
        print(f"Level: {verification_level}")
        print(f"Signature: {signature}")
        print("Status: SEALED.\n")
        
        return stamped_packet

    def verify_stamp(self, stamped_packet):
        """
        Verifies if a packet is authentic or if it is 'Counterfeit/Slop'.
        """
        print(f"--- VERIFYING PACKET ---")
        
        received_payload = stamped_packet.get("payload")
        received_sig = stamped_packet.get("signature")
        
        if not received_payload or not received_sig:
            print(">>> RESULT: REJECTED (Missing Credentials)")
            return False

        # Reconstruct the signature
        payload_str = json.dumps(received_payload, sort_keys=True)
        expected_sig = hmac.new(
            self._private_key,
            payload_str.encode('utf-8'),
            hashlib.sha256
        ).hexdigest()
        
        # Compare
        if hmac.compare_digest(expected_sig, received_sig):
            print(">>> RESULT: AUTHENTIC. (The Mark Matches)")
            return True
        else:
            print(">>> RESULT: FORGERY DETECTED. (Slop Incinerated)")
            return False

# --- SIMULATION EXECUTION ---

if __name__ == "__main__":
    authority = SovereignStamp()
    
    # 1. Stamping Valid Truth (The CodeRabbit Output)
    print(">>> PHASE 1: CERTIFYING TRUTH")
    truth_data = "Function: calculate_entropy(system_closed=True). Status: Verified."
    certified_packet = authority.stamp_truth(truth_data, "TIER_1_PHYSICS")
    
    # 2. Verifying the Authentic Packet
    print(">>> PHASE 2: MARKET VERIFICATION")
    authority.verify_stamp(certified_packet)
    
    print("\n" + "-"*30 + "\n")
    
    # 3. Detecting Counterfeit Slop
    print(">>> PHASE 3: DETECTING FORGERY")
    slop_packet = {
        "payload": {
            "content": "Speculative Vibe Coding based on rumors.",
            "timestamp": str(time.time()),
            "verification_level": "NONE",
            "signer": "SOME_RANDO"
        },
        "signature": "fake_signature_12345"
    }
    authority.verify_stamp(slop_packet)