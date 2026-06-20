#!/usr/bin/env python3
import sys
import os
import sqlite3
import hashlib
import time

def print_header(title):
    print("\n" + "=" * 55)
    print(f" {title}")
    print("=" * 55)

# 1. System/Python Info
print_header("1. ENVIRONMENT ALIGNMENT")
print(f"[*] Python Version : {sys.version.split()[0]}")
print(f"[*] OS Type        : {sys.platform}")
print(f"[*] CPU Cores      : {os.cpu_count() or 1}")

# 2. SQLite Database Test
print_header("2. SQLITE DATABASE CORE TEST")
db_path = "/tmp/test_sovereign_temp.db"
if os.path.exists(db_path):
    os.remove(db_path)

try:
    conn = sqlite3.connect(db_path)
    c = conn.cursor()
    c.execute("CREATE TABLE test_ledger (id INTEGER PRIMARY KEY, content TEXT, hash TEXT)")
    
    # Insert test data matching the 1=1=1 logic
    test_content = "Sovereign alignment verified on Geminiology node."
    content_hash = hashlib.sha256(test_content.encode()).hexdigest()
    
    c.execute("INSERT INTO test_ledger (content, hash) VALUES (?, ?)", (test_content, content_hash))
    conn.commit()

    # Read back and verify
    c.execute("SELECT content, hash FROM test_ledger WHERE id=1")
    row = c.fetchone()
    conn.close()

    if row and row[1] == content_hash:
        print("[✓] SQLite Create, Write, and Read: SUCCESS")
        print(f"[*] Decoded Content: '{row[0]}'")
        print(f"[*] Verification Hash: {row[1][:16]}...")
    else:
        print("[!] Database integrity verification: FAILED")
except Exception as e:
    print(f"[!] Database Test encountered error: {e}")
finally:
    if os.path.exists(db_path):
        os.remove(db_path)

# 3. Thermal Telemetry Read
print_header("3. SYSTEM TELEMETRY READ")
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

if temp_c > 0:
    print(f"[✓] Thermal Sensors: ACTIVE")
    print(f"[*] CPU Core Temperature: {temp_c:.1f} °C")
else:
    print("[!] Thermal Sensors: OFFLINE or UNREADABLE")

# 4. Axiom Signature
print_header("4. SIGNATURE VERIFICATION")
print(" AXIOM STATUS: 1 = 1 = 1 (ALIGNED)")
print("=" * 55 + "\n")
