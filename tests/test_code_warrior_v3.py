#!/usr/bin/env python3
"""
Unit Tests for Code Warrior v3 (5-Gate Deterministic Airlock)
============================================================
Axiom: 1=1=1 | Substrate: Pure Python 3.12 Standard Library
"""

import os
import sys
import tempfile
import unittest

sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), "..", "src")))

from code_warrior_v3 import (
    calculate_shannon_entropy,
    couple_with_agent_11,
    egress_scrub,
    inspect_python_ast,
    scan_payload,
)


class TestCodeWarriorV3(unittest.TestCase):
    def test_shannon_entropy(self):
        low_entropy = "AAAA" * 50
        normal_entropy = "def calculate_hash(data: str) -> str:\n    return hashlib.sha256(data.encode()).hexdigest()\n"
        h_low = calculate_shannon_entropy(low_entropy)
        h_norm = calculate_shannon_entropy(normal_entropy)
        self.assertLess(h_low, 2.5)
        self.assertGreaterEqual(h_norm, 2.5)
        self.assertLessEqual(h_norm, 5.2)

    def test_ast_jinja2_ssti_detection(self):
        sample = "template = '{{ config.__class__.__globals__ }}'\n"
        findings = inspect_python_ast(sample)
        self.assertTrue(any("JINJA2" in f for f in findings))

    def test_ast_attribute_smuggling_detection(self):
        sample = "f = getattr(__builtins__, 'eval')\n"
        findings = inspect_python_ast(sample)
        self.assertTrue(any("AST_ATTR_SMUGGLING" in f for f in findings))

    def test_ast_dunder_smuggling_detection(self):
        sample = "x = obj.__globals__\n"
        findings = inspect_python_ast(sample)
        self.assertTrue(any("AST_DUNDER_SMUGGLING" in f for f in findings))

    def test_ast_forbidden_builtins(self):
        sample = "eval('2 + 2')\n"
        findings = inspect_python_ast(sample)
        self.assertTrue(any("AST_FORBIDDEN_BUILTIN" in f for f in findings))

    def test_egress_secret_redaction(self):
        dirty_payload = "Authorization: Bearer my_secret_token_123456789 and api_key='sk-test99999' with ghost_key.key"
        clean = egress_scrub(dirty_payload)
        self.assertNotIn("my_secret_token_123456789", clean)
        self.assertNotIn("sk-test99999", clean)
        self.assertIn("[REDACTED_TOKEN]", clean)
        self.assertIn("[REDACTED_SECRET]", clean)
        self.assertIn("[REDACTED_ROYAL_KEY_REF]", clean)

    def test_scan_payload_clean(self):
        with tempfile.NamedTemporaryFile("w", suffix=".py", delete=False) as f:
            f.write("# Clean mathematical calculation under 1=1=1\n")
            f.write("def add(a: int, b: int) -> int:\n    return a + b\n")
            path = f.name
        try:
            res = scan_payload(path)
            self.assertEqual(res["verdict"], 1)
            self.assertEqual(res["status"], "CLEAN_VERIFIED")
        finally:
            if os.path.exists(path):
                os.remove(path)

    def test_scan_payload_hostile(self):
        with tempfile.NamedTemporaryFile("w", suffix=".py", delete=False) as f:
            f.write("import os\ngetattr(__builtins__, 'eval')('print(1)')\n")
            path = f.name
        try:
            res = scan_payload(path)
            self.assertEqual(res["verdict"], -1)
            self.assertEqual(res["status"], "HOSTILE_BLOCKED")
        finally:
            if os.path.exists(path):
                os.remove(path)


if __name__ == "__main__":
    unittest.main()
