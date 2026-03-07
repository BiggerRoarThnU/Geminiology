import cv2
import time
import os
from datetime import datetime

# --- Configuration ---
SAVE_DIR = r"C:\Users\Ofthe\SovereignNexus\src\Ironwood\02_SENTINEL\Video_Archive"
FILE_ROTATION_SECONDS = 1800  # 30 Minutes
FRAME_WIDTH = 1280
FRAME_HEIGHT = 720
FPS = 20.0

# Ensure the archive directory exists
if not os.path.exists(SAVE_DIR):
    os.makedirs(SAVE_DIR)

def start_recording():
    cap = cv2.VideoCapture(0) # Index 0 is the default webcam
    
    if not cap.isOpened():
        print("[!] ERROR: Could not open webcam.")
        return

    # Set resolution
    cap.set(cv2.CAP_PROP_FRAME_WIDTH, FRAME_WIDTH)
    cap.set(cv2.CAP_PROP_FRAME_HEIGHT, FRAME_HEIGHT)

    fourcc = cv2.VideoWriter_fourcc(*'XVID')
    
    print(f"[*] SENTINEL ACTIVE: Recording 24/7 to {SAVE_DIR}")

    while True:
        # Generate new filename based on timestamp
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        filename = os.path.join(SAVE_DIR, f"SENTINEL_{timestamp}.avi")
        
        out = cv2.VideoWriter(filename, fourcc, FPS, (FRAME_WIDTH, FRAME_HEIGHT))
        start_time = time.time()
        
        print(f"[>] RECORDING: {filename}")

        try:
            while (time.time() - start_time) < FILE_ROTATION_SECONDS:
                ret, frame = cap.read()
                if not ret:
                    print("[!] ERROR: Frame capture failed.")
                    break
                
                # Write the frame
                out.write(frame)
                
                # Check for interruption (optional)
                if cv2.waitKey(1) & 0xFF == ord('q'):
                    break
        except Exception as e:
            print(f"[!] ERROR during recording: {e}")
        finally:
            out.release()
            print(f"[#] SEGMENT SAVED: {filename}")
        
        # Small delay to prevent loop thrashing if errors occur
        time.sleep(1)

    cap.release()
    cv2.destroyAllWindows()

if __name__ == "__main__":
    start_recording()
