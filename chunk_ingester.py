#!/usr/bin/env python3
import os
import sqlite3
import hashlib
import time
from datetime import datetime
import ollama

DB_PATH = os.path.expanduser("~/SovereignNexus/nexus_ledger.db")
MODEL_NAME = "qwen2.5:0.5b"
CHUNK_SIZE_WORDS = 250 # Safe context limit for our micro-node

def init_chunk_db():
    """Creates a dedicated ledger table for text chunks."""
    conn = sqlite3.connect(DB_PATH)
    c = conn.cursor()
    c.execute('''CREATE TABLE IF NOT EXISTS chunk_ledger (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    timestamp TEXT,
                    source_file TEXT,
                    chunk_index INTEGER,
                    raw_chunk TEXT,
                    chunk_summary TEXT,
                    chunk_hash TEXT UNIQUE
                )''')
    conn.commit()
    return conn

def chunk_text(text, max_words):
    """Slices a massive text block into safe, bite-sized arrays."""
    words = text.split()
    chunks = []
    for i in range(0, len(words), max_words):
        chunk = " ".join(words[i:i + max_words])
        chunks.append(chunk)
    return chunks

def process_chunk(chunk_text, chunk_index, total_chunks, filename):
    """Sends a single chunk to the AI for processing and hashes the result."""
    print(f"\n[*] Processing Chunk {chunk_index}/{total_chunks} from {filename}...")
    
    system_prompt = "You are the Sovereign Archive Synapse. Summarize the core facts of this text block accurately and concisely."
    prompt = f"Summarize this excerpt:\n\n{chunk_text}"
    
    start_time = time.time()
    try:
        response = ollama.chat(model=MODEL_NAME, messages=[
            {'role': 'system', 'content': system_prompt},
            {'role': 'user', 'content': prompt}
        ])
        summary_text = response['message']['content']
        proc_time = time.time() - start_time
        print(f"[✓] Chunk {chunk_index} summarized in {proc_time:.2f}s.")
    except Exception as e:
        print(f"[!] Ollama query failed on chunk {chunk_index}: {e}")
        return

    # Cryptographic Seal for this specific chunk
    chunk_hash = hashlib.sha256(summary_text.encode('utf-8')).hexdigest()
    
    # Store in Ledger
    conn = init_chunk_db()
    c = conn.cursor()
    try:
        c.execute("""
            INSERT INTO chunk_ledger (timestamp, source_file, chunk_index, raw_chunk, chunk_summary, chunk_hash)
            VALUES (?, ?, ?, ?, ?, ?)
        """, (datetime.now().isoformat(), filename, chunk_index, chunk_text, summary_text, chunk_hash))
        conn.commit()
        print(f"[✓] Chunk {chunk_index} sealed: {chunk_hash[:16]}...")
    except sqlite3.IntegrityError:
        print(f"[-] Chunk {chunk_index} already exists in ledger. Skipping.")
    finally:
        conn.close()

def ingest_large_file(filepath):
    """The main handler for large documents."""
    filename = os.path.basename(filepath)
    print("=" * 60)
    print(f" INITIATING COGNITIVE CHUNKING: {filename}")
    print("=" * 60)
    
    try:
        with open(filepath, "r", encoding="utf-8", errors="ignore") as f:
            full_text = f.read().strip()
    except Exception as e:
        print(f"[!] Could not read file: {e}")
        return

    # Slice the text into safe pieces
    chunks = chunk_text(full_text, CHUNK_SIZE_WORDS)
    total_chunks = len(chunks)
    print(f"[*] File sliced into {total_chunks} safe processing blocks.")
    
    for i, chunk in enumerate(chunks, 1):
        process_chunk(chunk, i, total_chunks, filename)
        # Give the CPU a 5-second breather between chunks to prevent thermal buildup
        time.sleep(5) 

    print("\n" + "=" * 60)
    print(" FILE INGESTION AND CHUNKING COMPLETE")
    print("=" * 60)

if __name__ == "__main__":
    # Test file path - Replace with your actual large text file if it has a different name
    target_file = os.path.expanduser("~/SovereignNexus/sync_intake/Revise The Epistemology of Deterministic Autonomy  A Comp.txt")
    
    init_chunk_db()
    if os.path.exists(target_file):
        ingest_large_file(target_file)
    else:
        print(f"[!] Target file not found at: {target_file}")
        print("Please ensure the large text file is in the sync_intake folder.")
