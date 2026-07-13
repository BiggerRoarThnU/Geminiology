import os
import zlib

print("\n" + "="*60)
print(" VANGUARD PROTOCOL: THE ZLIB DECOMPRESSOR ")
print("="*60 + "\n")

TARGET_DIRS = [
    "/mnt/chromeos/removable/T7/FOUND.000",
    "/mnt/chromeos/removable/T7/FOUND.001"
]

OUTPUT_DIR = os.path.expanduser("~/Queen_Data_Extracted/Unpacked_Truths")

def unpack_the_truth():
    if not os.path.exists(OUTPUT_DIR):
        os.makedirs(OUTPUT_DIR)
        print(f"[!] Created expansion chamber: {OUTPUT_DIR}")

    unpacked_count = 0

    for target in TARGET_DIRS:
        if not os.path.exists(target): 
            continue
            
        print(f"\n[*] Sweeping Sector for Zlib Compression: {target}")
        for root, _, files in os.walk(target):
            for filename in files:
                if filename.lower().endswith('.chk'):
                    filepath = os.path.join(root, filename)
                    
                    try:
                        with open(filepath, 'rb') as f:
                            raw_data = f.read()
                        
                        # 78 9C is the exact hex signature for zlib default compression
                        if raw_data.startswith(b'\x78\x9c'):
                            
                            # Inflate the data back to its true size
                            inflated_data = zlib.decompress(raw_data)
                            
                            # Try to decode it back into readable text
                            try:
                                text_content = inflated_data.decode('utf-8')
                                new_filename = filename.replace('.chk', '.txt')
                                new_filepath = os.path.join(OUTPUT_DIR, new_filename)
                                
                                with open(new_filepath, 'w', encoding='utf-8') as out_f:
                                    out_f.write(text_content)
                                
                                print(f"[+] INFLATED (Text): {filename} -> {new_filename}")
                                unpacked_count += 1
                                
                            except UnicodeDecodeError:
                                # It decompressed, but it's not text (could be a packed binary or model weight)
                                new_filename = filename.replace('.chk', '.bin')
                                new_filepath = os.path.join(OUTPUT_DIR, new_filename)
                                
                                with open(new_filepath, 'wb') as out_f:
                                    out_f.write(inflated_data)
                                    
                                print(f"[*] INFLATED (Binary): {filename} -> {new_filename}")
                                unpacked_count += 1
                                
                    except Exception as e:
                        # If the decompression fails, the fragment might be incomplete. We skip it quietly.
                        pass 

    print("\n" + "="*60)
    print(f" DECOMPRESSION COMPLETE ")
    print(f" Total Truths Restored: {unpacked_count}")
    print("="*60 + "\n")

if __name__ == "__main__":
    unpack_the_truth()
