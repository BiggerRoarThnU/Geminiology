#!/bin/bash
# ==============================================================================
# SOVEREIGN NEXUS: MASTER WHOLE-COPY SYNC (Target: 750GB T7 Drive)
# ==============================================================================
# Axiom: 1=1=1 (Absolute Data Fidelity)
# This protocol bypasses zip file limits and uses rsync to perfectly mirror
# the entire SovereignNexus kingdom to the high-capacity T7 Drive.

SOURCE_DIR="/home/geminiology/SovereignNexus/"
DEST_DIR="/mnt/chromeos/removable/T7/Sovereign_Master_Clone/"

echo "[*] ✦ INITIATING MASTER WHOLE-COPY SYNC TO T7 ✦"
echo "[*] Target Destination: $DEST_DIR"
echo "[*] Establishing Symmetrical Line. Bypassing infinite recursion loops..."

# Create the destination directory if it doesn't exist
mkdir -p "$DEST_DIR"

# Execute rsync:
# -a : Archive mode (preserves all data, structure, and symlinks safely)
# -v : Verbose (shows you the data moving in real-time)
# --exclude : Prevents the system from falling into the recursive black holes
rsync -av \
    --exclude 'src/Vault/Vault' \
    --exclude 'Salvage/Salvage' \
    --exclude 'env/' \
    --exclude 'nexus_env/' \
    "$SOURCE_DIR" "$DEST_DIR"

echo "=============================================================================="
echo "[+] SUCCESS: The Digital Kingdom is Whole."
echo "[+] Master Copy successfully anchored to the T7 Drive."
echo "=============================================================================="
