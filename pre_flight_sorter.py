import os
import shutil
from pathlib import Path

def get_image_type(file_path):
    """
    Check the magic numbers of a file to determine if it is a JPEG, PNG, or GIF.
    """
    try:
        with open(file_path, 'rb') as f:
            header = f.read(12)
            if header.startswith(b'\xff\xd8\xff'):
                return 'jpeg'
            if header.startswith(b'\x89PNG\r\n\x1a\n'):
                return 'png'
            if header.startswith(b'GIF87a') or header.startswith(b'GIF89a'):
                return 'gif'
    except Exception as e:
        print(f"Error reading {file_path}: {e}")
    return None

def sweep_and_sort_archive(archive_path: str):
    """
    The Pre-Flight Sorter: Scans the archive, verifies true file types,
    and isolates incompatible formats to protect the 8GB Reality spin.
    """
    base_dir = Path(archive_path)
    
    # Create a quarantine zone for wild cards (like .gifs or mislabeled files)
    quarantine_dir = base_dir / "WILD_CARDS_QUARANTINE"
    quarantine_dir.mkdir(exist_ok=True)
    
    # Create a clean zone for verified, API-ready images
    clean_dir = base_dir / "API_READY_IMAGES"
    clean_dir.mkdir(exist_ok=True)

    print(f"Initiating Sweep on: {base_dir}")
    
    # Iterate through all files in the archive
    for item in base_dir.iterdir():
        if item.is_file() and item.name.lower().startswith("blood"):
            print(f"Inspecting: {item.name}...")
            
            # The Hands-and-Knees Check: What is the actual data?
            actual_type = get_image_type(item)
            
            if actual_type in ['jpeg', 'png']:
                # The data is true. It matches the API parameters.
                shutil.move(str(item), str(clean_dir / item.name))
                print(f"  -> Verified and moved to Clean Zone.")
                
            elif actual_type == 'gif':
                # The data is a wild card. It will lock up the API.
                shutil.move(str(item), str(quarantine_dir / item.name))
                print(f"  -> Wild Card (.gif) detected. Moved to Quarantine.")
                
            elif actual_type is None:
                # The file is not an image (e.g., it's actually a .txt file)
                print(f"  -> Anomaly detected: Not a valid image structure.")
                # We rename it to .txt so the system knows how to handle it
                if item.suffix.lower() != '.txt':
                    new_name = item.with_suffix('.txt')
                    if new_name.exists():
                        new_name = new_name.with_name(f"{new_name.stem}_renamed{new_name.suffix}")
                    item.rename(new_name)
                    shutil.move(str(new_name), str(quarantine_dir / new_name.name))
                    print(f"  -> Renamed to .txt and Quarantined.")
                else:
                    shutil.move(str(item), str(quarantine_dir / item.name))
                    print(f"  -> .txt file detected. Moved to Quarantine.")

    print("\nSweep Complete. The truth is sorted and the pipeline is safe.")

if __name__ == "__main__":
    # Point this to your specific archive folder
    target_directory = r"C:\Users\Ofthe\SovereignNexus\src\Ironwood\09_ARCHIVE"
    sweep_and_sort_archive(target_directory)
