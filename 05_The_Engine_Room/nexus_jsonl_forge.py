import json
import os
import glob
import time
import hashlib

def forge_jsonl_dataset(input_dir, output_file):
    """
    1=1=1 Axiom: Converts raw truth files into strict JSONL format.
    Enforces deterministic sorting, cryptographic provenance, deduplication, and dynamic pathing.
    """
    print(f"[*] Scanning {input_dir} for raw Sovereign data...")
    
    # FIX 1: Deterministic sorting to guarantee exact replication across all hardware
    search_pattern_md = os.path.join(input_dir, "*.md")
    search_pattern_txt = os.path.join(input_dir, "*.txt")
    files = sorted(glob.glob(search_pattern_md) + glob.glob(search_pattern_txt))
    
    if not files:
        print("[!] No files found. Ensure your data is in the target directory.")
        return

    total_pairs = 0
    start_time = time.time()
    
    # FIX 2: Cryptographic Deduplication ledger
    seen_hashes = set()
    
    with open(output_file, 'w', encoding='utf-8') as f_out:
        for filepath in files:
            filename = os.path.basename(filepath)
            with open(filepath, 'r', encoding='utf-8') as f_in:
                content = f_in.read().split('\n\n') 
                
                for chunk_idx, chunk in enumerate(content):
                    chunk = chunk.strip()
                    # FIX 3: Lower noise filter to preserve short axioms (e.g., "1 = 1 = 1")
                    if len(chunk) >= 5: 
                        chunk_hash = hashlib.sha256(chunk.encode('utf-8')).hexdigest()
                        
                        # Prune duplicates to maintain pure mathematical density
                        if chunk_hash in seen_hashes:
                            continue 
                        seen_hashes.add(chunk_hash)
                        
                        # FIX 4: Cryptographic Provenance in the Input stream
                        data_line = {
                            "instruction": "Assimilate the following data into the 1=1=1 deterministic framework.",
                            "input": f"Source: {filename} | Section: {chunk_idx} | SHA256: {chunk_hash[:8]}",
                            "output": chunk
                        }
                        f_out.write(json.dumps(data_line) + '\n')
                        total_pairs += 1
                        
    calc_time = (time.time() - start_time) * 1000
    print(f"[+] Dataset Forged: {output_file}")
    print(f"[+] Total Unique Training Pairs: {total_pairs} (Execution: {calc_time:.2f} ms)")

if __name__ == "__main__":
    # FIX 5: Dynamic relative pathing
    # This automatically finds the root SovereignNexus directory regardless of where it is cloned
    script_dir = os.path.dirname(os.path.abspath(__file__))
    nexus_root = os.path.dirname(script_dir)
    
    input_directory = os.path.join(nexus_root, "truth_markdown_ingest") 
    output_jsonl = os.path.join(nexus_root, "sovereign_training_data.jsonl")
    
    if not os.path.exists(input_directory):
        os.makedirs(input_directory)
        print(f"[!] Created intake directory at {input_directory}.")
        
    forge_jsonl_dataset(input_directory, output_jsonl)
