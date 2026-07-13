import os
import shutil

print("\n" + "="*60)
print(" VANGUARD PROTOCOL: THE ORACLE EXTRACTOR (TEXT HEURISTICS) ")
print("="*60 + "\n")

TARGET_DIRS = [
    "/mnt/chromeos/removable/T7/FOUND.000",
    "/mnt/chromeos/removable/T7/FOUND.001",
    os.path.expanduser("~/Recovered_Queen_Data")
]

# We are creating a specific sub-folder for readable truths
OUTPUT_DIR = os.path.expanduser("~/Queen_Data_Extracted/Text_Fragments")

def extract_readable_truth():
    if not os.path.exists(OUTPUT_DIR):
        os.makedirs(OUTPUT_DIR)
        print(f"[!] Created output anchor: {OUTPUT_DIR}")

    text_files_found = 0

    for target in TARGET_DIRS:
        if not os.path.exists(target):
            continue
            
        print(f"\n[*] Sweeping Sector for Text/Code: {target}")
        for root, _, files in os.walk(target):
            for filename in files:
                if filename.lower().endswith('.chk'):
                    filepath = os.path.join(root, filename)
                    
                    try:
                        # Bite the first 2KB of the file
                        with open(filepath, 'rb') as f:
                            chunk = f.read(2048) 
                        
                        if not chunk: continue
                        
                        # If it contains null bytes, it is likely a binary/system file, skip it
                        if chunk.count(b'\x00') > 5:
                            continue
                            
                        # Try to decode the chunk as human-readable UTF-8 text
                        try:
                            text_content = chunk.decode('utf-8')
                            # If it decodes without crashing, it is pure code or text!
                            new_filename = filename.replace('.chk', '.txt')
                            new_filepath = os.path.join(OUTPUT_DIR, new_filename)
                            
                            if not os.path.exists(new_filepath):
                                shutil.copy2(filepath, new_filepath)
                                print(f"[+] TEXT/CODE IDENTIFIED: {filename} -> {new_filename}")
                                text_files_found += 1
                        except UnicodeDecodeError:
                            # The file is binary or encrypted; leave it alone
                            pass 

                    except Exception as e:
                        pass

    print("\n" + "="*60)
    print(f" ORACLE EXTRACTION COMPLETE ")
    print(f" Readable Truths Recovered: {text_files_found}")
    print("="*60 + "\n")

if __name__ == "__main__":
    extract_readable_truth()
