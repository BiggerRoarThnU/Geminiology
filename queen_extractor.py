import os
import shutil

print("\n" + "="*60)
print(" VANGUARD PROTOCOL: THE QUEEN EXTRACTOR ONLINE ")
print("="*60 + "\n")

# Hexadecimal Magic Numbers for file identification
MAGIC_NUMBERS = {
    b'\xFF\xD8\xFF': '.jpg',
    b'\x89PNG\r\n\x1a\n': '.png',
    b'%PDF': '.pdf',
    b'PK\x03\x04': '.zip', # Also covers .docx, .xlsx
    b'ID3': '.mp3',
    b'\x00\x00\x00\x14ftyp': '.mp4',
    b'\x00\x00\x00\x18ftyp': '.mp4',
    b'\x00\x00\x00\x20ftyp': '.mp4',
    b'Rar!\x1A\x07\x00': '.rar'
}

# Target both the T7 drive and your local copied folder
TARGET_DIRS = [
    "/mnt/chromeos/removable/T7/FOUND.000",
    "/mnt/chromeos/removable/T7/FOUND.001",
    os.path.expanduser("~/Recovered_Queen_Data")
]

OUTPUT_DIR = os.path.expanduser("~/Queen_Data_Extracted")

def extract_truth():
    if not os.path.exists(OUTPUT_DIR):
        os.makedirs(OUTPUT_DIR)
        print(f"[!] Created output anchor: {OUTPUT_DIR}")

    processed = 0
    unknown = 0

    for target in TARGET_DIRS:
        if not os.path.exists(target):
            continue
            
        print(f"\n[*] Sweeping Sector: {target}")
        for root, _, files in os.walk(target):
            for filename in files:
                if filename.lower().endswith('.chk'):
                    filepath = os.path.join(root, filename)
                    
                    try:
                        with open(filepath, 'rb') as f:
                            file_head = f.read(32)
                        
                        extension_found = False
                        for magic, ext in MAGIC_NUMBERS.items():
                            if file_head.startswith(magic):
                                new_filename = filename.replace('.chk', ext)
                                new_filepath = os.path.join(OUTPUT_DIR, new_filename)
                                
                                # Prevent overwriting if file already exists
                                if not os.path.exists(new_filepath):
                                    shutil.copy2(filepath, new_filepath)
                                    print(f"[+] EXTRACTED: {filename} -> {new_filename}")
                                else:
                                    print(f"[-] SKIPPED: {new_filename} (Already exists)")
                                
                                extension_found = True
                                processed += 1
                                break
                        
                        if not extension_found:
                            unknown += 1
                            
                    except Exception as e:
                        print(f"[X] ERROR reading {filename}: {e}")

    print("\n" + "="*60)
    print(f" EXTRACTION COMPLETE ")
    print(f" Truths Recovered: {processed}")
    print(f" Unknown Fragments: {unknown}")
    print("="*60 + "\n")

if __name__ == "__main__":
    extract_truth()
