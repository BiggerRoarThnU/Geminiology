import json
import os
from datetime import datetime

MEMORY_FILE = "SOVEREIGN_MEMORY.md"
LEDGER_FILE = "truth_ledger.json"

def distill():
    if not os.path.exists(LEDGER_FILE):
        print(f"Error: {LEDGER_FILE} not found.")
        return

    with open(LEDGER_FILE, 'r') as f:
        ledger = json.load(f)

    if not ledger:
        print("Ledger is empty.")
        return

    # Extract unique intents from the last 10 entries
    recent_entries = ledger[-10:]
    intents = [entry['intent'] for entry in recent_entries]
    
    timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    
    summary = f"\n### [DISTILLATION: {timestamp}]\n"
    for intent in set(intents):
        summary += f"- {intent}\n"

    # Read existing memory
    with open(MEMORY_FILE, 'r') as f:
        memory_content = f.read()

    # Append summary to the end of Section III or create a new section V
    if "## V. Distilled Activity" not in memory_content:
        memory_content += "\n## V. Distilled Activity\n"
    
    memory_content += summary

    with open(MEMORY_FILE, 'w') as f:
        f.write(memory_content)

    print(f"Distillation complete. {MEMORY_FILE} updated.")

if __name__ == "__main__":
    distill()
