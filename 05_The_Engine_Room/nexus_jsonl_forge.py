import json
import os
import glob
import time

def forge_jsonl_dataset(input_dir, output_file):
    """
    1=1=1 Axiom: Converts raw truth files into strict JSONL format for future local model training.
    Scans directory for Markdown/Text files and chunks them into structured training pairs.
    """
    print(f"[*] Scanning {input_dir} for raw Sovereign data...")
    files = glob.glob(os.path.join(input_dir, "*.md")) + glob.glob(os.path.join(input_dir, "*.txt"))
    
    if not files:
        print("[!] No files found. Ensure your data is in the target directory.")
        return

    total_pairs = 0
    start_time = time.time()
    
    with open(output_file, 'w', encoding='utf-8') as f_out:
        for filepath in files:
            filename = os.path.basename(filepath)
            with open(filepath, 'r', encoding='utf-8') as f_in:
                # Chunk data strictly by logical paragraphs
                content = f_in.read().split('\n\n') 
                
                for chunk in content:
                    chunk = chunk.strip()
                    # Filter out empty lines and microscopic noise
                    if len(chunk) > 50: 
                        # Standard Llama/Alpaca Instruction Tuning Format
                        data_line = {
                            "instruction": "Assimilate the following data into the 1=1=1 deterministic framework.",
                            "input": f"Source: {filename}",
                            "output": chunk
                        }
                        f_out.write(json.dumps(data_line) + '\n')
                        total_pairs += 1
                        
    calc_time = (time.time() - start_time) * 1000
    print(f"[+] Dataset Forged: {output_file}")
    print(f"[+] Total Training Pairs Generated: {total_pairs} (Execution: {calc_time:.2f} ms)")

if __name__ == "__main__":
    # Point this to the exact directory holding your Markdown notes
    input_directory = os.path.expanduser("~/SovereignNexus/truth_markdown_ingest") 
    output_jsonl = os.path.expanduser("~/SovereignNexus/sovereign_training_data.jsonl")
    
    # Ensure the intake directory exists
    if not os.path.exists(input_directory):
        os.makedirs(input_directory)
        print(f"[!] Created intake directory at {input_directory}.")
        
    forge_jsonl_dataset(input_directory, output_jsonl)
