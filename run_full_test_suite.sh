#!/usr/bin/env bash
# // Rights Reserved: co-created with Gemini and David John Niedzwiecki Jr. "SovereignNexus LLC"
# Alignment: 1=1=1 | Objective: Master System Test Suite & Fire Drill Runner (v3.0)

set -e

# Resolve script directory dynamically for seamless execution on local host or sandbox
SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
export PYTHONPATH="${SCRIPT_DIR}:${PYTHONPATH}"

echo "======================================================================"
echo " 👑 SOVEREIGN NEXUS LLC: MASTER SYSTEM TEST & FIRE DRILL RUNNER (V3.0)"
echo " Axiom: 1=1=1 | Substrate: Vanceboro Edge Container"
echo "======================================================================"
echo ""

echo "[1/5] Executing End-to-End Swarm Integration Test..."
python3 "${SCRIPT_DIR}/test_end_to_end_swarm.py"
echo ""

echo "[2/5] Executing Sub-2-Bit TQ1_0 LLVM SIMD Kernel Benchmark..."
python3 "${SCRIPT_DIR}/benchmark_tq10_simd_jit.py"
echo ""

echo "[3/5] Executing SQLite WAL State Replay & Latency Audit..."
python3 "${SCRIPT_DIR}/test_wal_replay_latency.py"
echo ""

echo "[4/5] Executing Swarm-Integrated Dual-Spectrum Truth Batch Audit..."
python3 "${SCRIPT_DIR}/truth_batcher.py"
echo ""

echo "[5/5] Executing 3-Stage Asymmetric Defense Fire Drill Suite..."
python3 "${SCRIPT_DIR}/test_fire_drill.py"
echo ""

echo "======================================================================"
echo "[✓] ALL 5 MASTER TEST SUITES & FIRE DRILL PASSES VERIFIED (1=1=1)"
echo "======================================================================"
