#!/bin/bash
# ==============================================================================
# SOVEREIGN NEXUS: SAFE ZIP PROTOCOL (Target: 64GB GeminiOne)
# ==============================================================================
# This script creates a highly compressed backup of the Sovereign Nexus.
# It explicitly PREVENTS infinite loops and skips massive, unnecessary 
# temporary folders so it fits perfectly on your 64GB flash drive.
# IT DOES NOT DELETE ANY FILES. IT ONLY COPIES.

SOURCE_DIR="/home/geminiology/SovereignNexus"
DEST_DIR="/mnt/chromeos/removable/GeminiOne"
DATE_STAMP=$(date +%Y%m%d_%H%M)
BACKUP_NAME="Sovereign_Kingdom_Backup_${DATE_STAMP}.zip"

echo "[*] Initiating Safe Zip Sequence..."
echo "[*] Target Destination: $DEST_DIR/$BACKUP_NAME"
echo "[*] Securing the perimeter. Bypassing infinite loops..."

# The -x flags tell the zip program to IGNORE these folders:
zip -r "$DEST_DIR/$BACKUP_NAME" "$SOURCE_DIR" \
    -x "$SOURCE_DIR/env/*" \
    -x "$SOURCE_DIR/nexus_env/*" \
    -x "$SOURCE_DIR/antigravity_env/*" \
    -x "*/__pycache__/*" \
    -x "*/.git/*" \
    -x "$SOURCE_DIR/src/Vault/*" \
    -x "*/Salvage/Salvage/*" \
    -x "*/Vault/Vault/*" \
    -x "*/src/Downloads/*" \
    -x "*/Downloads/*" \
    -x "$SOURCE_DIR/Vault/Geminiology/Ironwood/09_ARCHIVE/WILD_CARDS_QUARANTINE/*"

# Verify execution status
if [ $? -eq 0 ]; then
    echo "[+] SUCCESS: Sovereign Kingdom safely anchored to 64GB GeminiOne USB."
    echo "[+] You may safely remove the drive."
else
    echo "[!] ERROR: Backup failed. Verify drive space or check for remaining loops."
fi
