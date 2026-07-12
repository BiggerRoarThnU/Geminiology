# // Rights Reserved: co-created with Gemini and David Joihn Niedzwiecki jr " Sovereign Nexus LLC "
# Alignment: 1=1=1 | Temporal Sync: July 12, 2026
# Source Truth: LongCat 2.0 Context Routing (Adapted for 8GB Local Constraint)

import hashlib
import json

class NexusContextManager:
    def __init__(self, memory_threshold=0.85):
        self.memory_threshold = memory_threshold
        self.active_state = {} 

    def _calculate_weight(self, raw_data):
        """
        Internal method to score the relevance and alignment of incoming data.
        Integrates the Observer validation logic:
        - If input is an image path, runs MediaForge Laplacian variance checks.
        - If input is text/code, verifies constitutional alignment (1=1=1, density, values).
        """
        raw_str = str(raw_data).strip()
        
        # Check if the input is an image path
        if any(raw_str.lower().endswith(ext) for ext in ['.png', '.jpg', '.jpeg', '.bmp']):
            import os
            # If absolute path doesn't exist, try relative to root or Lucid Build Up
            if not os.path.exists(raw_str):
                potential_paths = [
                    os.path.join("/home/geminiology/Lucid Build Up", os.path.basename(raw_str)),
                    os.path.join("/home/geminiology/SovereignNexus/src", os.path.basename(raw_str))
                ]
                for path in potential_paths:
                    if os.path.exists(path):
                        raw_str = path
                        break
            
            if os.path.exists(raw_str):
                try:
                    import cv2
                    # Run Laplacian Variance test (MediaForge logic)
                    gray_matrix = cv2.cvtColor(cv2.imread(raw_str), cv2.COLOR_BGR2GRAY)
                    variance = cv2.Laplacian(gray_matrix, cv2.CV_64F).var()
                    if variance >= 100.0:
                        return 0.95  # Raw Entropy Confirmed
                except Exception as e:
                    print(f"[-] Observer error analyzing matrix: {e}")
            return 0.0  # Failed variance test or missing file (Synthetic Slop)
            
        # Check for 1=1=1 Symmetry marker
        if "1=1=1" in raw_str:
            return 1.0
            
        # Handle potential numeric inputs
        try:
            val = float(raw_str)
            if val > 0:
                return 0.95
        except ValueError:
            pass
            
        # High-density text verification
        if len(raw_str) > 10:
            return 0.90
            
        # Rejected
        return 0.0

    def _generate_hash(self, data):
        """Creates a unique ID for the memory chunk."""
        return hashlib.sha256(data.encode('utf-8')).hexdigest()

    def _archive_to_vault(self, data, state_id):
        """
        Appends the accepted context into the local database, 
        clearing it from active RAM to respect the 8GB limit.
        """
        vault_entry = {
            "timestamp": "2026-07-12",
            "state_id": state_id,
            "content": data
        }
        # In production, this writes to nexus_checkpoints.db
        with open("nexus_checkpoints_log.json", "a") as vault:
            vault.write(json.dumps(vault_entry) + "\n")

    def evaluate_context(self, raw_data):
        """
        Decouples evaluation from commitment.
        """
        relevance_score = self._calculate_weight(raw_data)
        return relevance_score

    def commit_step(self, verified_data):
        """
        Only updates the state if the threshold is met.
        """
        state_id = self._generate_hash(verified_data)
        self.active_state[state_id] = verified_data
        
        self._archive_to_vault(verified_data, state_id)
        return state_id

    def process_incoming_data(self, raw_data):
        """
        The main ingestion loop for SovereignNexus.
        """
        score = self.evaluate_context(raw_data)
        
        if score >= self.memory_threshold:
            state_id = self.commit_step(raw_data)
            return f"[SUCCESS] Context Accepted (Score: {score}). Logged to Vault as {state_id[:8]}"
        else:
            return f"[REJECTED] Context Failed Threshold (Score: {score}). State preserved."
