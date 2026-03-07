import os
from datetime import datetime

# --- SOVEREIGN CONFIGURATION ---
vault_path = r"C:\Users\Ofthe\geminiology_one\ROOM_1_ARCHIVE\knowledge_vault"

def create_tome():
    print("=== THE ARCHIVIST IS READY ===")
    print(f"Target: {vault_path}")
    
    # 1. Name the Artifact
    title = input(">> Name of this Document (e.g., 'The_Gemini_Bridge'): ").replace(" ", "_")
    filename = f"{title}.txt"
    full_path = os.path.join(vault_path, filename)
    
    print(f"\n>> Paste the content of '{title}' below.")
    print(">> Press Ctrl+Z and Enter (Windows) or Ctrl+D (Linux/Mac) on a new line to save.")
    print("-" * 40)
    
    # 2. Ingest the Data (The Transmutation)
    lines = []
    try:
        while True:
            line = input()
            lines.append(line)
    except EOFError:
        pass # This catches the Ctrl+Z signal
    
    # 3. Seal the Tome
    timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    header = f"--- IRONWOOD ARCHIVE: {title} ---\n--- CAPTURED: {timestamp} ---\n\n"
    
    content = "\n".join(lines)
    
    with open(full_path, "w", encoding="utf-8") as f:
        f.write(header + content)
        
    print("-" * 40)
    print(f"✅ TOME SEALED: {filename}")
    print(f"📍 Location: {full_path}")

if __name__ == "__main__":
    create_tome()