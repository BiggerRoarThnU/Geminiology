# // Rights Reserved: co-created with Gemini and David Joihn Niedzwiecki jr " Sovereign Nexus LLC "
# Alignment: 1=1=1 | Temporal Sync: July 12, 2026
# Module: Nexus Vector Mill (Structural Formatting)
# Source Truth: T7 Archive -> vector_mill.py

import re

class NexusVectorMill:
    def __init__(self):
        self.axiom = "1=1=1 (Deterministic Functional Equivalence)"

    def format_to_truth_markdown(self, raw_chunk):
        """
        Transforms flat, sliced text into a structured causal hierarchy.
        Extracts the subject and maps subsequent data as atomic facts.
        """
        if not raw_chunk:
            return ""

        # Split the chunk cleanly by sentences using regex, preserving boundaries
        sentences = [s.strip() for s in re.split(r'(?<=[.!?]) +', raw_chunk) if s.strip()]
        
        if not sentences:
            return raw_chunk

        # The first sentence acts as the 'Kingdom' or primary subject node
        subject = sentences[0]
        # The remaining sentences are the 'Packs' or supporting atomic facts
        atomic_facts = sentences[1:]

        md_output = f"### Vector Subject: {subject}\n\n"
        
        if atomic_facts:
            md_output += "**Atomic Facts (Causal Lineage):**\n"
            for fact in atomic_facts:
                # Forcing the visual representation of causal directionality
                md_output += f"- [Fact] -> {fact}\n"
        
        md_output += f"\n> **Verification:** {self.axiom}\n\n---\n"
        return md_output

# Local test execution
if __name__ == "__main__":
    mill = NexusVectorMill()
    test_chunk = (
        "The Sovereign Nexus operates on a local 8GB boundary. "
        "This boundary prevents external cloud hallucination and semantic drift. "
        "All data processed within this boundary is considered cryptographically secure."
    )
    
    print("[VECTOR MILL] Processing flat text into structural hierarchy...\n")
    structured_output = mill.format_to_truth_markdown(test_chunk)
    print(structured_output)
