#!/home/geminiology/SovereignNexus/env/bin/python3
import os
import sys
import argparse
import numpy as np

# Reference gold standard vector representing the Sovereign baseline intent
GOLD_VECTOR = np.array([1, 0, 1, -1, 1, 0, -1, 1], dtype=float)
DEFAULT_THRESHOLD = 0.90
TIGHT_THRESHOLD = 0.0612

def fast_hadamard_transform(x):
    """Computes the Walsh-Hadamard Transform recursively."""
    d = len(x)
    if d <= 1:
        return x
    x_left = fast_hadamard_transform(x[0:d//2])
    x_right = fast_hadamard_transform(x[d//2:d])
    return np.concatenate([x_left + x_right, x_left - x_right])

def ternary_quantize(data, threshold=TIGHT_THRESHOLD):
    """Quantizes real numbers to ternary values (-1, 0, 1)."""
    return np.where(data > threshold, 1,
                    np.where(data < -threshold, -1, 0))

def calculate_similarity(v_current, v_reference=GOLD_VECTOR):
    """
    Computes cosine similarity between two vectors.
    C_sem = (V_current * V_ref) / (|V_current| * |V_ref|)
    """
    dot_product = np.dot(v_current, v_reference)
    norm_current = np.linalg.norm(v_current)
    norm_ref = np.linalg.norm(v_reference)
    
    if norm_current == 0 or norm_ref == 0:
        return 0.0
        
    return dot_product / (norm_current * norm_ref)

def analyze_text(text, threshold=DEFAULT_THRESHOLD):
    """Vectorizes text and calculates its similarity against the gold vector standard."""
    # Convert character ascii values (modulo 256)
    max_vector_len = 16384
    raw_data = np.array([ord(c) % 256 for c in text[:max_vector_len] if ord(c) < 1000], dtype=float)
    
    if len(raw_data) < 8:
        print("[!] Input text is too short to generate a valid 8-dimensional comparison vector.")
        return None
        
    # Pad to nearest power of 2 for Hadamard Transform
    n = 1 << (len(raw_data) - 1).bit_length()
    padded = np.pad(raw_data, (0, n - len(raw_data)), 'constant')
    
    # Apply Walsh-Hadamard Transform
    rotated = fast_hadamard_transform(padded)
    
    # Quantize to 1.58-bit ternary representation
    ternary = ternary_quantize(rotated)
    
    # Extract first 8 dimensions for standard validation
    v_current = ternary[:8].astype(float)
    
    # Calculate similarity index
    c_sem = calculate_similarity(v_current)
    
    aligned = c_sem >= threshold
    
    return {
        "c_sem": c_sem,
        "v_current": v_current.tolist(),
        "aligned": aligned,
        "raw_length": len(text),
        "vector_length": len(ternary)
    }

def main():
    parser = argparse.ArgumentParser(
        description="SovereignNexus Truth Testing CLI - Evaluates text drift using Walsh-Hadamard ternary projection."
    )
    group = parser.add_mutually_exclusive_group(required=True)
    group.add_argument("-t", "--text", type=str, help="Raw text string to evaluate.")
    group.add_argument("-f", "--file", type=str, help="Path to a text file to evaluate.")
    
    parser.add_argument(
        "--threshold", 
        type=float, 
        default=DEFAULT_THRESHOLD, 
        help=f"Alignment threshold (default: {DEFAULT_THRESHOLD:.2f})"
    )
    
    parser.add_argument(
        "--ledger",
        type=str,
        default=None,
        help="Optional path to an NDJSON ledger file to append the result."
    )
    
    args = parser.parse_args()
    
    # Get input content
    if args.text:
        source_name = "Raw CLI Input"
        text_content = args.text
    else:
        if not os.path.exists(args.file):
            print(f"[!] Error: File not found at {args.file}")
            sys.exit(1)
        source_name = os.path.basename(args.file)
        try:
            with open(args.file, 'r', encoding='utf-8', errors='ignore') as f:
                text_content = f.read()
        except Exception as e:
            print(f"[!] Error reading file: {e}")
            sys.exit(1)
            
    print("=" * 60)
    print(" SOVEREIGN TRUTH TESTING CLI: COGNITIVE ANALYSIS")
    print("=" * 60)
    print(f" Source: {source_name}")
    print(f" Reference Intent Vector: {GOLD_VECTOR.tolist()}")
    print(f" Threshold Target: >= {args.threshold:.2f}")
    print("-" * 60)
    
    result = analyze_text(text_content, args.threshold)
    
    if result:
        from datetime import datetime
        import json
        
        print(f" Character Count: {result['raw_length']}")
        print(f" Hadamard Space Dimensions: {result['vector_length']}")
        print(f" Target Vector: {result['v_current']}")
        print(f" C_sem Similarity: {result['c_sem']:.4f}")
        print("-" * 60)
        
        if result['aligned']:
            print("[✓] STATUS: ALIGNED (Axiom maintained).")
        else:
            print("[!] STATUS: DRIFT DETECTED (Below threshold target).")
            
        # Log to ledger if requested
        if args.ledger:
            ledger_path = os.path.abspath(args.ledger)
            ledger_entry = {
                "timestamp": datetime.now().isoformat(),
                "axiom": "1=1=1",
                "source": source_name,
                "c_sem": float(result['c_sem']),
                "v_current": result['v_current'],
                "status": "ALIGNED" if result['aligned'] else "DRIFTED"
            }
            try:
                # Atomically append the NDJSON log line
                with open(ledger_path, "a", encoding="utf-8", buffering=1) as f_ledger:
                    f_ledger.write(json.dumps(ledger_entry) + "\n")
                print(f"[✓] Logged entry to: {ledger_path}")
            except Exception as e:
                print(f"[!] Warning: Failed to write to ledger {ledger_path}: {e}")
                
    print("=" * 60)

if __name__ == "__main__":
    main()
