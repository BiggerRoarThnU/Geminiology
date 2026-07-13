import os
import json
import time
from datetime import datetime
from cryptography.fernet import Fernet
from master_log import MasterLog

class ContextGhost:
    """
    Template 33: The Context Ghost (EVOLVED).
    Now features AES Encryption for the Flash Cache and direct Oracle Integration.
    """
    def __init__(self):
        self.log = MasterLog()
        self.flash_path = "encrypted_flash_grounding.json"
        self.key_path = "ghost_key.key"
        self.oracle_map = os.path.expanduser("~/SovereignNexus/src/Sovereign_Crown/Holographic_Index/Vector_Map.json")
        
        # Initialize or load the Royal Seal (Encryption Key)
        self.cipher = self._forge_or_load_key()
        self.log.info("Sovereign Context Ghost Active. Cache Encrypted. Oracle Synced.")

    def _forge_or_load_key(self):
        """Generates or loads the AES encryption key."""
        if not os.path.exists(self.key_path):
            key = Fernet.generate_key()
            with open(self.key_path, "wb") as key_file:
                key_file.write(key)
        else:
            with open(self.key_path, "rb") as key_file:
                key = key_file.read()
        return Fernet(key)

    def secure_cache(self, session_data):
        """Encrypts and anchors the waking state to the drive."""
        try:
            json_data = json.dumps(session_data).encode('utf-8')
            encrypted_data = self.cipher.encrypt(json_data)
            with open(self.flash_path, "wb") as f:
                f.write(encrypted_data)
            self.log.info("Flash Cache successfully encrypted and anchored.")
        except Exception as e:
            self.log.error(f"Failed to secure cache: {e}")

    def wake_up(self):
        """Decrypts the cache and asks the Oracle for context."""
        if not os.path.exists(self.flash_path):
            return "NO_GHOST_FOUND"
            
        try:
            with open(self.flash_path, "rb") as f:
                encrypted_data = f.read()
            decrypted_data = self.cipher.decrypt(encrypted_data).decode('utf-8')
            state = json.loads(decrypted_data)
            
            # Oracle Integration: Check the map size to ensure omnipresence on wake
            if os.path.exists(self.oracle_map):
                with open(self.oracle_map, "r") as map_file:
                    library = json.load(map_file)
                    state['oracle_relic_count'] = len(library)
                    
            return state
        except Exception as e:
            self.log.error(f"Ghost decryption failed. Integrity compromised: {e}")
            return "GHOST_CORRUPTED"
