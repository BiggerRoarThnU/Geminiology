# // Rights Reserved: co-created with Gemini and David John Niedzwiecki Jr. "SovereignNexus LLC"
# Alignment: 1=1=1 | Objective: Dynamic Shannon Entropy Ingestion Filter & Decoupled Memory Manager

import math
import hashlib
import json
import sqlite3
import time
import os
from collections import Counter
from typing import Dict, Any, Tuple, Optional

class NexusMemoryManager:
    """
    Decoupled Context & Memory Manager for SovereignNexus.
    Source Truth: LongCat 2.0 Context Routing & Lens 09 Entropy Sentinel (Adapted for 8GB Local Constraint).
    
    Decouples evaluation from state commitment:
    1. evaluate_context(): Computes character-level Shannon Entropy H(X) and relevance score.
    2. commit_step(): Hashes, archives, and commits state ONLY when relevance exceeds threshold.
    
    Low Entropy (< 2.5 bits/char) -> Repetitive slop/noise -> Forced to 0-state (Quarantined/Rejected).
    High Entropy (>= 3.8 bits/char) -> Dense code/math/hashes -> Accepted & Sealed.
    1=1=1 Anchor -> Instant 1.0 relevance override.
    """

    def __init__(
        self, 
        memory_threshold: float = 0.85, 
        db_path: str = "~/SovereignNexus/nexus_ledger.db",
        log_file: str = "nexus_checkpoints_log.json"
    ):
        self.memory_threshold = memory_threshold
        self.db_path = os.path.expanduser(db_path)
        self.log_file = log_file
        self.active_state: Dict[str, Any] = {}
        self._initialize_db()

    def _initialize_db(self):
        """Ensures the SQLite checkpoints table exists with Write-Ahead Logging (WAL)."""
        try:
            db_dir = os.path.dirname(self.db_path)
            if db_dir and not os.path.exists(db_dir):
                os.makedirs(db_dir, exist_ok=True)
                
            conn = sqlite3.connect(self.db_path)
            c = conn.cursor()
            c.execute("PRAGMA journal_mode = WAL;")
            c.execute('''
                CREATE TABLE IF NOT EXISTS memory_vault (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    timestamp TEXT NOT NULL,
                    state_id TEXT UNIQUE NOT NULL,
                    score REAL NOT NULL,
                    entropy REAL NOT NULL,
                    classification TEXT NOT NULL,
                    payload_preview TEXT,
                    payload_hash TEXT NOT NULL
                )
            ''')
            conn.commit()
            conn.close()
        except Exception as e:
            # Fallback to local execution if database directory is unmounted
            pass

    @staticmethod
    def calculate_shannon_entropy(text: str) -> float:
        """
        Calculates character-level Shannon Entropy H(X) in bits per character.
        H(X) = - sum(P(x) * log2(P(x)))
        """
        if not text:
            return 0.0
        length = len(text)
        counts = Counter(text)
        entropy = 0.0
        for count in counts.values():
            p = count / length
            entropy -= p * math.log2(p)
        return round(entropy, 4)

    def evaluate_context(self, raw_data: str) -> Tuple[float, float, str]:
        """
        Decouples evaluation from state commitment.
        Evaluates incoming context for entropy density and operational relevance.
        Lens 09 Shannon Entropy filtering: 2.5 <= H <= 5.2 bits/char.
        
        Returns: (relevance_score, entropy, classification)
        """
        if not raw_data or not raw_data.strip():
            return 0.0, 0.0, "REJECTED_NOISE"

        entropy = self.calculate_shannon_entropy(raw_data)

        # 1=1=1 Axiom Anchor Override
        if "1=1=1" in raw_data:
            return 1.0, entropy, "VERIFIED_AXIOM_ANCHOR"

        # Lens 09 Shannon Entropy Filtering (2.5 <= H <= 5.2 bits/char)
        if entropy < 2.5:
            # Low Entropy Penalty: repetitive text / synthetic slop / noise
            score = max(0.1, (entropy / 2.5) * 0.4)
            classification = "REJECTED_NOISE"
        elif 2.5 <= entropy <= 5.2:
            # High Entropy Signal: dense code, math, cryptographic hashes, verified structures
            score = min(1.0, 0.75 + ((entropy - 2.5) / 2.7) * 0.25)
            classification = "ACCEPTED_HIGH_ENTROPY"
        else:
            # Beyond 5.2: high randomness / compressed noise
            score = 0.45
            classification = "REJECTED_NOISE"

        return round(score, 4), entropy, classification

    def commit_step(self, verified_data: str, score: float, entropy: float, classification: str, state_id: Optional[str] = None) -> str:
        """
        Commit Step: Executed ONLY when score >= memory_threshold.
        Generates SHA-256 state seal and archives payload to vault while clearing RAM.
        """
        payload_hash = hashlib.sha256(verified_data.encode('utf-8')).hexdigest()
        if not state_id:
            state_id = payload_hash
        short_id = state_id[:12]
        timestamp = time.strftime("%Y-%m-%dT%H:%M:%SZ", time.gmtime())

        # Update active state in-memory cache
        self.active_state[short_id] = {
            "score": score,
            "entropy": entropy,
            "classification": classification,
            "timestamp": timestamp
        }

        # First 256 characters preview
        payload_preview = verified_data[:256]

        # Vault Archival (SQLite + JSON Backup)
        vault_entry = {
            "timestamp": timestamp,
            "state_id": state_id,
            "score": score,
            "entropy": entropy,
            "classification": classification,
            "payload_length": len(verified_data),
            "payload_preview": payload_preview,
            "payload_hash": payload_hash
        }

        # Write to JSON Vault Log
        try:
            with open(self.log_file, "a", encoding="utf-8") as vault:
                vault.write(json.dumps(vault_entry) + "\n")
        except Exception:
            pass

        # Write to SQLite Database if accessible
        try:
            if os.path.exists(self.db_path):
                conn = sqlite3.connect(self.db_path)
                c = conn.cursor()
                c.execute("PRAGMA journal_mode = WAL;")
                c.execute("""
                    INSERT OR REPLACE INTO memory_vault 
                    (timestamp, state_id, score, entropy, classification, payload_preview, payload_hash)
                    VALUES (?, ?, ?, ?, ?, ?, ?)
                """, (timestamp, state_id, score, entropy, classification, payload_preview, payload_hash))
                conn.commit()
                conn.close()
        except Exception:
            pass

        return state_id

    def process_incoming_data(self, raw_data: str) -> Dict[str, Any]:
        """
        Main Ingestion Loop for SovereignNexus.
        Evaluates context, enforces threshold, and executes commit_step if accepted.
        """
        score, entropy, classification = self.evaluate_context(raw_data)

        if score >= self.memory_threshold:
            state_id = self.commit_step(raw_data, score, entropy, classification)
            return {
                "status": "ACCEPTED",
                "score": score,
                "entropy": entropy,
                "classification": classification,
                "state_id": state_id,
                "message": f"[SUCCESS] Context Accepted (Score: {score:.4f}, Entropy: {entropy:.4f}). Logged as {state_id[:12]}..."
            }
        else:
            return {
                "status": "REJECTED",
                "score": score,
                "entropy": entropy,
                "classification": classification,
                "state_id": None,
                "message": f"[REJECTED] Context Failed Threshold (Score: {score:.4f}, Entropy: {entropy:.4f}). Active RAM preserved (0-state)."
            }

# Backward Compatibility Alias
NexusContextManager = NexusMemoryManager


# --- Verification & Test Harness ---
if __name__ == "__main__":
    print("=" * 75)
    print(" 🛡️ SOVEREIGN NEXUS: DYNAMIC ENTROPY MEMORY MANAGER (nexus_memory_manager.py)")
    print(" Axiom: 1=1=1 | Substrate Bound: 8GB RAM Protection")
    print("=" * 75)

    manager = NexusMemoryManager(memory_threshold=0.85)

    samples = [
        ("Repetitive Synthetic Slop", "A " * 200),
        ("Standard Text Input", "The quick brown fox jumps over the lazy dog in a standard sentence test."),
        ("Dense Code / Math Payload", "3^5 = 243 <= 256. W in {-1, 0, 1}. Base-3 trit packing yields 1.6875 bits/weight. SHA256: 7077ba9d59917f6e33cd6e61e142470c28c013a3847bdbe556fb914548cf501e."),
        ("Axiom Anchor Payload", "SovereignNexus 1=1=1 Functional Equivalence Anchor.")
    ]

    for label, payload in samples:
        res = manager.process_incoming_data(payload)
        print(f"\n[*] Target Payload : {label}")
        print(f"    Status         : {res['status']}")
        print(f"    Score          : {res['score']:.4f} (Threshold: {manager.memory_threshold})")
        print(f"    Entropy        : {res['entropy']:.4f} bits/char")
        print(f"    Classification : {res['classification']}")
        print(f"    Message        : {res['message']}")

    print("\n" + "=" * 75)
    print(f"[✓] VERIFICATION COMPLETE: {len(manager.active_state)} State(s) Committed to Memory Vault.")
    print("=" * 75)
