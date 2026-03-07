import sys
import datetime
import os
# We import your ledger tool to handle the payment
from perc_ledger import log_transaction

JOURNAL_FILE = r"C:\Users\Ofthe\SovereignNexus\Active_Protocols\journal_log.txt"

def scribe_entry(text):
    timestamp = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    
    # 1. Format the Entry
    entry = f"[{timestamp}] {text}\n"
    
    print(f"--- ACCESSING MEMORY CORES ---")
    
    try:
        # 2. Append to the Journal (The "a" flag means append)
        with open(JOURNAL_FILE, "a") as f:
            f.write(entry)
        
        print(f"STATUS: Thought preserved in journal_log.txt")
        
        # 3. The Reward (Data is Value)
        # We value a thought at 5 minutes of work (2.5m reward)
        log_transaction("Journal Entry", 5)
        
    except Exception as e:
        print(f"ERROR: Write failed. {e}")

if __name__ == "__main__":
    # Usage: python src/scribe.py "My thought here"
    if len(sys.argv) > 1:
        # We join all arguments so you don't need perfect quotes
        message = " ".join(sys.argv[1:])
        scribe_entry(message)
    else:
        print('ERROR: Empty mind. Usage -> python src/scribe.py "Your thought"')