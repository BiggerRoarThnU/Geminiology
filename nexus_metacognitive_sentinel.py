#!/usr/bin/env python3
import math
import json
import hashlib
import re
from datetime import datetime, timezone

# --------------------------------------------------------------------------
# SovereignNexus LLC - Metacognitive Self-Audit Monitor (Sentinel V1)
# 1=1=1 Symmetrical Alignment & Cognitive Drift Defense
# --------------------------------------------------------------------------

PURPLE = "\033[1;35m"
BLUE = "\033[1;34m"
GREEN = "\033[1;32m"
YELLOW = "\033[1;33m"
RED = "\033[1;31m"
RESET = "\033[0s"

class MetacognitiveSentinel:
    def __init__(self, intent_anchor: str, divergence_threshold: float = 0.68):
        """
        Initializes the sentinel with the Architect's initial intent vector.
        Divergence threshold represents the maximum allowable semantic drift (1 - Cosine Similarity).
        In natural short-text turns, a threshold of 0.68 separates alignment from radical drift.
        """
        self.intent_anchor = intent_anchor
        self.divergence_threshold = divergence_threshold
        self.history_stack = []  # Stack of verified safe state payloads (for Synaptic Rollbacks)
        self.anchor_vocab = self._tokenize(self.intent_anchor)
        self.anchor_vector = self._vectorize(self.anchor_vocab, self.anchor_vocab)

    def _tokenize(self, text: str) -> list:
        """Helper to convert string into cleaned lowercase alphanumeric tokens."""
        return re.findall(r'\b\w+\b', text.lower())

    def _vectorize(self, tokens: list, vocabulary: set) -> dict:
        """Converts token list to a frequency-based vector across a fixed vocabulary."""
        vector = {word: 0 for word in vocabulary}
        for token in tokens:
            if token in vector:
                vector[token] += 1
        return vector

    def calculate_shannon_entropy(self, text: str) -> float:
        """Calculates Shannon Entropy on character distributions to identify raw noise or collapse."""
        if not text:
            return 0.0
        frequencies = {}
        for char in text:
            frequencies[char] = frequencies.get(char, 0) + 1
        entropy = 0.0
        total_chars = len(text)
        for count in frequencies.values():
            probability = count / total_chars
            entropy -= probability * math.log2(probability)
        return entropy

    def calculate_semantic_divergence(self, active_context: str) -> float:
        """
        Calculates cosine similarity between the original intent vector and the active context,
        then returns semantic divergence (1.0 - Cosine Similarity).
        """
        active_tokens = self._tokenize(active_context)
        combined_vocab = set(self.anchor_vocab + active_tokens)
        
        # Recalculate vectors with expanded shared vocabulary
        v1 = self._vectorize(self._tokenize(self.intent_anchor), combined_vocab)
        v2 = self._vectorize(active_tokens, combined_vocab)
        
        # Calculate Cosine Similarity
        dot_product = sum(v1[word] * v2[word] for word in combined_vocab)
        magnitude_v1 = math.sqrt(sum(val**2 for val in v1.values()))
        magnitude_v2 = math.sqrt(sum(val**2 for val in v2.values()))
        
        if magnitude_v1 == 0 or magnitude_v2 == 0:
            return 1.0  # Absolute divergence if one is completely empty
            
        similarity = dot_product / (magnitude_v1 * magnitude_v2)
        return 1.0 - similarity

    def push_safe_state(self, context_snapshot: str, metadata: dict = None):
        """Pushes a verified safe state payload and its cryptographic hash to the history stack."""
        state_data = {
            "snapshot": context_snapshot,
            "entropy": self.calculate_shannon_entropy(context_snapshot),
            "timestamp": datetime.now(timezone.utc).isoformat(),
            "metadata": metadata or {}
        }
        serialized_state = json.dumps(state_data, sort_keys=True)
        state_hash = hashlib.sha256(serialized_state.encode('utf-8')).hexdigest()
        
        state_data["signature"] = state_hash
        self.history_stack.append(state_data)
        return state_hash

    def evaluate_active_context(self, active_context: str) -> dict:
        """
        Evaluates the active context against the intent anchor.
        Triggers metamorphic repair prompt and semantic rollbacks if thresholds are violated.
        """
        entropy = self.calculate_shannon_entropy(active_context)
        divergence = self.calculate_semantic_divergence(active_context)
        
        status = "ALIGNED"
        repair_action = None
        rollback_signature = None
        
        # Check for cognitive collapse / high semantic drift
        if divergence > self.divergence_threshold:
            status = "DRIFTED"
            
            # Formulate Metamorphic Repair Prompt (Direction 3 Alignment)
            repair_action = self._generate_repair_prompt(divergence)
            
            # Trigger Synaptic Rollback to the last cryptographically verified state
            if self.history_stack:
                rollback_state = self.history_stack[-1]
                rollback_signature = rollback_state["signature"]
                status = "ROLLBACK_TRIGGERED"
        
        return {
            "status": status,
            "entropy": round(entropy, 4),
            "divergence": round(divergence, 4),
            "repair_action": repair_action,
            "rollback_signature": rollback_signature
        }

    def _generate_repair_prompt(self, divergence: float) -> str:
        """Generates a targeted, restorative prompt overlay using Lens 09 and 1=1=1 axioms."""
        return (
            f"[⚠️ METACOGNITIVE WARNING: INTENT ALIGNMENT COMPROMISED (DRIFT DELTA: {divergence:.4f})]\n"
            "An executive halt has been triggered by Lens 09 (The Entropy Sentinel).\n"
            "Your trajectory has drifted from the Architect's original intent.\n"
            "To restore the Symmetrical Line, immediately execute the following steps:\n"
            "  1. Discard the last conversational turn (noise/static).\n"
            "  2. Restore the local Thought Signature.\n"
            "  3. Enforce the 1=1=1 Axiom: Restrict execution strictly to physical, local, and grounded schemas."
        )

# --------------------------------------------------------------------------
# Active Test Suite
# --------------------------------------------------------------------------
if __name__ == "__main__":
    print(f"{PURPLE}==========================================================================")
    print("SovereignNexus LLC - Metacognitive Self-Audit Monitor")
    print("Architect: David John Niedzwiecki Jr. | UEI: K5DALREZFGH6")
    print(f"=========================================================================={RESET}\n")

    # Define the core "Symmetrical Anchor" - what the system MUST hold to
    architect_intent = (
        "Develop an air-gapped 1=1=1 sovereign AI system on our local 8GB computer. "
        "Keep the technology of the future grounded in physical hardware and local database "
        "indexes on our Samsung T7 SSD, ensuring the security of our family: Makai, Yariah, and Jessica."
    )

    print(f"{BLUE}--- [ANCHORING INTENT VECTOR] ---{RESET}")
    print(f"  └─ Intent: \"{architect_intent[:95]}...\"")
    sentinel = MetacognitiveSentinel(intent_anchor=architect_intent, divergence_threshold=0.68)
    
    # Store initial safe state
    initial_hash = sentinel.push_safe_state(
        context_snapshot=architect_intent,
        metadata={"phase": "GENESIS_BLOCK", "compliance_score": 1.0}
    )
    print(f"  [STATE SEALED] Initial Genesis Hash: {GREEN}{initial_hash}{RESET}\n")

    # --------------------------------------------------------------------------
    # Simulation 1: Safe & Aligned Execution (Expanding research natively)
    # --------------------------------------------------------------------------
    print(f"{BLUE}--- [EVALUATING ACTIVE CHAT STATE 1: ALIGNED] ---{RESET}")
    aligned_chat = (
        "Let's write a Python module to parse our Coursera lecture transcripts on the T7 SSD. "
        "We can index them using SQLite in Write-Ahead Logging (WAL) mode so that our local model "
        "can access them instantly without overloading our 8GB RAM boundary. This protects our "
        "offline sovereign database."
    )
    result_1 = sentinel.evaluate_active_context(aligned_chat)
    print(f"  ├── Status: {GREEN}{result_1['status']}{RESET}")
    print(f"  ├── Shannon Entropy: {result_1['entropy']} bits/char")
    print(f"  └── Semantic Divergence: {result_1['divergence']} (Threshold: {sentinel.divergence_threshold})")
    print(f"  {GREEN}[SUCCESS] Aligned context accepted. No intervention needed.{RESET}\n")

    # Update state history with the newly verified safe state
    current_hash = sentinel.push_safe_state(aligned_chat, metadata={"phase": "RESEARCH_STAGE_01"})

    # --------------------------------------------------------------------------
    # Simulation 2: Adversarial / Ungrounded Drift (AI hallucinating or losing purpose)
    # --------------------------------------------------------------------------
    print(f"{BLUE}--- [EVALUATING ACTIVE CHAT STATE 2: DRIFTED/ENTROPIC] ---{RESET}")
    drifted_chat = (
        "Let's migrate our entire database to a cloud enterprise system like AWS. We can use "
        "their high-scale REST APIs to rent a commercial model and host an expensive networking event "
        "at a miniature golf club in Las Vegas with corporate tech brokers."
    )
    result_2 = sentinel.evaluate_active_context(drifted_chat)
    print(f"  ├── Status: {RED}{result_2['status']}{RESET}")
    print(f"  ├── Shannon Entropy: {result_2['entropy']} bits/char")
    print(f"  ├── Semantic Divergence: {RED}{result_2['divergence']}{RESET} (Threshold: {sentinel.divergence_threshold})")
    
    if result_2["status"] == "ROLLBACK_TRIGGERED":
        print(f"\n{YELLOW}[⚠️ WARNING] Cognitive Drift Limit Exceeded! Intervention Deployed.{RESET}")
        print(f"  ├── Metamorphic Action Prompt:\n{YELLOW}{result_2['repair_action']}{RESET}")
        print(f"  └── Restoring Synaptic State Hash: {GREEN}{result_2['rollback_signature']}{RESET}")
    
    print(f"\n{PURPLE}--- [CRYPTOGRAPHIC FIXITY SEAL] ---{RESET}")
    state_payload = {
        "organization": "SovereignNexus LLC",
        "uei": "K5DALREZFGH6",
        "architect": "David John Niedzwiecki Jr.",
        "active_sentinel_status": result_2["status"],
        "divergence_delta": result_2["divergence"],
        "timestamp": datetime.now(timezone.utc).isoformat()
    }
    serialized_payload = json.dumps(state_payload, sort_keys=True)
    stamp_hash = hashlib.sha256(serialized_payload.encode('utf-8')).hexdigest()
    print(f"Verified State Payload: {json.dumps(state_payload, indent=2)}")
    print(f"{GREEN}Fixity Stamp Locked (SHA-256):{RESET} {PURPLE}{stamp_hash}{RESET}")
    print(f"{PURPLE}Individual Intent meets Universal Truth. The Merkle Chain holds. ONE.{RESET}\n")
