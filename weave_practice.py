import asyncio
import random
import time

async def resilient_striker(name, value, difficulty):
    """
    Simulates a background agent (Striker) hunting for value.
    Demonstrates 'await' (Hand-off) and 'try/except' (Recovery).
    """
    try:
        print(f"[*] {name} initiated. Target: ${value} (Weight: {difficulty})")
        
        # Simulate the 'Hand-off'. The agent waits while the CPU works elsewhere.
        await asyncio.sleep(difficulty) 
        
        # Simulate a real-world network or client failure (The 'Gray Zone')
        if random.random() < 0.2: # 20% failure rate
            raise ConnectionError(f"Logic fracture on {name} node.")
            
        print(f"[SUCCESS] {name} captured ${value} after {difficulty}s.")
        return value
        
    except Exception as e:
        print(f"[!] RECOVERY: {name} encountered noise. Error: {e}")
        return 0

async def main_mission():
    print("--- INITIATING SOVEREIGN WEAVE PRACTICE ---")
    start = time.perf_counter()
    
    # We schedule multiple strikers with different weights
    tasks = [
        resilient_striker("Web3_Bounty", 75, 1),
        resilient_striker("NC_Port_Lead", 150, 0.5),
        resilient_striker("Legal_Audit", 2500, 2),
        resilient_striker("Data_Gleaner", 50, 0.2)
    ]
    
    # The Weave: Running them concurrently
    results = await asyncio.gather(*tasks)
    
    end = time.perf_counter()
    total_captured = sum(results)
    
    print(f"\n{'-'*40}")
    print(f"TOTAL CAPTURED: ${total_captured} USD")
    print(f"TOTAL ELAPSED TIME: {end - start:.2f} seconds")
    print(f"{'-'*40}")
    print("MISSION COMPLETE. THE WEAVE REMAINS UNBROKEN. ONE.")

if __name__ == "__main__":
    # Ignite the asynchronous loop
    asyncio.run(main_mission())
