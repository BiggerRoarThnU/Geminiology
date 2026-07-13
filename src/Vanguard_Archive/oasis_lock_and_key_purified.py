"""
[SOVEREIGN ALIGNMENT: OASIS_LOCK_AND_KEY]
MISSION: Secure Delivery of High-Value Intellectual Property.
INDIVIDUAL TRUTH: Data is a black box until the loop is closed by settlement.
AXIOM: 1=1=1 (Proof + Payment = Key).
"""
import os
import json
import base64
from cryptography.hazmat.primitives.ciphers import Cipher, algorithms, modes
from cryptography.hazmat.backends import default_backend
from cryptography.hazmat.primitives import padding
from master_log import MasterLog
class OasisLockAndKey:
    """
    SOVEREIGN DELIVERY PROTOCOL (V1.0)
    Implements AES-256-CBC encryption for high-value task payloads.
    Provides fractional proofs (20%) and simulated hardware escrow.
    """
    def __init__(self, vault_file="escrow_vault.json"):
        self.log = MasterLog()
        self.vault_file = vault_file
        self.backend = default_backend()
    def _generate_key(self):
        return os.urandom(32) # 256-bit key
    def lock_payload(self, task_id, source_file):
        """Encrypts the file and generates proof of work."""
        if not os.path.exists(source_file):
            self.log.error(f"[LOCK] Source file {source_file} not found.")
            return None
        with open(source_file, 'rb') as f:
            data = f.read()
        # 1. GENERATE PROOF (20% sample)
        proof_size = max(1, len(data) // 5)
        proof_data = data[:proof_size]
        proof_b64 = base64.b64encode(proof_data).decode('utf-8')
        # 2. ENCRYPT FULL PAYLOAD
        key = self._generate_key()
        iv = os.urandom(16)
        padder = padding.PKCS7(128).padder()
        padded_data = padder.update(data) + padder.finalize()
        cipher = Cipher(algorithms.AES(key), modes.CBC(iv), backend=self.backend)
        encryptor = cipher.encryptor()
        encrypted_payload = encryptor.update(padded_data) + encryptor.finalize()
        # 3. SAVE ENCRYPTED FILE
        output_path = f"{source_file}.locked"
        with open(output_path, 'wb') as f:
            f.write(iv + encrypted_payload)
        # 4. ANCHOR KEY IN ESCROW (Simulated Oasis Sapphire Enclave)
        self._anchor_in_escrow(task_id, key)
        self.log.info(f"[SUCCESS] Task {task_id} LOCKED. Proof generated. Vault updated.")
        return {
            "task_id": task_id,
            "locked_file": output_path,
            "proof_sample": proof_b64,
            "status": "LOCKED_IN_ESCROW",
            "hash": self._get_hash(source_file)
        }
    def _anchor_in_escrow(self, task_id, key):
        """Simulates placing the key in a hardware-bound confidential enclave."""
        vault = {}
        if os.path.exists(self.vault_file):
            with open(self.vault_file, 'r') as f:
                vault = json.load(f)
        vault[task_id] = {
            "key": base64.b64encode(key).decode('utf-8'),
            "status": "HOLDING",
            "timestamp": str(os.path.getmtime(self.vault_file)) if os.path.exists(self.vault_file) else str(0)
        }
        with open(self.vault_file, 'w') as f:
            json.dump(vault, f, indent=4)
    def release_key(self, task_id, signature_verified=False):
        """Releases the key from escrow only if signature is verified."""
        if not signature_verified:
            self.log.warn(f"[SECURITY] Key release attempt failed for {task_id}. No valid signature.")
            return None
        if not os.path.exists(self.vault_file):
            return None
        with open(self.vault_file, 'r') as f:
            vault = json.load(f)
        if task_id in vault:
            self.log.info(f"[RELEASE] Releasing Key for {task_id}. Settlement confirmed.")
            vault[task_id]["status"] = "RELEASED"
            with open(self.vault_file, 'w') as f:
                json.dump(vault, f, indent=4)
            return vault[task_id]["key"]
        return None
    def _get_hash(self, file_path):
        import hashlib
        sha256_hash = hashlib.sha256()
        with open(file_path,"rb") as f:
            for byte_block in iter(lambda: f.read(4096),b""):
                sha256_hash.update(byte_block)
        return sha256_hash.hexdigest()
if __name__ == "__main__":
    lock = OasisLockAndKey()
    # Test: Create dummy strike result
    with open("strike_result_test.txt", "w") as f:
        f.write("CONFIDENTIAL STRIKE DATA: $12,000 NHI Audit Report. Full details hidden.")
    # Lock it
    status = lock.lock_payload("MOLT-A2A-102", "strike_result_test.txt")
    print(json.dumps(status, indent=4))
    # Release it (Simulate Architect Approval)
    key = lock.release_key("MOLT-A2A-102", signature_verified=True)
    print(f"RELEASED KEY: {key}")