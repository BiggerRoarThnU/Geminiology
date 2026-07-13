import unittest
from src.vampire_algorithm import VampireParsingEngine

class TestVampireParsingEngine(unittest.TestCase):
    """
    Automated verification suite validating the structural integrity,
    noise-reduction, and truth-distillation thresholds of the Vampire Engine.
    """
    def setUp(self):
        """Initializes a fresh, isolated engine instance before each evaluation loop."""
        self.engine = VampireParsingEngine(confidence_threshold=0.75)
        self.system_primitives = ["status", "assert", "verify", "critical"]

    def test_semantic_noise_reduction(self):
        """Validates that extraneous whitespace and conversational padding are stripped cleanly."""
        raw_bloat = "   System status normal.    Oh by the way, trailing anomalies detected.   "
        expected_clean = "System status normal. Oh by the way, trailing anomalies detected."
        
        sanitized = self.engine.strip_semantic_noise(raw_bloat)
        self.assertEqual(sanitized, expected_clean)

    def test_truth_vector_isolation(self):
        """Verifies that the engine successfully extracts sentences containing priority syntactic anchors."""
        test_payload = "This is a random sentence. Assert system connectivity is established. Another unrelated comment. Verify terminal state."
        
        vectors = self.engine.extract_truth_vectors(test_payload)
        self.assertEqual(len(vectors), 2)
        self.assertIn("Assert system connectivity is established.", vectors)
        self.assertIn("Verify terminal state.", vectors)

    def test_strict_alignment_threshold_pass(self):
        """Ensures that assertions meeting or exceeding the confidence metric are preserved."""
        # This assertion contains 'assert' and 'status' (2 matches out of 4 system primitives = 0.50 score)
        # We will dynamically adjust the threshold to verify successful state capture
        self.engine.confidence_threshold = 0.50
        raw_stream = "Assert baseline system status is functional."
        
        result = self.engine.distill_payload(raw_stream, self.system_primitives)
        self.assertEqual(result["status"], "processed")
        self.assertEqual(result["extracted_vectors_count"], 1)

    def test_strict_alignment_threshold_drop(self):
        """Ensures that assertions falling below the confidence metric are aggressively dropped."""
        # High confidence requirement
        self.engine.confidence_threshold = 0.90
        raw_stream = "Assert system status is normal." # Low primitive density ratio
        
        result = self.engine.distill_payload(raw_stream, self.system_primitives)
        # The sentence passes the initial regex anchor but should fail the score math and get filtered out
        self.assertEqual(result["extracted_vectors_count"], 0)

if __name__ == "__main__":
    print("[!] Executing Automated Geminiology Unit Test Matrix...")
    unittest.main()
