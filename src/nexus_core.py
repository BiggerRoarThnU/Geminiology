#!/usr/bin/env python3
"""
SovereignNexus Core
Single Source of Truth for SQLite Schemas and Entropy Mathematics.
"""
import sqlite3
import math
import os
from collections import Counter

# Dynamic absolute pathing to prevent Crostini execution errors
ROOT_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
DB_PATH = os.path.join(ROOT_DIR, "nexus_ledger.db")

def calculate_shannon_entropy(text: str) -> float:
    """Calculates true character-level Shannon Entropy."""
    if not text:
        return 0.0
    length = len(text)
    frequencies = Counter(text)
    entropy = 0.0
    for freq in frequencies.values():
        p = freq / length
        entropy -= p * math.log2(p)
    return entropy

def verify_entropy_gate(text: str) -> bool:
    """
    Unified Lens 09 Rule: Enforces the Royal Seal standard (2.5 - 5.2).
    """
    h = calculate_shannon_entropy(text)
    return 2.5 <= h <= 5.2

def get_unified_db_connection():
    """
    Initializes the unified SQLite schema combining all required columns.
    Enforces WAL journal mode for edge concurrency.
    """
    conn = sqlite3.connect(DB_PATH)
    conn.execute("PRAGMA journal_mode = WAL;")
    cursor = conn.cursor()
    
    # The single, unified schema for routed_master_ledger
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS routed_master_ledger (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            timestamp DATETIME DEFAULT CURRENT_TIMESTAMP,
            node_id TEXT,
            node_name TEXT,
            triggering_agent TEXT,
            log_content TEXT,
            log_hash TEXT,
            signature TEXT
        )
    ''')
    conn.commit()
    return conn
