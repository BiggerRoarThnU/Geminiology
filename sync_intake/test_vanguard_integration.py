#!/usr/bin/env python3
import sys
import os
import sqlite3
import time

sys.path.append("/home/geminiology")
from vanguard_core_protocols import execute_night_watch

def test_integration():
    db_path = "/home/geminiology/sovereign_memory.db"
    
    # 1. Clean previous test entries to have a clear benchmark
    print("🧹 Cleaning database test entries...")
    conn = sqlite3.connect(db_path)
    cursor = conn.cursor()
    cursor.execute("DELETE FROM prime_ledger WHERE user_id = 'Swarm_Agent'")
    cursor.execute("DELETE FROM suspension_gate WHERE user_id = 'Swarm_Agent'")
    conn.commit()
    conn.close()
    
    # 2. Create a temporary high-variance dummy file in a temp directory
    temp_dir = "/home/geminiology/temp_test_dir"
    os.makedirs(temp_dir, exist_ok=True)
    
    dummy_file = os.path.join(temp_dir, "noisy_temp_file.txt")
    with open(dummy_file, "w") as f:
        # Write exactly 120 lines (10 lines per agent for 12 agents)
        # Inside each block of 10 lines, lengths vary extremely: 1, 100, 2, 200, 3, 300, etc.
        # This guarantees standard deviation is high and Coefficient of Variation > 0.15.
        for agent in range(12):
            for i in range(5):
                f.write("x" * (i * 100 + 1) + "\n")
                f.write("y" * (i * 2 + 1) + "\n")
        
    print(f"🚀 Running execute_night_watch on: {temp_dir}")
    execute_night_watch(target_paths=[temp_dir], ingestion_speed=0.0, variance_threshold=0.15, max_workers=2)
    
    # Clean up dummy file
    if os.path.exists(dummy_file):
        os.remove(dummy_file)
    if os.path.exists(temp_dir):
        os.rmdir(temp_dir)
        
    # 3. Check if entries were added to the database
    print("\n📊 Checking database after scan:")
    conn = sqlite3.connect(db_path)
    cursor = conn.cursor()
    
    cursor.execute("SELECT COUNT(*) FROM prime_ledger WHERE user_id = 'Swarm_Agent'")
    prime_count = cursor.fetchone()[0]
    
    cursor.execute("SELECT COUNT(*) FROM suspension_gate WHERE user_id = 'Swarm_Agent'")
    suspension_count = cursor.fetchone()[0]
    
    print(f"   - Prime Ledger Count (Verified): {prime_count}")
    print(f"   - Suspension Gate Count (Non-verified): {suspension_count}")
    
    # Print some entries
    cursor.execute("SELECT content, decay_rate, unix_time FROM suspension_gate WHERE user_id = 'Swarm_Agent' LIMIT 3")
    rows = cursor.fetchall()
    for row in rows:
        print(f"     • Content: {row[0][:70]}... | Decay Rate: {row[1]} | Time: {row[2]}")
        
    conn.close()
    
    # Ensure we actually have entries in suspension gate to prune
    if suspension_count == 0:
        print("\n❌ INTEGRATION TEST FAILED: No entries in suspension gate to test pruning.")
        return

    # 4. Test Dynamic Decay Pruning with a simulation multiplier
    print("\n⏰ Simulating 1000 seconds of elapsed time to test dynamic decay...")
    from sovereign_memory_core import SovereignMemoryNode
    node = SovereignMemoryNode()
    
    # This will simulate decay over time and delete entries with weight < 0.1
    # decay_rate is 0.02, so for weight to fall below 0.1:
    # e^(-0.02 * elapsed) < 0.1 => -0.02 * elapsed < ln(0.1) => -0.02 * elapsed < -2.3025 => elapsed > 115 seconds.
    # With a 1000x multiplier, 1 real second represents 1000 simulated seconds (far exceeding 115s).
    time.sleep(1.0)
    node.prune_decayed_memories(threshold=0.1, time_multiplier=1000.0)
    
    # 5. Check database counts again
    print("\n📊 Checking database after simulated pruning:")
    conn = sqlite3.connect(db_path)
    cursor = conn.cursor()
    
    cursor.execute("SELECT COUNT(*) FROM prime_ledger WHERE user_id = 'Swarm_Agent'")
    prime_count_after = cursor.fetchone()[0]
    
    cursor.execute("SELECT COUNT(*) FROM suspension_gate WHERE user_id = 'Swarm_Agent'")
    suspension_count_after = cursor.fetchone()[0]
    
    print(f"   - Prime Ledger Count: {prime_count_after}")
    print(f"   - Suspension Gate Count: {suspension_count_after}")
    
    conn.close()
    
    if suspension_count_after < suspension_count:
        print("\n✅ INTEGRATION TEST PASSED: Decayed log files successfully pruned!")
    else:
        print("\n❌ INTEGRATION TEST FAILED: Decayed log files were not pruned.")

if __name__ == "__main__":
    test_integration()
