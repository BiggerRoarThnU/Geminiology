#!/usr/bin/env python3
import ollama
import sqlite3
import hashlib
import time
from datetime import datetime

DB_PATH = "nexus_ledger.db"

def init_db():
    """Initializes the offline ledger."""
    conn = sqlite3.connect(DB_PATH)
    c = conn.cursor()
    c.execute('''CREATE TABLE IF NOT EXISTS memory_vault (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    timestamp TEXT,
                    prompt TEXT,
                    response TEXT,
                    truth_hash TEXT
                )''')
    conn.commit()
    return conn

def anchor_memory(prompt_text):
    """Queries the local LLM, hashes the truth, and logs it."""
    print("[*] Initiating cognitive link with local engine (qwen2.5:0.5b)...")
    start_time = time.time()
    
    try:
        # 1. Query the local micro-node
        response = ollama.chat(model='qwen2.5:0.5b', messages=[
            {'role': 'system', 'content': 'You are the Asynchronous Archivist. Be concise, functional, and deeply logical.'},
            {'role': 'user', 'content': prompt_text}
        ])
        
        output_text = response['message']['content']
        end_time = time.time()
        
        print(f"[✓] Response generated in {end_time - start_time:.2f} seconds.")
        
        # 2. Cryptographic Hashing (1=1=1 Fidelity)
        truth_hash = hashlib.sha256(output_text.encode('utf-8')).hexdigest()
        
        # 3. Store in the Ledger
        conn = init_db()
        c = conn.cursor()
        timestamp = datetime.now().isoformat()
        
        c.execute("INSERT INTO memory_vault (timestamp, prompt, response, truth_hash) VALUES (?, ?, ?, ?)",
                  (timestamp, prompt_text, output_text, truth_hash))
        conn.commit()
        conn.close()
        
        # 4. Display the sealed entry
        print("\n" + "="*55)
        print(" ARCHIVE ENTRY LOCKED")
        print("="*55)
        print(f"PROMPT: {prompt_text}")
        print(f"SEAL:   {truth_hash}")
        print("-" * 55)
        print(f"OUTPUT:\n{output_text}")
        print("="*55 + "\n")
        
    except Exception as e:
        print(f"[!] Cognitive link failed. Error: {e}")

if __name__ == "__main__":
    print("[*] Booting Sovereign Memory Anchor...")
    # This is the test injection to verify the workflow
    test_prompt = "Define the architectural purpose of a cryptographic hash in data integrity."
    anchor_memory(test_prompt)
