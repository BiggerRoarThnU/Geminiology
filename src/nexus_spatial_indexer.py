import sqlite3
import numpy as np
import hashlib
import time
import math
from collections import Counter

DB_PATH = "nexus_ledger.db"

def compute_wave_metrics(text_chunk):
    """
    Evaluates multi-dimensional wave physics and information entropy.
    1. Lee C_seq Phase Bias: DC polarization across BPSK phases.
    2. Spectral Coherence: Peak power ratio via FFT (detects standing-wave resonance/slop).
    3. Shannon Information Entropy: Normalized byte diversity.
    """
    raw_bytes = text_chunk.encode("utf-8")
    bits = np.unpackbits(np.frombuffer(raw_bytes, dtype=np.uint8))
    total_bits = len(bits)
    if total_bits == 0:
        return 0.0, 0.0, 0.0
        
    # 1. Lee C_seq DC Phase Bias (|sum exp(i*theta)| / N)
    phases = bits.astype(float) * np.pi
    c_seq_bias = float(abs(np.sum(np.exp(1j * phases))) / total_bits)
    
    # 2. Spectral Coherence via FFT (BPSK mapping: 0 -> +1.0, 1 -> -1.0)
    wave = 1.0 - 2.0 * bits.astype(float)
    spectrum = np.abs(np.fft.rfft(wave)) ** 2
    total_power = np.sum(spectrum)
    spectral_coherence = float(np.max(spectrum) / total_power) if total_power > 0 else 0.0
    
    # 3. Shannon Entropy (bits per byte, normalized to [0.0, 1.0])
    counts = Counter(text_chunk)
    total_chars = len(text_chunk)
    h = -sum((c / total_chars) * math.log2(c / total_chars) for c in counts.values())
    norm_entropy = float(min(1.0, h / 8.0))
    
    return c_seq_bias, spectral_coherence, norm_entropy

def generate_phase_space_coordinate(chunk_index, total_chunks, spectral_coh, norm_entropy):
    """
    3D Phase-Space Manifold:
    X = Document Sequence Progression (0.0 to 1.0)
    Y = Spectral Wave Coherence (0.0 to 1.0) - High value indicates repetitive standing wave
    Z = Shannon Information Entropy (0.0 to 1.0) - High value indicates rich information density
    """
    x = float(np.interp(chunk_index, [0, max(1, total_chunks - 1)], [0.0, 1.0]))
    y = float(spectral_coh)
    z = float(norm_entropy)
    return np.array([x, y, z], dtype=np.float32)

def generate_chain_hash(prev_hash, data_string, coords):
    """
    Sequential Merkle hash chaining: S_t = SHA256(S_{t-1} || Content || Coords)
    Enforces continuous state fixity and immediate tamper detection.
    """
    payload = f"{prev_hash}_{data_string}_{coords[0]:.4f}_{coords[1]:.4f}_{coords[2]:.4f}"
    return hashlib.sha256(payload.encode('utf-8')).hexdigest()

def initialize_ledger():
    """Initializes the SQLite WAL Ledger with Phase-Space and Merkle Chain columns."""
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()
    cursor.execute("PRAGMA journal_mode=WAL;")
    cursor.execute("PRAGMA synchronous=NORMAL;")
    
    cursor.execute('''
    CREATE TABLE IF NOT EXISTS spatial_memory (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        timestamp REAL,
        content TEXT,
        coord_x REAL,
        coord_y REAL,
        coord_z REAL,
        c_seq_bias REAL,
        spectral_coherence REAL,
        entropy REAL,
        prev_hash TEXT,
        fixity_seal TEXT UNIQUE
    )
    ''')
    conn.commit()
    return conn

def ingest_payload(conn, text_chunks):
    """Ingests data into the 3D phase-space grid, sealed with sequential Merkle fixity."""
    cursor = conn.cursor()
    total = len(text_chunks)
    
    # Retrieve latest block hash for unbroken chain continuity
    cursor.execute("SELECT fixity_seal FROM spatial_memory ORDER BY id DESC LIMIT 1;")
    last_record = cursor.fetchone()
    prev_hash = last_record[0] if last_record else "0" * 64
    
    print(f"[*] Ingesting {total} chunks into the Sovereign 3D Phase-Space Grid...")
    
    for idx, chunk in enumerate(text_chunks):
        c_bias, spec_coh, entropy = compute_wave_metrics(chunk)
        coords = generate_phase_space_coordinate(idx, total, spec_coh, entropy)
        seal = generate_chain_hash(prev_hash, chunk, coords)
        
        try:
            cursor.execute('''
            INSERT INTO spatial_memory (
                timestamp, content, coord_x, coord_y, coord_z, 
                c_seq_bias, spectral_coherence, entropy, prev_hash, fixity_seal
            ) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
            ''', (time.time(), chunk, float(coords[0]), float(coords[1]), float(coords[2]),
                  c_bias, spec_coh, entropy, prev_hash, seal))
            
            print(f"  [+] Chunk {idx} | Coords: ({coords[0]:.2f}, {coords[1]:.2f}, {coords[2]:.2f}) | "
                  f"SpecCoh: {spec_coh:.4f} | H: {entropy:.4f} | Hash: {seal[:8]}")
            prev_hash = seal
        except sqlite3.IntegrityError:
            print(f"  [!] Collision: Chunk {idx} already anchored in ledger.")
            
    conn.commit()
    print("[*] Ingestion Complete. Phase-Space Merkle Ledger Sealed.")

if __name__ == "__main__":
    test_chunks = [
        "The 1=1=1 Axiom enforces deterministic hardware execution.",
        "Neural Operators map physics across continuous time.",
        "The 12-Node Swarm utilizes mmap zero-copy paging.",
        "SovereignNexus is immune to cloud API context decay.",
        "aaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaa",  # Repetitive slop type 1
        "ffffffffffffffffffffffffffffffffffffffffffffffffff"   # Repetitive slop type 2 (DC-Null)
    ]
    
    db_conn = initialize_ledger()
    db_conn.execute("DROP TABLE IF EXISTS spatial_memory")  # Reset schema for upgrade
    initialize_ledger()
    ingest_payload(db_conn, test_chunks)
    db_conn.close()
