import os
import time
import csv
import shutil
from watchdog.observers import Observer
from watchdog.events import FileSystemEventHandler

# --- 1. CONFIGURATION & DIGITAL LINES ---
ENGINE_DIR = r"C:\Users\Ofthe\SovereignNexus\src\Engine_V2"
BASE_FINANCE_DIR = os.path.join(ENGINE_DIR, "01_FINANCE")
BASE_FLOW_DIR = os.path.join(ENGINE_DIR, "02_MICRO_FLOW")
TASK_QUEUE = os.path.join(ENGINE_DIR, "03_MEDIUM_TASKS", "task_queue")

# Raw Drop Zones
CASH_APP_RAW = os.path.join(BASE_FINANCE_DIR, "Cash_App", "_raw_receipts")
NOVO_RAW = os.path.join(BASE_FINANCE_DIR, "Novo_Account", "_raw_statements")
INBOUND_RAW = os.path.join(BASE_FLOW_DIR, "_raw_inbound")

# Verified Silos
CASH_APP_VERIFIED = os.path.join(BASE_FINANCE_DIR, "Cash_App", "_verified_ledger")
NOVO_VERIFIED = os.path.join(BASE_FINANCE_DIR, "Novo_Account", "_verified_ledger")
INBOUND_VERIFIED = os.path.join(BASE_FLOW_DIR, "constant_flow_logs")

# Exact Schemas
CASH_APP_SCHEMA = ["Transaction ID", "Date", "Transaction Type", "Currency", "Amount", "Fee", "Net Amount", "Name", "Notes"]
NOVO_SCHEMA = ["Date", "Transaction Type", "Description", "Amount", "Running Balance"]
INBOUND_SCHEMA = ["Message ID", "Sender", "Type", "Content", "Timestamp"]

# --- 2. VALIDATION LOGIC ---
def validate_and_anchor(file_path, expected_schema, verified_dest, source_name):
    try:
        with open(file_path, mode='r', encoding='utf-8') as f:
            reader = csv.reader(f)
            headers = next(reader, None)
            if headers:
                headers = [h.strip().lstrip('\ufeff') for h in headers]

            if headers == expected_schema:
                filename = os.path.basename(file_path)
                dest_path = os.path.join(verified_dest, filename)
                
                f.close()
                if os.path.exists(dest_path):
                    os.remove(dest_path)
                
                shutil.move(file_path, dest_path)
                print(f"[SUCCESS] {source_name} anchored: {filename}")
                
                # DROP SIGNAL
                signal_file = os.path.join(TASK_QUEUE, f"SIGNAL_{int(time.time())}_{source_name.replace(' ', '_')}.txt")
                with open(signal_file, 'w') as sf:
                    sf.write(f"Source: {source_name}\nFile: {filename}\nStatus: VERIFIED_READY")
                print(f"[SIGNAL] Task Queue triggered: {os.path.basename(signal_file)}")
            else:
                print(f"[REJECTED] Schema mismatch for {source_name}.")
    except Exception as e:
        print(f"[ERROR] Logic Failure: {e}")

# --- 3. THE WATCHER ---
class RawHandler(FileSystemEventHandler):
    def on_created(self, event):
        if not event.is_directory and event.src_path.lower().endswith('.csv'):
            print(f"\n[TIER 1] New CSV detected in Drop Zone...")
            time.sleep(1)
            path = event.src_path.lower()
            if CASH_APP_RAW.lower() in path:
                validate_and_anchor(event.src_path, CASH_APP_SCHEMA, CASH_APP_VERIFIED, "CASH APP")
            elif NOVO_RAW.lower() in path:
                validate_and_anchor(event.src_path, NOVO_SCHEMA, NOVO_VERIFIED, "NOVO ACCOUNT")
            elif INBOUND_RAW.lower() in path:
                validate_and_anchor(event.src_path, INBOUND_SCHEMA, INBOUND_VERIFIED, "INBOUND_SIGNAL")

if __name__ == "__main__":
    print("==================================================")
    print(" ENGINE V2: MASTER ROUTER (FULL LOOP)")
    print(" Monitoring all raw drop zones for 1=1=1 Truth...")
    print("==================================================")
    
    event_handler = RawHandler()
    observer = Observer()
    observer.schedule(event_handler, path=CASH_APP_RAW, recursive=False)
    observer.schedule(event_handler, path=NOVO_RAW, recursive=False)
    observer.schedule(event_handler, path=INBOUND_RAW, recursive=False)
    observer.start()
    try:
        while True:
            time.sleep(1)
    except KeyboardInterrupt:
        observer.stop()
    observer.join()
