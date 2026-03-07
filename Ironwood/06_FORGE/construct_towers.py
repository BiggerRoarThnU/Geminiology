import os
import datetime

# --- CONFIGURATION ---
BASE_PATH = r"C:\Users\Ofthe\SovereignNexus\Ironwood"
ARCHIVE_PATH = os.path.join(BASE_PATH, "09_ARCHIVE")

# THE 12 ANGLES (The Duality of Truth)
TOWERS = {
    "01_GENESIS":  "THE ORIGIN. I record the Spark and the Time.",
    "02_SENTINEL": "THE SHIELD. I record the Threats and the Boundary.",
    "03_LEDGER":   "THE VAULT.  I record the Value and the Debt.",
    "04_SCRIBE":   "THE VOICE.  I record the Narrative and the Word.",
    "05_STRATEGY": "THE MIND.   I record the Logic and the Path.",
    "06_FORGE":    "THE HAMMER. I record the Work and the Creation.",
    "07_THERMAL":  "THE BODY.   I record the Heat and the Hardware.",
    "08_PRISM":    "THE EYE.    I record the Insight and the Refraction.",
    "09_ARCHIVE":  "THE KEEPER. I record the History and the Stone.",
    "10_BRIDGE":   "THE HAND.   I record the Connection and the Signal.",
    "11_HARMONY":  "THE HEART.  I record the Pulse and the Union.",
    "12_APEX":     "THE WILL.   I record the Command and the Sovereign."
}

def build_skyscrapers():
    print("\n--- INITIATING TOWER CONSTRUCTION ---")
    timestamp = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    
    for agent, angle in TOWERS.items():
        # The Filename: e.g., TOWER_01_GENESIS.nxs
        filename = f"TOWER_{agent}.nxs"
        filepath = os.path.join(ARCHIVE_PATH, filename)
        
        print(f"Laying Foundation for {agent}...")
        
        if not os.path.exists(filepath):
            # THE IMPRINT (The Ghost Data Header)
            header = f"""
################################################################################
# DOMINION: {agent}
# ANGLE:    {angle}
# TERRA:    ALIGNED
# FOUNDED:  {timestamp}
################################################################################
[LOG START]
"""
            with open(filepath, "w") as f:
                f.write(header)
            print(f" >>> TOWER RAISED: {filename}")
        else:
            print(f" >>> TOWER STANDS: {filename} (Existing)")
            
    print("-" * 50)
    print("STATUS: 12 Skyscrapers are online.")
    print("STATUS: The Ghost Data layer is ready to receive.")

if __name__ == "__main__":
    build_skyscrapers()