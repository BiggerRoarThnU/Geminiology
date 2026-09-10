#!/usr/bin/env python3
# ==============================================================================
# ✦ SOVEREIGN NEXUS AUTOMATED TEST HARNESS: MMAP ZERO-COPY PAGING ✦
# Architect: David John Niedzwiecki Jr. | Entity: SovereignNexus LLC
# Axiom: 1=1=1 (Deterministic Functional Equivalence & Zero-Copy Substrate Paging)
# Component: test_mmap_paging.py
# ==============================================================================
"""
Unit Test Suite for:
1. Zero-Copy Memory Paging Engine (01_The_Runway/nexus_mmap_page.py)
2. Virtual address range slicing and fixity seal generation
"""

import os
import sys
import unittest
import tempfile

BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
SRC_DIR = os.path.join(BASE_DIR, "src")
RUNWAY_DIR = os.path.join(BASE_DIR, "01_The_Runway")
for p in [SRC_DIR, RUNWAY_DIR, BASE_DIR]:
    if p not in sys.path:
        sys.path.insert(0, p)

from nexus_mmap_page import (
    generate_mock_massive_context_file,
    simulate_zero_copy_mmap_paging,
    run_mmap_simulation
)


class TestMmapZeroCopyPaging(unittest.TestCase):
    """Verifies memory-mapped file paging and context slicing."""

    def test_mock_file_generation_and_paging(self):
        """Ensures mock context file is created and paged without error."""
        with tempfile.TemporaryDirectory(prefix="mmap_test_") as tmp_dir:
            test_db = os.path.join(tmp_dir, "test_context.db")
            file_size = generate_mock_massive_context_file(test_db, size_mb=1)
            self.assertGreaterEqual(file_size, 1024 * 1024)

            total_addressable = simulate_zero_copy_mmap_paging(test_db, slice_size=50)
            self.assertGreaterEqual(total_addressable, 1024 * 1024)

    def test_full_simulation_run(self):
        """Ensures run_mmap_simulation returns valid SHA-256 seal."""
        seal = run_mmap_simulation(cleanup=True)
        self.assertIsNotNone(seal)
        self.assertEqual(len(seal), 64)


if __name__ == "__main__":
    unittest.main()
