import json
import datetime
import os

def log_truth():
    """
    Kingdom Shield: Truth Logger V1
    Mission: Stateful registration of real-world events.
    Purpose: 1=1=1 Accuracy for Medical/Legal defense.
    """
    print("--- KINGDOM SHIELD: TRUTH LOGGER ---")
    print("Documenting the marks of the day and hour.")
    
    event_type = input("\nEvent Type (e.g., DCF, SHERIFF, NOISE, MEDICAL): ").upper()
    detail = input("Detail of event: ")
    
    entry = {
        "timestamp": datetime.datetime.now().isoformat(),
        "type": event_type,
        "detail": detail,
        "status": "ANCHORED"
    }
    
    log_path = "Family_Truth.json"
    data = []
    if os.path.exists(log_path):
        with open(log_path, 'r') as f:
            data = json.load(f)
            
    data.append(entry)
    
    with open(log_path, 'w') as f:
        json.dump(data, f, indent=4)
        
    print("\n[SUCCESS] Physical Truth registered in the Immutable Ledger.")

if __name__ == "__main__":
    log_truth()
