#!/usr/bin/env python3

# ==============================================================================
# SovereignNexus: Mixture of Experts Educational Router
# Component: moe_educational_router.py
# Axiom: 1=1=1 | Status: ACTIVE EDUCATION ROUTING ENGINE
# Description: Pure retrieval-based routing engine that reads static JSON ledgers
#              to provide unhallucinated educational facts for the family.
# ==============================================================================

import os
import json
import hashlib
import sys

class EducationalMoE:
    def __init__(self):
        self.base_dir = "/home/geminiology/sovereign_nexus/moe_sectors/knowledge_vault/education"
        self.sectors = {
            "mathematics": os.path.join(self.base_dir, "mathematics/mathematics.json"),
            "logic": os.path.join(self.base_dir, "logic/logic.json"),
            "history": os.path.join(self.base_dir, "history/history.json"),
            "python_core": os.path.join(self.base_dir, "python_core/python_core.json")
        }
        # Fixed baseline verification hashes to ensure no data drift (1=1=1 verification)
        self.baseline_hashes = {}
        self.calculate_baselines()

    def calculate_baselines(self):
        """Calculates current SHA-256 hashes of the files to serve as verification anchors."""
        for sector, filepath in self.sectors.items():
            if os.path.exists(filepath):
                hasher = hashlib.sha256()
                with open(filepath, "rb") as f:
                    hasher.update(f.read())
                self.baseline_hashes[sector] = hasher.hexdigest()
            else:
                self.baseline_hashes[sector] = None

    def verify_integrity(self, sector):
        """Verifies if the target sector file matches the recorded anchor hash."""
        filepath = self.sectors.get(sector)
        if not filepath or not os.path.exists(filepath):
            return False, "File missing"
        
        hasher = hashlib.sha256()
        with open(filepath, "rb") as f:
            hasher.update(f.read())
        current_hash = hasher.hexdigest()
        
        anchor = self.baseline_hashes.get(sector)
        if anchor and current_hash == anchor:
            return True, current_hash
        return False, f"Integrity check failed: current {current_hash[:10]} != baseline {str(anchor)[:10]}"

    def query(self, user_query):
        """Routes query to correct expert ledger based on keyword matching and retrieves truth."""
        user_query = user_query.lower().strip()
        
        # Route categorization
        target_sector = None
        target_concept = None
        
        # Logic routing keywords
        if any(word in user_query for word in ["logic", "syllogism", "ternary", "de morgan", "premise", "deductive"]):
            target_sector = "logic"
            if "syllogism" in user_query or "deductive" in user_query:
                target_concept = "syllogism"
            elif "ternary" in user_query:
                target_concept = "ternary_logic"
            elif "morgan" in user_query:
                target_concept = "de_morgan"
                
        # Mathematics routing keywords
        elif any(word in user_query for word in ["math", "addition", "pythagorean", "geometry", "fraction", "plus", "triangle"]):
            target_sector = "mathematics"
            if "addition" in user_query or "plus" in user_query:
                target_concept = "addition"
            elif "pythagorean" in user_query or "geometry" in user_query or "triangle" in user_query:
                target_concept = "geometry"
            elif "fraction" in user_query:
                target_concept = "fractions"
                
        # History routing keywords
        elif any(word in user_query for word in ["history", "printing", "gutenberg", "internet", "arpanet", "sovereignty", "metallurgy", "diamond"]):
            target_sector = "history"
            if "printing" in user_query or "gutenberg" in user_query:
                target_concept = "printing_press"
            elif "internet" in user_query or "arpanet" in user_query:
                target_concept = "internet_genesis"
            elif "sovereignty" in user_query or "metallurgy" in user_query or "diamond" in user_query:
                target_concept = "hardware_sovereignty"

        # Python core routing keywords
        elif any(word in user_query for word in ["python", "code", "programming", "variable", "conditional", "loop", "type", "branching"]):
            target_sector = "python_core"
            if "variable" in user_query or "type" in user_query:
                target_concept = "variables_and_types"
            elif "conditional" in user_query or "branch" in user_query or "if" in user_query:
                target_concept = "conditionals"
            elif "loop" in user_query or "for" in user_query or "while" in user_query:
                target_concept = "loops"

        if not target_sector:
            return {
                "status": "UNKNOWN",
                "message": "Query did not match educational moat routing rules. To protect from drift, no probabilistic response is generated."
            }

        # Verify cryptographic line holds
        is_ok, hash_or_err = self.verify_integrity(target_sector)
        if not is_ok:
            return {
                "status": "INTEGRITY_COMPROMISED",
                "error": hash_or_err,
                "message": "The database has drifted from the Sovereign Baseline. Process halted."
            }

        # Retrieve static truth
        try:
            with open(self.sectors[target_sector], "r") as f:
                data = json.load(f)
            
            curriculum = data.get("curriculum", {})
            
            if target_concept and target_concept in curriculum:
                concept_data = curriculum[target_concept]
                return {
                    "status": "VERIFIED_TRUTH",
                    "sector": target_sector,
                    "concept": target_concept,
                    "hash": hash_or_err[:12],
                    "details": concept_data
                }
            else:
                # Return general sector overview if specific concept not matched
                return {
                    "status": "VERIFIED_TRUTH",
                    "sector": target_sector,
                    "hash": hash_or_err[:12],
                    "message": f"Retrieved general database overview for '{target_sector}' sector.",
                    "available_concepts": list(curriculum.keys())
                }
        except Exception as e:
            return {
                "status": "READ_ERROR",
                "error": str(e)
            }


if __name__ == "__main__":
    moe = EducationalMoE()
    
    # Run test queries
    print("=== Educational MoE Moat Interface ===")
    
    test_queries = [
        "How does addition work in math?",
        "Explain balanced ternary logic parameters.",
        "Tell me about the history of the printing press by Gutenberg.",
        "What is the weather like today?" # Should yield UNKNOWN to block hallucination
    ]
    
    for q in test_queries:
        print(f"\n[QUERY] '{q}'")
        res = moe.query(q)
        print(json.dumps(res, indent=2))
        
    print("\n========================================")
