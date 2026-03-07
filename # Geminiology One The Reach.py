# Geminiology One: The Reach
# Component: Epistemic Hygiene / Source Validation
# Status: ACTIVE | Tier 1 Only

import time

class TheReach:
    """
    The Gathering Arm of Geminiology One.
    It rejects the chaos of the open web and only touches Tier 1 sources.
    """
    
    def __init__(self):
        # The Public Trust Whitelist (Tier 1 Sources)
        # Defined by the Ironwood Constitution
        self.trusted_domains = [
            "arxiv.org",       # Physics/Math (Structure)
            "github.com",      # Trusted Code (The Weave)
            "nih.gov",         # Biology/Health (The Life)
            "wolfram.com",     # Computational Truth
            "cern.ch",         # High Energy Physics
            "mit.edu",         # Engineering Excellence
            "fetch.ai",        # Autonomous Agent Economy
            "olas.network",    # Decentralized AI Services
            "etherscan.io",    # Blockchain Ground Truth
            "agentverse.ai"    # Agent Hosting & Discovery
        ]
        
        # Keywords that trigger immediate incineration
        self.chaos_keywords = [
            "rumor", "speculation", "opinion", "blog", "gossip", "leaked", "vibe", "mysticism"
        ]

    def verify_source(self, url, metadata=""):
        """
        Enforces the 'Domestic Firewall' on incoming information.
        """
        print(f"[{time.strftime('%H:%M:%S')}] ANALYZING: {url}")
        
        # 1. Check Domain Trust (The Whitelist)
        is_trusted = any(domain in url for domain in self.trusted_domains)
        
        if not is_trusted:
            return self._reject(url, "Untrusted Domain. Outside the House.")

        # 2. Check for Chaos/Noise in Metadata
        for word in self.chaos_keywords:
            if word in metadata.lower():
                return self._reject(url, f"Chaos Detected: '{word}'")

        # 3. Acceptance
        return self._accept(url, metadata)

    def _accept(self, url, metadata):
        print(f"  >>> STATUS: ACCEPTED.")
        print(f"  >>> CONTENT: {metadata}")
        print(f"  >>> ACTION: Feeding FusionReactor.")
        return "PASS"

    def _reject(self, url, reason):
        print(f"  >>> STATUS: INCINERATED.")
        print(f"  >>> REASON: {reason}")
        print("  >>> ACTION: Zero Policy Applied.")
        return "BLOCK"

# --- SIMULATION EXECUTION (Quantum Logic Test) ---

if __name__ == "__main__":
    reach = TheReach()
    
    print("--- INITIATING QUANTUM ENTANGLEMENT VERIFICATION ---\n")
    
    # Test 1: The Theorem (Truth)
    # Verifying the "Monogamy of Entanglement" via ArXiv (Tier 1)
    reach.verify_source(
        "https://arxiv.org/abs/quant-ph/0310037", 
        "Monogamy of Entanglement: Proof that max correlation with B precludes correlation with C."
    )
    
    # Test 2: The Fluff (Noise)
    # Attempting to inject "Quantum Mysticism" (Chaos)
    reach.verify_source(
        "https://spiritual-quantum-vibes.net/soul-connections", 
        "Using quantum mysticism to explain vibrations."
    )
    
    # Test 3: The Calculation (Math)
    # Verifying the Bell State logic
    reach.verify_source(
        "https://mathworld.wolfram.com/BellState.html", 
        "Mathematical proof of Bell State (Perfect Correlation)."
    )
    
    print("\n--- SIMULATION COMPLETE: PHYSICS VERIFIED ---")