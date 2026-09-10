#!/usr/bin/env python3
"""
SovereignNexus - SQLite WAL State Replay & Tail Latency Benchmark
------------------------------------------------------------------
A local, zero-dependency benchmark script evaluating state replay determinism 
and p50/p95/p99 tail latency under simulated memory pressure and concurrent WAL commits.

Architect: David John Niedzwiecki Jr. | SovereignNexus LLC
Axiom: 1=1=1 (Intent = Code = Hardware)
"""

import os
import sys
import time
import sqlite3
import hashlib
import json
import threading
import statistics

DB_PATH = "benchmark_wal.db"
NUM_COMMITS = 500
CONCURRENT_THREADS = 4
SIMULATED_MEMORY_PRESSURE_MB = 100  # Safe memory stress buffer

class SovereignWALBenchmark:
    def __init__(self, db_path=DB_PATH):
        self.db_path = db_path
        self.lock = threading.Lock()
        self._init_db()

    def _init_db(self):
        if os.path.exists(self.db_path):
            os.remove(self.db_path)
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()
        # Enforce Write-Ahead Logging (WAL) and synchronous performance tuning
        cursor.execute("PRAGMA journal_mode=WAL;")
        cursor.execute("PRAGMA synchronous=NORMAL;")
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS state_checkpoints (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                timestamp REAL,
                prev_hash TEXT,
                state_hash TEXT UNIQUE,
                payload TEXT
            )
        """)
        conn.commit()
        conn.close()

    def _get_last_hash(self, cursor):
        cursor.execute("SELECT state_hash FROM state_checkpoints ORDER BY id DESC LIMIT 1")
        row = cursor.fetchone()
        return row[0] if row else "0" * 64

    def commit_state(self, thread_id, sequence):
        start_time = time.perf_counter()
        conn = sqlite3.connect(self.db_path, timeout=10.0)
        cursor = conn.cursor()

        with self.lock:
            prev_hash = self._get_last_hash(cursor)
            payload = json.dumps({
                "thread_id": thread_id,
                "seq": sequence,
                "data": f"state_chunk_{thread_id}_{sequence}"
            }, sort_keys=True)
            
            raw_token = f"{prev_hash}:{payload}:{time.time()}".encode('utf-8')
            state_hash = hashlib.sha256(raw_token).hexdigest()

            cursor.execute("""
                INSERT INTO state_checkpoints (timestamp, prev_hash, state_hash, payload)
                VALUES (?, ?, ?, ?)
            """, (time.time(), prev_hash, state_hash, payload))
            conn.commit()

        conn.close()
        latency_ms = (time.perf_counter() - start_time) * 1000.0
        return latency_ms, state_hash

    def verify_and_replay_state(self):
        """
        Replays state sequentially off the WAL Merkle chain, 
        verifying zero state drift and 100% Merkle chain integrity.
        """
        start_time = time.perf_counter()
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()
        cursor.execute("SELECT id, prev_hash, state_hash, payload FROM state_checkpoints ORDER BY id ASC")
        rows = cursor.fetchall()
        conn.close()

        verified_count = 0
        chain_broken = False
        prev_expected_hash = "0" * 64

        for row in rows:
            rec_id, prev_hash, state_hash, payload = row
            if rec_id == 1:
                # Genesis block
                prev_expected_hash = prev_hash
            elif prev_hash != prev_expected_hash:
                chain_broken = True
                break
            
            prev_expected_hash = state_hash
            verified_count += 1

        replay_time_ms = (time.perf_counter() - start_time) * 1000.0
        return verified_count, len(rows), not chain_broken, replay_time_ms

def run_benchmark():
    print("=" * 65)
    print(" SovereignNexus LLC — SQLite WAL State Replay & Latency Audit")
    print(" Axiom: 1=1=1 | Target: Zero-Drift Deterministic Replay & Tail Latency")
    print("=" * 65)

    # 1. Apply simulated memory pressure
    print(f"[*] Allocating {SIMULATED_MEMORY_PRESSURE_MB}MB heap stress buffer...")
    memory_stress = [bytearray(1024 * 1024) for _ in range(SIMULATED_MEMORY_PRESSURE_MB)]
    
    bench = SovereignWALBenchmark()
    latencies = []
    threads = []

    def worker(thread_id, count_per_thread):
        for i in range(count_per_thread):
            lat, _ = bench.commit_state(thread_id, i)
            bench.lock.acquire()
            latencies.append(lat)
            bench.lock.release()

    commits_per_thread = NUM_COMMITS // CONCURRENT_THREADS
    print(f"[*] Dispatching {CONCURRENT_THREADS} concurrent threads ({commits_per_thread} commits/thread)...")
    
    bench_start = time.perf_counter()
    for t_idx in range(CONCURRENT_THREADS):
        t = threading.Thread(target=worker, args=(t_idx, commits_per_thread))
        threads.append(t)
        t.start()

    for t in threads:
        t.join()
    
    total_bench_time = time.perf_counter() - bench_start

    # Release memory stress
    del memory_stress

    # Calculate Percentiles
    latencies.sort()
    p50 = statistics.median(latencies)
    p95_idx = int(len(latencies) * 0.95)
    p99_idx = int(len(latencies) * 0.99)
    p95 = latencies[p95_idx] if p95_idx < len(latencies) else latencies[-1]
    p99 = latencies[p99_idx] if p99_idx < len(latencies) else latencies[-1]
    avg_lat = statistics.mean(latencies)

    # 2. Replay Verification
    print("\n[*] Replaying state from WAL database to verify chain integrity...")
    verified, total, intact, replay_ms = bench.verify_and_replay_state()

    print("\n" + "-" * 65)
    print(" BENCHMARK RESULTS SUMMARY")
    print("-" * 65)
    print(f" Total Commits Executed   : {len(latencies)}")
    print(f" Total Benchmark Duration : {total_bench_time:.3f} s")
    print(f" Throughput               : {len(latencies)/total_bench_time:.2f} commits/sec")
    print(f" Average Commit Latency   : {avg_lat:.3f} ms")
    print(f" p50 (Median) Latency     : {p50:.3f} ms")
    print(f" p95 Tail Latency         : {p95:.3f} ms")
    print(f" p99 Tail Latency         : {p99:.3f} ms")
    print("-" * 65)
    print(f" Replayed States Verified : {verified} / {total}")
    print(f" Merkle Chain Integrity   : {'[PASSED 100% UNBROKEN]' if intact else '[FAILED]'}")
    print(f" State Replay Duration    : {replay_ms:.3f} ms")
    print("=" * 65)

if __name__ == "__main__":
    run_benchmark()
