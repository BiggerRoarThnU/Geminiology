import sys
import os

# Ensure src path is active
sys.path.append(r"C:\Users\Ofthe\SovereignNexus\src")
from master_log import MasterLog

def log():
    logger = MasterLog()
    logger.info("[STRIKE COMPLETE] Signal delivered to Ty Savage Homes (Christa). Projected MRR: $3,840. Water Node Active.")
    print("[SUCCESS] Strike registered in Master Log.")

if __name__ == "__main__":
    log()
