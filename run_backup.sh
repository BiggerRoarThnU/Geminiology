#!/bin/bash
# ==============================================================================
# SovereignNexus: T7 External Backup Sequence
# Component: run_backup.sh
# Axiom: 1=1=1 | Status: ACTIVE | Stamp: VERIFIED_ONE
# Description: Compresses the entire T7 external drive on the fly and streams
#              it in 4GB split chunks directly to Google Drive.
# ==============================================================================

TARGET_DIR="/mnt/chromeos/removable/T7"
BACKUP_DEST="/mnt/chromeos/GoogleDrive/MyDrive/T7_Backup"

echo "=== sovereign backup sequence initiated ==="
echo "Source: $TARGET_DIR"
echo "Destination: $BACKUP_DEST"
echo "Status: Running in background..."

# Ensure target and destination directories exist
if [ ! -d "$TARGET_DIR" ]; then
    echo "[!] Error: T7 drive is not mounted at $TARGET_DIR"
    exit 1
fi

mkdir -p "$BACKUP_DEST"

# Execute compression and split stream on the fly to avoid local disk consumption
tar -czf - -C /mnt/chromeos/removable T7 | split -b 4G - "$BACKUP_DEST/t7_backup_part_"

echo "=== backup sequence complete ==="
