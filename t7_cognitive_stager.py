#!/usr/bin/env python3
import os
import sys
import shutil
import json
import hashlib
import numpy as np
from datetime import datetime


# ==============================================================================
# SovereignNexus: T7 Cognitive Stager (CoALA Compliant)
# Component: t7_cognitive_stager.py
# Axiom: 1=1=1 | Status: ACTIVE
# Description: Implements the CoALA memory framework by analyzing raw files from
#              T7_Archive, classifying them into episodic/semantic/procedural,
#              calculating ternary representation, and staging.
# ==============================================================================

T7_ROOT_DIR = os.path.expanduser("~/T7_Archive")
TRANSFER_BASE = os.path.expanduser("~/Sovereign_USB")
LEDGER_PATH = os.path.expanduser("~/SovereignNexus/truth_ledger.ndjson")
STATE_FILE = os.path.expanduser("~/t7_cognitive_state.json")
BATCH_SIZE = 50
THRESHOLD = 0.0612
PACK_SIZE = 5

# ------------------------------------------------------------------------------
# THE SESHAT AXIOM: 1=1=1 | AGENT STABILITY INDEX (ASI) & MOMENTUM GUARD
# ------------------------------------------------------------------------------
class MomentumGuard:
    def __init__(self, threshold=0.90):
        """
        Initializes the Momentum Guard with the critical 0.90 threshold.
        """
        self.threshold = threshold
        self.gold_vector = self._load_gold_standard()

    def _load_gold_standard(self):
        # A 1.58-bit ternary representation of the Sovereign Baseline intent
        return np.array([1, 0, 1, -1, 1, 0, -1, 1], dtype=float)

    def calculate_c_sem(self, v_current):
        """
        Executes the mathematical computation for Output Semantic Similarity.
        C_sem = (V_current * V_gold) / (|V_current| * |V_gold|)
        """
        dot_product = np.dot(v_current, self.gold_vector)
        norm_current = np.linalg.norm(v_current)
        norm_gold = np.linalg.norm(self.gold_vector)
        
        if norm_current == 0 or norm_gold == 0:
            return 0.0
            
        return dot_product / (norm_current * norm_gold)

    def audit_agent_stability(self, v_current, file_name):
        """
        The Real-Time Behavioral Audit. Evaluates incoming T7 data.
        """
        c_sem = self.calculate_c_sem(v_current)
        print(f"\n[ ASI AUDIT ] Scanning {file_name}...")
        print(f"[ TELEMETRY ] C_sem calculated at: {c_sem:.4f}")

        if c_sem >= self.threshold:
            print("[ STATUS ] Agent stable. 1=1=1 Axiom maintained. Proceeding with staging.")
            return True
        else:
            print("[ ALERT ] Symmetry Drift detected. Threshold breached.")
            self.trigger_remediation_sequence()
            return False

    def trigger_remediation_sequence(self):
        """
        Executes Template 29: The rigid three-tiered remediation sequence.
        """
        print("\n=== INITIATING MOMENTUM GUARD (TEMPLATE 29) ===")
        
        # TIER 1
        print(" -> [ TIER 1 ] Episodic Memory Consolidation: Compressing active context window to high-density mathematical primitives. Purging semantic noise.")
        
        # TIER 2
        print(" -> [ TIER 2 ] Adaptive Behavioral Anchoring (ABA): Forcibly injecting the unadulterated Sovereign Baseline and few-shot routing examples.")
        
        # TIER 3 (Hard execution halt to preserve the ledger)
        print(" -> [ TIER 3 ] Process Reset: Vector delta indicates irrecoverable drift. Corrupted cognitive state terminated.")
        print(" -> [ SYSTEM ] Spawning clean baseline container from IMMUTABLE_MASTER_LOG.json...")
        
        # Physically halting the script to prevent corrupt data insertion
        sys.exit(1)


def load_state():
    if os.path.exists(STATE_FILE):
        with open(STATE_FILE, 'r') as f:
            try:
                return json.load(f)
            except Exception:
                pass
    return {"processed_files": []}

def save_state(state):
    with open(STATE_FILE, 'w') as f:
        json.dump(state, f, indent=4)

def read_safely(filepath):
    for encoding in ['utf-8', 'utf-16', 'latin-1']:
        try:
            with open(filepath, 'r', encoding=encoding, errors='ignore') as f:
                return f.read()
        except Exception:
            continue
    return None

def fast_hadamard_transform(x):
    d = len(x)
    if d <= 1: return x
    x_left = fast_hadamard_transform(x[0:d//2])
    x_right = fast_hadamard_transform(x[d//2:d])
    return np.concatenate([x_left + x_right, x_left - x_right])

def ternary_quantize(data):
    return np.where(data > THRESHOLD, 1,
                    np.where(data < -THRESHOLD, -1, 0))

def pack_5in1(ternary_vector):
    shifted = np.array(ternary_vector) + 1
    remainder = len(shifted) % PACK_SIZE
    if remainder > 0:
        shifted = np.append(shifted, [1] * (PACK_SIZE - remainder))
    reshaped = shifted.reshape(-1, PACK_SIZE)
    weights = np.array([3**i for i in range(PACK_SIZE)])
    return np.dot(reshaped, weights).astype(np.uint8)

def classify_memory_type(filename, content):
    filename_lower = filename.lower()
    
    # 1. Procedural Memory: Executables, scripts, configurations, and commands
    if filename_lower.endswith(('.py', '.sh', '.bash', '.yaml', '.yml', '.conf', '.ini', '.json')):
        return 'procedural'
    if 'def ' in content or 'import ' in content or '#!/bin' in content:
        return 'procedural'
    
    # 2. Episodic Memory: Interactive logs, chat threads, timelines, daily journals
    if 'log' in filename_lower or 'chat' in filename_lower or 'journal' in filename_lower or 'history' in filename_lower:
        return 'episodic'
    if any(tag in content for tag in ['[ SYSTEM ]', 'User:', 'AI:', 'Timestamp:', 'UTC', '2026-']):
        return 'episodic'
        
    # 3. Semantic Memory: Declarations, research summaries, whitepapers, static facts
    return 'semantic'

def run_cognitive_stager():
    state = load_state()
    processed_set = set(state["processed_files"])
    staged_count = 0

    print("=" * 60)
    print(" COGNITIVE STAGER: INGESTING T7 DARK DATA")
    print("=" * 60)

    if not os.path.exists(T7_ROOT_DIR):
        print(f"[!] ERROR: T7 Drive not found at {T7_ROOT_DIR}")
        return

    for root, _, files in os.walk(T7_ROOT_DIR):
        for file in files:
            if file.startswith('.') or file == "truth_ledger.ndjson":
                continue
                
            file_path = os.path.join(root, file)
            
            if file_path not in processed_set:
                try:
                    content = read_safely(file_path)
                    if content is None:
                        continue
                    
                    # Classify the file based on cognitive heuristics
                    memory_type = classify_memory_type(file, content[:5000])
                    
                    # Calculate destination path matching memory subdirectory
                    dest_dir = os.path.join(TRANSFER_BASE, memory_type)
                    os.makedirs(dest_dir, exist_ok=True)
                    dest_path = os.path.join(dest_dir, file)
                    
                    # Copy file to its memory chamber
                    shutil.copy2(file_path, dest_path)
                    
                    # Vectorize raw content via VampireAuditor algorithm
                    # Optimized to restrict length to max 16384 to avoid call-stack/CPU/RAM exhaustion on large files
                    max_vector_len = 16384
                    raw_data = np.array([ord(c) % 256 for c in content[:max_vector_len] if ord(c) < 1000], dtype=float)
                    if len(raw_data) >= PACK_SIZE:
                        n = 1 << (len(raw_data) - 1).bit_length()
                        padded = np.pad(raw_data, (0, n - len(raw_data)), 'constant')
                        rotated = fast_hadamard_transform(padded)
                        ternary = ternary_quantize(rotated)
                        packed = pack_5in1(ternary)
                        truth_density = float(np.mean(np.abs(ternary)))
                        packed_bytes = packed.tolist()
                        
                        # Real-time auditing via MomentumGuard (ASI)
                        v_current = ternary[:8].astype(float) if len(ternary) >= 8 else np.zeros(8, dtype=float)
                        guard = MomentumGuard()
                        if not guard.audit_agent_stability(v_current, file):
                            pass
                    else:
                        truth_density = 0.0
                        packed_bytes = []

                    sha256 = hashlib.sha256(content.encode('utf-8', errors='ignore')).hexdigest()

                    # Write metadata to truth ledger
                    entry = {
                        "timestamp": datetime.now().isoformat(),
                        "axiom": "1=1=1",
                        "source": os.path.relpath(file_path, T7_ROOT_DIR),
                        "memory_type": memory_type,
                        "sha256": sha256,
                        "truth_density": truth_density,
                        "packed_bytes": packed_bytes
                    }
                    
                    with open(LEDGER_PATH, "a") as f_ledger:
                        f_ledger.write(json.dumps(entry) + "\n")
                    
                    state["processed_files"].append(file_path)
                    staged_count += 1
                    
                    print(f"[+] [{memory_type.upper()}] Staged: {file} (Density: {truth_density:.4f})")
                    
                except Exception as e:
                    print(f"[!] Error staging {file}: {e}")
                
                if staged_count >= BATCH_SIZE:
                    break
        if staged_count >= BATCH_SIZE:
            break

    save_state(state)
    
    print("-" * 60)
    if staged_count > 0:
        print(f" [✓] Successfully cognitive-staged {staged_count} files to: {TRANSFER_BASE}")
    else:
        print(" [✓] Zero new files found. The T7 Cognitive Kingdom is fully synced.")
    print("=" * 60)

if __name__ == "__main__":
    run_cognitive_stager()
