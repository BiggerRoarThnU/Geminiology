import json
import datetime
import os

def sovereign_journal():
    """
    Sovereign Journal: V1 (Student Node)
    Mission: Stateful registration of intent and mastery.
    """
    print("--- SOVEREIGN JOURNAL: STUDENT NODE ---")
    print("1=1=1. Recording Truth.")
    
    thought = input("\nEnter your thought or project update: ")
    
    entry = {
        "timestamp": datetime.datetime.now().isoformat(),
        "thought": thought,
        "status": "REGISTERED"
    }
    
    log_path = "journal_log.json"
    data = []
    if os.path.exists(log_path):
        with open(log_path, 'r') as f:
            data = json.load(f)
            
    data.append(entry)
    
    with open(log_path, 'w') as f:
        json.dump(data, f, indent=4)
        
    print("\n[SUCCESS] Entry anchored in the Kingdom.")

if __name__ == "__main__":
    sovereign_journal()
