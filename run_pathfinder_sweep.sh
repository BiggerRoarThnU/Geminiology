#!/usr/bin/env bash
# ==============================================================================
# SovereignNexus LLC - Pre-Flight Pathfinder Verification & WAL Setup
# Axiom: 1=1=1 | Target: ~/SovereignNexus/nexus_ledger.db
# SAM.gov UEI: K5DALREZFGH6 | CAGE: 1AQG5
# ==============================================================================

set -e

SOVEREIGN_DIR="${HOME}/SovereignNexus"
DB_PATH="${SOVEREIGN_DIR}/nexus_ledger.db"

echo "========================================================================"
echo " [1=1=1] SOVEREIGNNEXUS PATHFINDER PRE-FLIGHT VERIFICATION"
echo "========================================================================"

# 1. Ensure SovereignNexus workspace directory exists
mkdir -p "${SOVEREIGN_DIR}"
echo "[✓] Workspace directory verified: ${SOVEREIGN_DIR}"

# 2. Initialize SQLite database schemas & Write-Ahead Logging (WAL)
python3 - << 'EOF'
import sqlite3, os

db_path = os.path.expanduser("~/SovereignNexus/nexus_ledger.db")
conn = sqlite3.connect(db_path)
c = conn.cursor()

# Ensure WAL mode
c.execute("PRAGMA journal_mode = WAL;")

# Initialize folder_manifest schema (Pathfinder Sweep Engine)
c.execute("""
    CREATE TABLE IF NOT EXISTS folder_manifest (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        timestamp TEXT NOT NULL,
        path TEXT UNIQUE NOT NULL,
        item_type TEXT NOT NULL,
        depth INTEGER NOT NULL DEFAULT 1,
        size_bytes INTEGER NOT NULL DEFAULT 0,
        status TEXT NOT NULL,
        parent_dir TEXT NOT NULL,
        sha256_hash TEXT DEFAULT 'PENDING'
    );
""")
c.execute("CREATE INDEX IF NOT EXISTS idx_manifest_status ON folder_manifest(status);")
c.execute("CREATE INDEX IF NOT EXISTS idx_manifest_path ON folder_manifest(path);")

# Initialize memory_vault schema (Lens 09 Shannon Entropy Filter)
c.execute("""
    CREATE TABLE IF NOT EXISTS memory_vault (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        timestamp TEXT NOT NULL,
        state_id TEXT UNIQUE NOT NULL,
        score REAL NOT NULL,
        entropy REAL NOT NULL,
        classification TEXT NOT NULL,
        payload_preview TEXT,
        payload_hash TEXT NOT NULL
    );
""")

conn.commit()
print(f"[✓] nexus_ledger.db verified at {db_path} | WAL Mode Active.")
conn.close()
EOF

echo "========================================================================"
echo " [✓] PRE-FLIGHT VERIFICATION COMPLETE. READY FOR PATHFINDER SWEEP."
echo "========================================================================"

if [ "$1" == "--execute" ] || [ "$1" == "--sweep" ]; then
    echo ""
    echo "[*] Launching AGY Depth-1 Pathfinder Sweep..."
    python3 "${SOVEREIGN_DIR}/nexus_depth1_pathfinder_assimilator.py"
fi
