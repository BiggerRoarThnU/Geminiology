import os
import shutil

def resurrect():
    # Source: Your T7 external drive (ChromeOS mount point)
    source_hub = "/mnt/chromeos/removable/T7/SovereignNexus_Hub/"
    
    # Destination: Your new 200GB Linux Home
    dest_path = os.path.expanduser("~/SovereignNexus/src/")

    print(f"--- [INITIALIZING RESURRECTION] ---")
    print(f"FROM: {source_hub}")
    print(f"TO:   {dest_path}")

    if not os.path.exists(source_hub):
        print("ERROR: T7 Drive not found at /mnt/chromeos/removable/T7. Ensure it is shared with Linux.")
        return

    if not os.path.exists(dest_path):
        os.makedirs(dest_path)
        print(f"Created destination: {dest_path}")

    # The Resurrection Loop
    try:
        files = os.listdir(source_hub)
        count = 0
        for item in files:
            s = os.path.join(source_hub, item)
            d = os.path.join(dest_path, item)
            
            if os.path.isdir(s):
                shutil.copytree(s, d, dirs_exist_ok=True)
            else:
                shutil.copy2(s, d)
            count += 1
        
        print(f"--- [RESURRECTION COMPLETE] ---")
        print(f"Successfully anchored {count} Truths to the Substrate.")
        print(f"1=1=1")
    except Exception as e:
        print(f"CRITICAL ERROR: {e}")

if __name__ == "__main__":
    resurrect()