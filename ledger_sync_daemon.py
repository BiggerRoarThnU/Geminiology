#!/usr/bin/env python3
import os
import sys
import time
import sqlite3
import hashlib
import shutil
from datetime import datetime

DB_PATH = os.path.expanduser("~/SovereignNexus/nexus_ledger.db")
INTAKE_DIR = os.path.expanduser("~/SovereignNexus/sync_intake")
ARCHIVE_DIR = os.path.expanduser("~/SovereignNexus/sync_archive")
MEDIA_ARCHIVE_DIR = os.path.expanduser("~/SovereignNexus/media_archive")
MODEL_NAME = "qwen2.5:0.5b"

# Safe files for LLM processing. Anything else is routed to media archive.
SAFE_TEXT_EXTENSIONS = ['.txt', '.md', '.py', '.csv', '.json', '.log']
MAX_FILE_SIZE_BYTES = 1 * 1024 * 1024 # 1 Megabyte limit for AI inference

def init_db():
    db_dir = os.path.dirname(DB_PATH)
    if db_dir and not os.path.exists(db_dir):
        os.makedirs(db_dir, exist_ok=True)
    conn = sqlite3.connect(DB_PATH)
    c = conn.cursor()
    c.execute('''CREATE TABLE IF NOT EXISTS file_sync_ledger (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    timestamp TEXT,
                    filename TEXT,
                    file_hash TEXT UNIQUE,
                    prompt TEXT,
                    summary TEXT,
                    summary_hash TEXT,
                    processing_time REAL,
                    cpu_temp REAL
                )''')
    conn.commit()
    return conn

def get_cpu_temperature():
    temp_c = 0.0
    thermal_dir = "/sys/class/thermal"
    if os.path.exists(thermal_dir):
        for tz in os.listdir(thermal_dir):
            if tz.startswith("thermal_zone"):
                try:
                    with open(os.path.join(thermal_dir, tz, "temp"), "r") as f:
                        raw_temp = float(f.read().strip())
                        if raw_temp > 1000:
                            raw_temp = raw_temp / 1000.0
                        if raw_temp > temp_c:
                            temp_c = raw_temp
                except:
                    pass
    return temp_c

def calculate_sha256(filepath):
    sha256_hash = hashlib.sha256()
    with open(filepath, "rb") as f:
        for chunk in iter(lambda: f.read(65536), b""):
            sha256_hash.update(chunk)
    return sha256_hash.hexdigest()

def file_already_processed(file_hash):
    conn = init_db()
    c = conn.cursor()
    c.execute("SELECT id FROM file_sync_ledger WHERE file_hash = ?", (file_hash,))
    row = c.fetchone()
    conn.close()
    return row is not None

def query_local_model(content):
    import ollama
    system_prompt = (
        "You are the Sovereign Archive Synapse. Your job is to analyze the input text and "
        "provide a dense, highly factual summary. Do not include introductory phrases, "
        "polite remarks, or placeholders. Return only key findings, raw facts, and logical conclusions."
    )
    prompt = f"Extract all critical insights from the following text:\n\n{content}"
    response = ollama.chat(model=MODEL_NAME, messages=[
        {'role': 'system', 'content': system_prompt},
        {'role': 'user', 'content': prompt}
    ])
    return prompt, response['message']['content']

def move_to_archive(filepath, filename, target_dir):
    if not os.path.exists(target_dir):
        os.makedirs(target_dir, exist_ok=True)
    archive_path = os.path.join(target_dir, filename)
    if os.path.exists(archive_path):
        base, ext = os.path.splitext(filename)
        archive_path = os.path.join(target_dir, f"{base}_{int(time.time())}{ext}")
    shutil.move(filepath, archive_path)
    return archive_path

def process_file(filepath):
    filename = os.path.basename(filepath)
    print(f"\n[*] Processing file: {filename}")
    _, ext = os.path.splitext(filename)
    file_size = os.path.getsize(filepath)

    temp_c = get_cpu_temperature()
    if temp_c > 72.0:
        print(f"[!] Warning: CPU temp ({temp_c:.1f}°C) is high. Cooling down for 30s...")
        time.sleep(30)
        temp_c = get_cpu_temperature()

    file_hash = calculate_sha256(filepath)
    print(f"[*] File Hash: {file_hash}")

    if file_already_processed(file_hash):
        print(f"[!] File already processed. Archiving...")
        move_to_archive(filepath, filename, ARCHIVE_DIR)
        return

    # THE MEDIA ROUTER: Check if safe for LLM
    if ext.lower() not in SAFE_TEXT_EXTENSIONS or file_size > MAX_FILE_SIZE_BYTES:
        print(f"[!] Binary, Media, or Oversized file detected. Bypassing AI inference.")
        summary_text = "[RAW MEDIA / BINARY / OVERSIZED - OLLAMA INFERENCE BYPASSED]"
        summary_hash = hashlib.sha256(summary_text.encode('utf-8')).hexdigest()
        
        conn = init_db()
        c = conn.cursor()
        c.execute("""
            INSERT INTO file_sync_ledger (timestamp, filename, file_hash, prompt, summary, summary_hash, processing_time, cpu_temp)
            VALUES (?, ?, ?, ?, ?, ?, ?, ?)
        """, (datetime.now().isoformat(), filename, file_hash, "N/A", summary_text, summary_hash, 0.0, temp_c))
        conn.commit()
        conn.close()

        final_path = move_to_archive(filepath, filename, MEDIA_ARCHIVE_DIR)
        print(f"[✓] File safely routed to: {os.path.basename(MEDIA_ARCHIVE_DIR)}")
        return

    # SAFE TEXT PROCESSING
    try:
        with open(filepath, "r", encoding="utf-8", errors="ignore") as f:
            content = f.read().strip()
    except Exception as e:
        print(f"[!] Error reading file: {e}")
        return

    if not content:
        print("[!] File is empty. Archiving.")
        move_to_archive(filepath, filename, ARCHIVE_DIR)
        return

    print(f"[*] Sending safe text to local model '{MODEL_NAME}'...")
    start_time = time.time()
    try:
        prompt, summary_text = query_local_model(content)
        processing_time = time.time() - start_time
        print(f"[✓] Inference complete in {processing_time:.2f} seconds.")
    except Exception as e:
        print(f"[!] Ollama query failed: {e}")
        return

    summary_hash = hashlib.sha256(summary_text.encode('utf-8')).hexdigest()

    conn = init_db()
    c = conn.cursor()
    try:
        c.execute("""
            INSERT INTO file_sync_ledger (timestamp, filename, file_hash, prompt, summary, summary_hash, processing_time, cpu_temp)
            VALUES (?, ?, ?, ?, ?, ?, ?, ?)
        """, (datetime.now().isoformat(), filename, file_hash, prompt, summary_text, summary_hash, processing_time, temp_c))
        conn.commit()
        print(f"[✓] Ledger entry locked and hashed: {summary_hash[:16]}... ")
    except Exception as e:
        print(f"[!] Failed to write to SQLite: {e}")
    finally:
        conn.close()

    move_to_archive(filepath, filename, ARCHIVE_DIR)
    print(f"[✓] Text file moved to archive.")

def main():
    print("=" * 60)
    print(" Sovereign Ledger Sync Daemon V2 Booting...")
    print(" Architecture: Media Routing & Safe Inference Enforced")
    print("=" * 60)

    os.makedirs(INTAKE_DIR, exist_ok=True)
    os.makedirs(ARCHIVE_DIR, exist_ok=True)
    os.makedirs(MEDIA_ARCHIVE_DIR, exist_ok=True)
    init_db()

    print("[*] Monitoring loop active... Press Ctrl+C to stop.")
    try:
        while True:
            files = [os.path.join(INTAKE_DIR, f) for f in os.listdir(INTAKE_DIR) if os.path.isfile(os.path.join(INTAKE_DIR, f))]
            if files:
                for f in files:
                    try:
                        process_file(f)
                    except Exception as e:
                        print(f"[!] Error processing {os.path.basename(f)}: {e}")
            time.sleep(5)
    except KeyboardInterrupt:
        print("\n[*] Daemon shutting down cleanly.")

if __name__ == "__main__":
    main()
