#!/usr/bin/env python3
import sqlite3
import os

DB_PATH = os.path.expanduser("~/SovereignNexus/nexus_ledger.db")

def read_latest():
    conn = sqlite3.connect(DB_PATH)
    c = conn.cursor()
    # Pull the most recent entry
    c.execute("SELECT timestamp, filename, summary, summary_hash, processing_time, cpu_temp FROM file_sync_ledger ORDER BY id DESC LIMIT 1")
    row = c.fetchone()
    conn.close()

    if row:
        print("\n" + "="*60)
        print(" LATEST LEDGER ENTRY")
        print("="*60)
        print(f" Timestamp:  {row[0]}")
        print(f" Source File:{row[1]}")
        print(f" CPU Temp:   {row[5]:.1f} °C")
        print(f" Compute:    {row[4]:.2f} seconds")
        print(f" Truth Seal: {row[3]}")
        print("-" * 60)
        print(f"EXTRACTED SUMMARY:\n\n{row[2]}")
        print("="*60 + "\n")
    else:
        print("[!] The ledger is currently empty.")

if __name__ == "__main__":
    read_latest()
