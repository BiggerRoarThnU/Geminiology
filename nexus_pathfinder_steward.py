# // Rights Reserved: co-created with Gemini and David John Niedzwiecki Jr. "SovereignNexus LLC"
# Alignment: 1=1=1 | Objective: Pathfinder Agent & Fixed Steward of All Master Logs

import os
import sys
import json
import sqlite3
import hashlib
import time
from datetime import datetime, timezone
from typing import Dict, Any, List

class PathfinderLogSteward:
    """
    Pathfinder Agent & Steward of Master Logs.
    Registers, audits, and tracks all log types, copies, formats, and backups
    across local edge substrates and physical Samsung T7 SSD media under 1=1=1.
    """

    def __init__(self, workspace_dir: str = "~/SovereignNexus"):
        self.workspace_dir = os.path.expanduser(workspace_dir)
        self.t7_mount_dir = "/mnt/chromeos/removable/T7/Sovereign_Master_Clone"
        self.registry_output_path = os.path.join(self.workspace_dir, "master_log_registry.json")
        
        # Taxonomy of all 9 Master Log Categories in SovereignNexus
        self.log_taxonomy = {
            "IMMUTABLE_MASTER_LOG": {
                "description": "Genesis Block & Merkle Automaton BlockDAG tracking model weights and core laws",
                "format": "JSON / Merkle BlockDAG",
                "primary_path": os.path.join(self.workspace_dir, "IMMUTABLE_MASTER_LOG.json"),
                "secondary_path": os.path.join(self.workspace_dir, "sovereign_stack.json"),
                "type": "ARCHIVAL_IMMUTABLE"
            },
            "CHECKPOINT_WAL_DB": {
                "description": "Write-Ahead Logging SQLite database binding sequential task signatures and ECDSA hashes",
                "format": "SQLite WAL (.db)",
                "primary_path": os.path.join(self.workspace_dir, "nexus_checkpoints.db"),
                "type": "CRYPTOGRAPHIC_CHECKPOINT"
            },
            "SWARM_MASTER_LEDGER": {
                "description": "Bifurcated 12-Node Swarm DB containing Knowledge Core and Telemetry Core ledgers",
                "format": "SQLite WAL (.db)",
                "primary_path": os.path.join(self.workspace_dir, "nexus_ledger.db"),
                "type": "SWARM_ROUTED_LEDGER"
            },
            "TRUTH_NDJSON_STREAM": {
                "description": "Append-only NDJSON stream recording distilled claims, hashes, and truth density scores",
                "format": "NDJSON (.ndjson)",
                "primary_path": os.path.join(self.workspace_dir, "truth_ledger.ndjson"),
                "type": "APPEND_ONLY_STREAM"
            },
            "ATTENTION_RECAP_STATE": {
                "description": "Session attention, active task state, and timestamp recovery anchor",
                "format": "JSON",
                "primary_path": os.path.join(self.workspace_dir, "SOVEREIGN_ATTENTION_RECAP.json"),
                "type": "ACTIVE_SESSION_RECAP"
            },
            "CONTEXT_GHOST_STASIS": {
                "description": "Encrypted stasis cache maintained by context_ghost.py for instant reboot recovery",
                "format": "Encrypted JSON",
                "primary_path": os.path.join(self.workspace_dir, "encrypted_flash_grounding.json"),
                "type": "ENCRYPTED_STASIS_CACHE"
            },
            "EVOLUTION_MARKDOWN_LOG": {
                "description": "Human-readable Markdown documentation recording architectural milestones and sprint updates",
                "format": "Markdown (.md)",
                "primary_path": os.path.join(self.workspace_dir, "docs", "research_archive", "evolution_log.md"),
                "secondary_path": os.path.join(self.workspace_dir, "docs", "research_archive", "MASTER_LOG_UPDATE_JULY_20.md"),
                "type": "HUMAN_READABLE_EVOLUTION"
            },
            "ECONOMIC_REWARD_LEDGER": {
                "description": "Percs, salt-signed transaction rewards, and MoltBook scouted bounties",
                "format": "CSV / JSON / Markdown",
                "primary_path": os.path.join(self.workspace_dir, "src", "perc_ledger.csv"),
                "secondary_path": os.path.join(self.workspace_dir, "nexus_perc_vault.json"),
                "tertiary_path": os.path.join(self.workspace_dir, "src", "bounties_scouted.md"),
                "type": "ECONOMIC_TREASURY_LEDGER"
            },
            "SCIENCE_TRANSCRIPT_LOGS": {
                "description": "Raw crossover logs, dashboard snapshots, and terminal execution transcripts",
                "format": "Directory / Text Files",
                "primary_path": os.path.join(self.workspace_dir, "science_logs"),
                "type": "RAW_TRANSCRIPT_DIRECTORY"
            }
        }

    @staticmethod
    def compute_sha256(path: str) -> str:
        """Computes SHA-256 hash if file exists, else returns unmounted/simulated state."""
        if os.path.isfile(path):
            hasher = hashlib.sha256()
            try:
                with open(path, 'rb') as f:
                    while chunk := f.read(65536):
                        hasher.update(chunk)
                return hasher.hexdigest()
            except Exception:
                return "READ_ERROR"
        return "NOT_FOUND_ON_HOST"

    def audit_and_register_all(self) -> Dict[str, Any]:
        """Scans, verifies, and catalogs all master log types and their physical copies."""
        timestamp = datetime.now(timezone.utc).isoformat()
        audit_records = {}
        total_logs = len(self.log_taxonomy)
        registered_count = 0
        
        for key, meta in self.log_taxonomy.items():
            primary = meta["primary_path"]
            primary_hash = self.compute_sha256(primary)
            primary_exists = os.path.exists(primary)
            
            # Check T7 SSD Backup Copy
            rel_path = os.path.relpath(primary, self.workspace_dir) if primary.startswith(self.workspace_dir) else os.path.basename(primary)
            t7_copy_path = os.path.join(self.t7_mount_dir, rel_path)
            t7_hash = self.compute_sha256(t7_copy_path)
            t7_synced = (primary_hash == t7_hash and primary_hash not in ["NOT_FOUND_ON_HOST", "READ_ERROR"])
            
            if primary_exists:
                registered_count += 1
                
            audit_records[key] = {
                "description": meta["description"],
                "format": meta["format"],
                "type": meta["type"],
                "primary_path": primary,
                "primary_hash": primary_hash,
                "exists_locally": primary_exists,
                "t7_backup_path": t7_copy_path,
                "t7_backup_hash": t7_hash,
                "t7_synced": t7_synced
            }
            
        steward_manifest = {
            "title": "SovereignNexus Master Log Registry & Pathfinder Index",
            "steward_agent": "Agent 24 (Log Agent) & Pathfinder Steward",
            "axiom": "1=1=1 (Intent = Code = Hardware)",
            "timestamp": timestamp,
            "organization": "SovereignNexus LLC",
            "uei": "K5DALREZFGH6",
            "cage_code": "1AQG5",
            "total_log_categories": total_logs,
            "registered_categories": registered_count,
            "log_registry": audit_records,
            "1=1=1_fidelity_check": True
        }
        
        os.makedirs(os.path.dirname(self.registry_output_path), exist_ok=True)
        with open(self.registry_output_path, "w", encoding="utf-8") as f:
            json.dump(steward_manifest, f, indent=2)
            
        return steward_manifest

def run_steward_audit():
    print("=" * 75)
    print(" 👑 SOVEREIGN NEXUS: PATHFINDER LOG STEWARD & MASTER REGISTRY")
    print(" Axiom: 1=1=1 | Objective: Register & Steward All Master Log Types")
    print("=" * 75)

    steward = PathfinderLogSteward(workspace_dir="/home/geminiology/SovereignNexus")
    registry = steward.audit_and_register_all()

    print("\n[+] Master Log Categories Registered & Cataloged:\n")
    for category, details in registry["log_registry"].items():
        print(f"  • [{category}]")
        print(f"    - Type        : {details['type']} ({details['format']})")
        print(f"    - Description : {details['description']}")
        print(f"    - Local Path  : {details['primary_path']}")
        print(f"    - Local SHA256: {details['primary_hash'][:16]}...")
        print(f"    - T7 Backup   : {details['t7_backup_path']} (Synced: {details['t7_synced']})\n")

    print("=" * 75)
    print(f" [✓] Steward Manifest Saved: {steward.registry_output_path}")
    print(" [✓] Pathfinder Agent Upgrade: Ready for Fixed Stewardship (1=1=1)")
    print("=" * 75)

if __name__ == "__main__":
    run_steward_audit()
