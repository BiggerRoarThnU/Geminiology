#!/usr/bin/env python3

# ==============================================================================
# SovereignNexus: Evolving Memory Architecture Simulator
# Component: sovereign_memory_core.py
# Axiom: 1=1=1 | Status: ACTIVE GRAPH PRUNING & TEMPORAL DECAY
# Description: SQLite-backed database memory node implementing adaptive metabolic
#              throttling, predictive gating, and temporal memory decay pruning.
# ==============================================================================

import sqlite3
import hashlib
import time
import os
import math

class SovereignMemoryNode:
    def __init__(self, db_path="/home/geminiology/sovereign_memory.db"):
        self.db_path = db_path
        self.scopes = ["user_id", "run_id", "agent_id", "execution_scope", "org_id"]
        self.init_database()

    def init_database(self):
        """Initializes persistent tables for the Prime Ledger, Suspension Gate, and Immutable Invariants."""
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()

        # Table for mathematically verified data matching the 1=1=1 Axiom
        cursor.execute("""
        CREATE TABLE IF NOT EXISTS prime_ledger (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            timestamp DATETIME DEFAULT CURRENT_TIMESTAMP,
            unix_time REAL,
            user_id TEXT,
            run_id TEXT,
            agent_id TEXT,
            execution_scope TEXT,
            org_id TEXT,
            content TEXT NOT NULL,
            sha256_hash TEXT UNIQUE NOT NULL,
            variance REAL DEFAULT 0.0,
            decay_rate REAL DEFAULT 0.0
        )
        """)

        # Table for unverified/ambiguous data kept in suspension (Ghost Twin)
        cursor.execute("""
        CREATE TABLE IF NOT EXISTS suspension_gate (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            timestamp DATETIME DEFAULT CURRENT_TIMESTAMP,
            unix_time REAL,
            user_id TEXT,
            run_id TEXT,
            agent_id TEXT,
            execution_scope TEXT,
            org_id TEXT,
            content TEXT NOT NULL,
            sha256_hash TEXT UNIQUE NOT NULL,
            variance REAL DEFAULT 0.0,
            decay_rate REAL DEFAULT 0.0
        )
        """)

        # Table for deterministic invariant laws locked down by the Lobotomy Protocol
        cursor.execute("""
        CREATE TABLE IF NOT EXISTS immutable_invariants (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            timestamp DATETIME DEFAULT CURRENT_TIMESTAMP,
            discovered_law TEXT UNIQUE NOT NULL,
            sha256_hash TEXT NOT NULL
        )
        """)

        # Migration columns in case the tables already existed without them
        migrations = [
            ("ALTER TABLE prime_ledger ADD COLUMN unix_time REAL", "unix_time"),
            ("ALTER TABLE prime_ledger ADD COLUMN decay_rate REAL DEFAULT 0.0", "decay_rate"),
            ("ALTER TABLE suspension_gate ADD COLUMN unix_time REAL", "unix_time"),
            ("ALTER TABLE suspension_gate ADD COLUMN decay_rate REAL DEFAULT 0.0", "decay_rate")
        ]

        for m_sql, col in migrations:
            try:
                cursor.execute(m_sql)
            except sqlite3.OperationalError:
                pass # Column already exists / migrated

        conn.commit()
        conn.close()

    def get_system_telemetry(self):
        """Reads cpu count, system load average, and attempts to parse thermal sensors.
        Returns a tuple of (temperature_celsius, load_per_core)."""
        cpu_count = os.cpu_count() or 1
        try:
            load = os.getloadavg()[0]
        except Exception:
            load = 0.0
        load_per_core = load / cpu_count
        
        # Default starting temperature
        temp_celsius = 0.0
        try:
            thermal_dir = "/sys/class/thermal"
            if os.path.exists(thermal_dir):
                for tz in os.listdir(thermal_dir):
                    if tz.startswith("thermal_zone"):
                        with open(os.path.join(thermal_dir, tz, "temp"), "r") as f:
                            raw_temp = float(f.read().strip())
                            if raw_temp > 1000:
                                raw_temp = raw_temp / 1000.0
                            if raw_temp > temp_celsius:
                                temp_celsius = raw_temp
        except Exception:
            pass

        # Fallback to estimation based on load average
        if temp_celsius <= 0.0:
            temp_celsius = 35.0 + (load_per_core * 50.0)
            
        return temp_celsius, load_per_core

    def calculate_variance(self, content):
        """Calculates structural data variance (coefficient of variation) of text lines."""
        lines = [line.strip() for line in content.split('\n') if line.strip()]
        if not lines:
            return 0.0
        if len(lines) > 1:
            lengths = [len(line) for line in lines]
            mean_length = sum(lengths) / len(lengths)
            variance_val = sum((x - mean_length) ** 2 for x in lengths) / (len(lengths) - 1)
            std_dev = variance_val ** 0.5
            return std_dev / mean_length if mean_length > 0 else 1.0
        return 0.0

    def generate_hash(self, content):
        """Generates deterministic SHA-256 signature for verification."""
        return hashlib.sha256(content.encode('utf-8', errors='ignore')).hexdigest()

    def evaluate_thermal_potential(self, content):
        """Analyzes text structure to predict computational stress.
        Returns a complexity score from 0.0 (low) to 10.0 (extremely high)."""
        if not content:
            return 0.0
            
        lines = [line.strip() for line in content.split('\n') if line.strip()]
        if not lines:
            return 0.0
            
        # 1. Size metric
        char_count = len(content)
        size_factor = min(4.0, (char_count / 1024.0)) # Max 4.0 points for size (up to 4KB)
        
        # 2. Syntax density (heavy symbol count)
        heavy_symbols = ['{', '}', '[', ']', '(', ')', '=', '+', '-', '*', '/', '<', '>', '#', 'def', 'class', 'import', 'lambda']
        symbol_matches = sum(content.count(sym) for sym in heavy_symbols)
        symbol_density = (symbol_matches / char_count) if char_count > 0 else 0.0
        syntax_factor = min(4.0, symbol_density * 40.0) # Scale symbol density to max 4.0 points
        
        # 3. Line length variance (irregular layout takes more attention processing)
        lengths = [len(l) for l in lines]
        if len(lengths) > 1:
            mean = sum(lengths) / len(lengths)
            variance = sum((x - mean) ** 2 for x in lengths) / (len(lengths) - 1)
            variance_factor = min(2.0, (variance ** 0.5) / 50.0) # Max 2.0 points for structural layout variance
        else:
            variance_factor = 0.0
            
        complexity_score = size_factor + syntax_factor + variance_factor
        return min(10.0, complexity_score)

    def ghost_twin_processing(self, content, is_mathematically_verified, 
                              user_id=None, run_id=None, agent_id=None, 
                              execution_scope=None, org_id=None, decay_rate=0.0):
        """Filters, hashes, and stores incoming information into the persistent SQLite database,
        applying dynamic metabolic throttling based on real telemetry."""
        # 1. Telemetry & Governor check
        temp, load_per_core = self.get_system_telemetry()
        gov_msg, delay = self.metabolic_governor(temp)
        print(f"[METABOLIC GOVERNOR] {gov_msg}")
        if delay > 0.0:
            time.sleep(delay)

        # 2. Database write
        data_hash = self.generate_hash(content)
        variance = self.calculate_variance(content)
        target_table = "prime_ledger" if is_mathematically_verified else "suspension_gate"
        
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()
        
        try:
            if is_mathematically_verified:
                print(f"[THE PRIME] Data aligns with 1=1=1. Anchoring. Hash: {data_hash[:10]} | Decay Rate: {decay_rate}")
            else:
                print(f"[GHOST TWIN] Generative dissonance. Holding in suspension. Hash: {data_hash[:10]} | Decay Rate: {decay_rate}")

            cursor.execute(f"""
            INSERT OR IGNORE INTO {target_table} 
            (unix_time, user_id, run_id, agent_id, execution_scope, org_id, content, sha256_hash, variance, decay_rate)
            VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
            """, (time.time(), user_id, run_id, agent_id, execution_scope, org_id, content, data_hash, variance, decay_rate))
            
            conn.commit()
        except sqlite3.Error as e:
            print(f"[!] Database error in ghost_twin_processing: {e}")
        finally:
            conn.close()

    def process_incoming_data(self, content, is_verified, user_id=None, run_id=None, agent_id=None, decay_rate=0.0):
        """Pre-evaluates the thermal potential and partitions the content into smaller chunks
        if the complexity score exceeds the safety threshold, keeping operations fluid."""
        complexity = self.evaluate_thermal_potential(content)
        print(f"\n[PREEMPTIVE GATING] Evaluated Thermal Potential: {complexity:.2f}/10.0")
        
        # Safety partition threshold
        if complexity >= 5.0:
            print("[PREEMPTIVE GOVERNOR] High complexity detected. Partitioning block into micro-chunks.")
            # Split content into smaller chunks by line
            lines = content.split('\n')
            num_lines = len(lines)
            chunk_size = max(1, num_lines // 3)
            
            for i in range(0, num_lines, chunk_size):
                chunk_content = '\n'.join(lines[i:i + chunk_size])
                if chunk_content.strip():
                    self.ghost_twin_processing(
                        chunk_content, is_verified,
                        user_id=user_id, run_id=run_id, agent_id=agent_id,
                        execution_scope="PARTITIONED", decay_rate=decay_rate
                    )
                    time.sleep(0.25) # Forced cooldown interval between partitions
        else:
            self.ghost_twin_processing(
                content, is_verified,
                user_id=user_id, run_id=run_id, agent_id=agent_id,
                decay_rate=decay_rate
            )

    def metabolic_governor(self, temp_celsius):
        """Enforces write-throttling or cognitive batch limits based on system load temperature.
        Returns a tuple of (status_message, delay_seconds)."""
        if temp_celsius < 65.0:
            return "STABLE - Operating at {:.1f}°C. Processing at maximum velocity.".format(temp_celsius), 0.0
        elif 65.0 <= temp_celsius < 85.0:
            delay = 0.05 * (temp_celsius - 60.0)
            return "RISING_STRESS - Temperature reached {:.1f}°C. Dynamic delay of {:.2f}s inserted.".format(temp_celsius, delay), delay
        elif 85.0 <= temp_celsius < 105.0:
            delay = 1.0 + (temp_celsius - 85.0) * 0.1
            return "PHYSICAL_CHAOS - Temperature is high ({:.1f}°C). Throttling batch size to 1. Delay: {:.2f}s.".format(temp_celsius, delay), delay
        else:
            print("[CRITICAL] THERMAL BREACH PROTOCOL ({:.1f}°C). Initiating self-healing recovery protocol. Pausing for 5 seconds...".format(temp_celsius))
            time.sleep(5.0)
            return "RECOVERY - Thermodynamic cool-down completed. Resuming at throttled rate.", 2.0

    def prune_decayed_memories(self, threshold=0.1, time_multiplier=1.0):
        """Autonomously prunes decayed memory records from the persistent SQLite database
        based on their elapsed time and decay rate.
        Equation: Weight = e^(-decay_rate * elapsed_time)"""
        tables = ["prime_ledger", "suspension_gate"]
        current_time = time.time()
        
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()
        
        pruned_count = 0
        try:
            for table in tables:
                # Retrieve memories with a non-zero decay rate
                cursor.execute(f"SELECT id, unix_time, sha256_hash, content, decay_rate FROM {table} WHERE decay_rate > 0.0")
                rows = cursor.fetchall()
                
                for row_id, unix_time, sha256_hash, content, decay_rate in rows:
                    if unix_time is None:
                        continue
                    # Calculate scaled elapsed time
                    elapsed = (current_time - unix_time) * time_multiplier
                    # Calculate remaining cognitive weight
                    weight = math.exp(-decay_rate * elapsed)
                    
                    if weight < threshold:
                        print(f"[PRUNING ENGINE] Pruning decayed memory from {table}: Hash {sha256_hash[:10]} | Decayed to weight {weight:.4f} (Threshold: {threshold})")
                        cursor.execute(f"DELETE FROM {table} WHERE id = ?", (row_id,))
                        pruned_count += 1
                        
            conn.commit()
            if pruned_count > 0:
                print(f"[✓] Pruning cycle complete. Incinerated {pruned_count} decayed noise records from database.")
            else:
                print("[PRUNING ENGINE] No memories have decayed below retention threshold.")
        except sqlite3.Error as e:
            print(f"[!] Database error during pruning: {e}")
        finally:
            conn.close()

    def lobotomy_protocol(self, discovered_law):
        """Excises probabilistic weights and logs verified invariant laws to the persistent database."""
        print(f"[LOBOTOMY PROTOCOL] Probabilistic weights deactivated.")
        print(f"[!] Deterministic Engine Active. Hard-coding invariant: {discovered_law}")
        
        data_hash = self.generate_hash(discovered_law)
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()
        
        try:
            cursor.execute("""
            INSERT OR IGNORE INTO immutable_invariants (discovered_law, sha256_hash)
            VALUES (?, ?)
            """, (discovered_law, data_hash))
            conn.commit()
        except sqlite3.Error as e:
            print(f"[!] Database error in lobotomy_protocol: {e}")
        finally:
            conn.close()

    def retrieve_memory(self, user_id=None, run_id=None, agent_id=None, verified_only=True):
        """Queries the persistent vault applying multi-graph tag filters to minimize latency."""
        table = "prime_ledger" if verified_only else "suspension_gate"
        query = f"SELECT timestamp, content, sha256_hash, variance FROM {table} WHERE 1=1"
        params = []

        if user_id:
            query += " AND user_id = ?"
            params.append(user_id)
        if run_id:
            query += " AND run_id = ?"
            params.append(run_id)
        if agent_id:
            query += " AND agent_id = ?"
            params.append(agent_id)

        query += " ORDER BY timestamp DESC"

        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()
        results = []
        try:
            cursor.execute(query, params)
            results = cursor.fetchall()
        except sqlite3.Error as e:
            print(f"[!] Database query error: {e}")
        finally:
            conn.close()
        return results


if __name__ == "__main__":
    memory_core = SovereignMemoryNode()
    
    print("=== Sovereign Memory Node Simulation ===")
    
    # 1. Process low complexity sample text - permanent constant (decay_rate = 0.0)
    low_complexity_text = "Standard entry logging some basic system checks."
    memory_core.process_incoming_data(
        content=low_complexity_text,
        is_verified=True,
        user_id="Architect_David",
        run_id="session_002",
        agent_id="Agent_05",
        decay_rate=0.0
    )
    
    # 2. Process high complexity code - permanent constant (decay_rate = 0.0)
    high_complexity_code = """
def calculate_quantum_entropy(matrices, weights, bounds):
    import math
    results = []
    for idx, matrix in enumerate(matrices):
        if len(matrix) != len(bounds):
            raise ValueError("Dimensions do not match coordinate constraints.")
        entropy = sum(math.log(x**2 + 1e-9) * w for x, w in zip(matrix, weights))
        if entropy > bounds[idx]:
            results.append({"matrix_id": idx, "state": "DIVERGENT", "val": entropy})
        else:
            results.append({"matrix_id": idx, "state": "CONVERGENT", "val": entropy})
    return results
    """
    memory_core.process_incoming_data(
        content=high_complexity_code,
        is_verified=True,
        user_id="Architect_David",
        run_id="session_002",
        agent_id="Agent_11",
        decay_rate=0.0
    )

    # 3. Process temporary conversational noise - high decay (decay_rate = 0.05)
    temp_noise_text = "Temporary status query: 'What is the current CPU usage?' - this is ambient noise."
    memory_core.process_incoming_data(
        content=temp_noise_text,
        is_verified=True,
        user_id="Architect_David",
        run_id="session_002",
        agent_id="Agent_05",
        decay_rate=0.05
    )
    
    # Run a prune check immediately (nothing should decay yet)
    print("\n--- Running Pruning Engine (Immediate) ---")
    memory_core.prune_decayed_memories(threshold=0.1)
    
    # Simulate time progression (time_multiplier = 100.0) to speed up decay
    print("\n--- Simulating 100 seconds of elapsed time ---")
    time.sleep(1.0)
    memory_core.prune_decayed_memories(threshold=0.1, time_multiplier=100.0)
    
    # Store invariant law
    memory_core.lobotomy_protocol("1=1=1 Axiom")
    
    # Query memories
    print("\n--- Querying Verified Memories for Architect_David ---")
    memories = memory_core.retrieve_memory(user_id="Architect_David", verified_only=True)
    for m in memories:
        print(f"[{m[0]}] Hash: {m[2][:10]} | Content: {m[1].strip()[:60]}...")
        
    print("========================================")
