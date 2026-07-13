import os
import binascii

print("\n" + "="*60)
print(" VANGUARD DIAGNOSTIC: HEXADECIMAL MICROSCOPE ")
print("="*60)

TARGET_DIR = "/mnt/chromeos/removable/T7/FOUND.001"
files_checked = 0

try:
    for filename in os.listdir(TARGET_DIR):
        if filename.lower().endswith('.chk'):
            filepath = os.path.join(TARGET_DIR, filename)
            
            with open(filepath, 'rb') as f:
                header = f.read(64) # Grab the first 64 bytes
            
            print(f"\n[+] FRAGMENT: {filename}")
            # Format the raw bytes into a readable hex grid
            hex_output = binascii.hexlify(header, ' ', 1).decode('ascii')
            print(hex_output.upper())
            
            files_checked += 1
            if files_checked >= 3: 
                break
                
except Exception as e:
    print(f"[X] ERROR: {e}")

print("\n" + "="*60 + "\n")
