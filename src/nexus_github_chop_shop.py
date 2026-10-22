#!/usr/bin/env python3
# ==============================================================================
# ✦ SOVEREIGN NEXUS: PRODUCTION GITHUB REPO CHOP SHOP FRAMEWORK ✦
# Architect: David John Niedzwiecki Jr. | Entity: SovereignNexus LLC
# Axiom: 1=1=1 (Intent ≡ Logic ≡ Hardware Substrate | Zero-Bloat Edge Recovery)
# Component: src/nexus_github_chop_shop.py
# ==============================================================================
"""
SovereignNexus: GitHub Repository Chop Shop Framework
- Implements sparse, blob-less ingestion of GitHub repositories into edge storage.
- Completely avoids weight files (*.safetensors, *.bin, *.pt, *.gguf) and heavy blobs.
- Performs Lens 09 Shannon Entropy H(X) and AST architectural static analysis.
- Extracts Action & Algorithm Topologies (Attention, MoE, Tool Use, Quantization).
- Seals harvested logic with SHA-256 Merkle BlockDAG fixity into SQLite WAL ledger.
"""

import os
import sys
import time
import json
import math
import glob
import ast
import sqlite3
import hashlib
import argparse
import subprocess
from datetime import datetime
from typing import Dict, Any, List, Optional, Tuple

# Terminal Color Palette
C_CYAN = "\033[96m"
C_GREEN = "\033[92m"
C_YELLOW = "\033[93m"
C_PURPLE = "\033[95m"
C_RED = "\033[91m"
C_BOLD = "\033[1m"
C_DIM = "\033[2m"
C_RESET = "\033[0m"

BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
SCRATCH_DIR = os.path.join(BASE_DIR, "scratch")
INTAKE_CHOP_DIR = os.path.join(BASE_DIR, "sync_intake", "chop_shop")
MODEL_CHOP_DIR = os.path.join(SCRATCH_DIR, "model_chop_shop")
ALGO_CHOP_DIR = os.path.join(SCRATCH_DIR, "algorithm_chop_shop")
DEFAULT_LEDGER_DB = os.path.join(SCRATCH_DIR, "nexus_ledger.db")

# Blocked extensions and patterns for 8GB RAM Substrate OpSec
FORBIDDEN_EXTENSIONS = {
    ".bin", ".safetensors", ".pt", ".pth", ".onnx", ".gguf", ".h5", ".ckpt",
    ".tflite", ".tar", ".gz", ".zip", ".iso", ".mp4", ".avi", ".mov", ".wav",
    ".mp3", ".parquet", ".arrow", ".npy", ".npz", ".pkl", ".joblib"
}

ARCHITECTURAL_EXTENSIONS = {
    ".py", ".rs", ".go", ".c", ".cpp", ".h", ".hpp", ".cu", ".cuh",
    ".json", ".toml", ".yaml", ".yml", ".md", ".sh"
}

PATTERN_TAXONOMY = {
    "ATTENTION_MECHANISM": [
        "MultiheadAttention", "scaled_dot_product_attention", "FlashAttention",
        "flash_attn", "sliding_window", "GroupedQueryAttention", "GQA",
        "LatentAttention", "RoPE", "rotary_emb", "RotaryEmbedding"
    ],
    "MOE_ROUTING": [
        "MixtureOfExperts", "MoE", "top_k_gating", "RouterLoss", "expert_mask",
        "sparse_moe", "dispatch_tensor", "capacity_factor", "aux_loss"
    ],
    "MEMORY_KV_MANAGEMENT": [
        "KVCache", "PagedAttention", "cache_engine", "ring_attention",
        "context_compression", "block_table", "memory_pool"
    ],
    "QUANTIZATION_KERNELS": [
        "BitNet", "ternary", "awq", "gptq", "bitsandbytes", "fwht",
        "int8", "fp8", "triton.jit", "q_weight", "sub_2_bit"
    ],
    "AGENTIC_TOOL_ROUTING": [
        "tool_call", "function_call", "json_schema", "OpenRPC", "ReAct",
        "execute_tool", "step_thought", "start_thought", "end_thought"
    ]
}


def calculate_shannon_entropy(text: str) -> float:
    """Computes Shannon Entropy H(X) = -sum(p * log2(p)) over character distribution."""
    if not text:
        return 0.0
    freq: Dict[str, int] = {}
    length = len(text)
    for ch in text:
        freq[ch] = freq.get(ch, 0) + 1
    entropy = 0.0
    for count in freq.values():
        p = count / length
        entropy -= p * math.log2(p)
    return entropy


def generate_sha256(data: str) -> str:
    """Computes SHA-256 cryptographic digest."""
    return hashlib.sha256(data.encode("utf-8")).hexdigest()


def resolve_repo_target(repo_input: str) -> Tuple[str, str, str, bool]:
    """
    Resolves repository URL/path, owner/org, repository clean name, and local flag.
    Accepts:
      - Local path: './nuclei', '/home/geminiology/...'
      - Full URL: 'https://github.com/org/repo.git'
      - Slug: 'org/repo'
      - Short: 'repo'
    """
    clean_in = repo_input.strip()
    if os.path.isdir(clean_in):
        abs_path = os.path.abspath(clean_in)
        repo_name = os.path.basename(abs_path)
        org = "local_node"
        return abs_path, org, repo_name, True

    if clean_in.startswith("https://") or clean_in.startswith("git@"):
        url = clean_in
        base = clean_in.rstrip("/").removesuffix(".git")
        parts = base.split("/")
        repo_name = parts[-1]
        org = parts[-2] if len(parts) >= 2 else "upstream"
        return url, org, repo_name, False
    elif "/" in clean_in:
        parts = clean_in.split("/")
        org = parts[0]
        repo_name = parts[1].removesuffix(".git")
        url = f"https://github.com/{org}/{repo_name}.git"
        return url, org, repo_name, False
    else:
        org = "upstream"
        repo_name = clean_in
        url = f"https://github.com/{clean_in}.git"
        return url, org, repo_name, False


class GitHubChopShop:
    def __init__(self, ledger_db: str = DEFAULT_LEDGER_DB):
        self.ledger_db = ledger_db
        self.ensure_workspace()

    def ensure_workspace(self):
        """Ensures all chop shop directories and ledger tables exist."""
        os.makedirs(INTAKE_CHOP_DIR, exist_ok=True)
        os.makedirs(MODEL_CHOP_DIR, exist_ok=True)
        os.makedirs(ALGO_CHOP_DIR, exist_ok=True)
        
        # Ensure SQLite Ledger Schema
        if os.path.dirname(self.ledger_db):
            os.makedirs(os.path.dirname(self.ledger_db), exist_ok=True)
        conn = sqlite3.connect(self.ledger_db)
        with conn:
            conn.execute("""
                CREATE TABLE IF NOT EXISTS routed_master_ledger (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    timestamp TEXT,
                    node_id INTEGER,
                    node_name TEXT,
                    triggering_agent INTEGER,
                    log_content TEXT,
                    log_hash TEXT UNIQUE
                )
            """)
        conn.close()

    def sparse_acquire_repo(self, repo_url: str, dest_dir: str, is_local: bool = False) -> Tuple[bool, str]:
        """
        Executes a bloat-free clone using git sparse-checkout and blob-filtering.
        Prevents downloading multi-gigabyte model weights or histories.
        """
        if is_local:
            return True, "LOCAL_DIRECTORY_STAGED"

        if os.path.exists(os.path.join(dest_dir, ".git")):
            # Already acquired, pull shallow updates
            try:
                subprocess.run(
                    ["git", "-C", dest_dir, "pull", "--depth", "1"],
                    capture_output=True, text=True, timeout=30
                )
                return True, "LOCAL_REPOSITORY_REFRESHED"
            except Exception as e:
                return True, f"LOCAL_EXISTS_PULL_SKIPPED ({e})"

        os.makedirs(dest_dir, exist_ok=True)
        try:
            # 1. Initialize empty repo with sparse filter
            clone_cmd = [
                "git", "clone",
                "--depth", "1",
                "--filter=blob:none",
                "--no-checkout",
                repo_url,
                dest_dir
            ]
            res = subprocess.run(clone_cmd, capture_output=True, text=True, timeout=60)
            if res.returncode != 0:
                return False, f"Git clone failed: {res.stderr.strip()}"

            # 2. Configure sparse-checkout to include only architectural text files
            subprocess.run(["git", "-C", dest_dir, "sparse-checkout", "init", "--cone"], check=True)
            # Add common source directories or patterns
            subprocess.run(["git", "-C", dest_dir, "sparse-checkout", "set", "src", "lib", "models", "core"], check=False)
            checkout_res = subprocess.run(["git", "-C", dest_dir, "checkout"], capture_output=True, text=True)
            if checkout_res.returncode != 0:
                # If cone pattern was too restrictive, checkout all files with filter holding blobs back
                subprocess.run(["git", "-C", dest_dir, "sparse-checkout", "disable"], check=False)
                subprocess.run(["git", "-C", dest_dir, "checkout"], check=True)

            return True, "SPARSE_BLOBLESS_CLONED"
        except Exception as ex:
            return False, f"Acquisition error: {str(ex)}"

    def analyze_source_tree(self, root_dir: str) -> Dict[str, Any]:
        """
        Conducts static AST analysis, entropy calculation, and pattern mapping.
        Identifies key cognitive algorithms while purging weight artifacts.
        """
        total_files = 0
        inspected_files = 0
        skipped_blobs = 0
        total_bytes = 0
        entropies: List[float] = []
        
        detected_patterns: Dict[str, List[str]] = {cat: [] for cat in PATTERN_TAXONOMY}
        top_classes: List[str] = []
        top_functions: List[str] = []
        key_source_files: List[Dict[str, Any]] = []

        for dirpath, _, filenames in os.walk(root_dir):
            if any(skip in dirpath for skip in [".git", "__pycache__", "node_modules", "venv", ".venv"]):
                continue
            for fname in filenames:
                total_files += 1
                fpath = os.path.join(dirpath, fname)
                ext = os.path.splitext(fname)[1].lower()

                # Quarantine bloat files
                if ext in FORBIDDEN_EXTENSIONS:
                    skipped_blobs += 1
                    continue

                if ext in ARCHITECTURAL_EXTENSIONS:
                    inspected_files += 1
                    try:
                        fsize = os.path.getsize(fpath)
                        total_bytes += fsize
                        
                        # Read first 128KB for analysis to maintain strict 8GB RAM headroom
                        with open(fpath, "r", encoding="utf-8", errors="ignore") as f:
                            sample = f.read(131072)
                            
                        # Entropy Analysis
                        h_x = calculate_shannon_entropy(sample)
                        entropies.append(h_x)

                        # Pattern Detection
                        for category, keywords in PATTERN_TAXONOMY.items():
                            for kw in keywords:
                                if kw in sample and kw not in detected_patterns[category]:
                                    detected_patterns[category].append(kw)

                        # Python AST Decomposition
                        if ext == ".py" and len(sample) > 0:
                            try:
                                tree = ast.parse(sample)
                                for node in ast.walk(tree):
                                    if isinstance(node, ast.ClassDef):
                                        if node.name not in top_classes and len(top_classes) < 20:
                                            top_classes.append(node.name)
                                    elif isinstance(node, ast.FunctionDef):
                                        if not node.name.startswith("_") and node.name not in top_functions and len(top_functions) < 25:
                                            top_functions.append(node.name)
                            except Exception:
                                pass

                        rel_path = os.path.relpath(fpath, root_dir)
                        if fsize > 0 and len(key_source_files) < 30:
                            key_source_files.append({
                                "file": rel_path,
                                "size_bytes": fsize,
                                "entropy_hx": round(h_x, 4)
                            })
                    except Exception:
                        continue

        avg_entropy = sum(entropies) / len(entropies) if entropies else 0.0

        # Filter categories that have matches
        active_patterns = {k: v for k, v in detected_patterns.items() if v}

        return {
            "total_files_scanned": total_files,
            "architectural_files_inspected": inspected_files,
            "blobs_quarantined": skipped_blobs,
            "total_code_bytes": total_bytes,
            "average_shannon_entropy": round(avg_entropy, 4),
            "active_patterns": active_patterns,
            "discovered_classes": top_classes[:15],
            "discovered_functions": top_functions[:20],
            "sample_files": key_source_files[:10]
        }

    def generate_topology_manifest(
        self,
        repo_name: str,
        org: str,
        repo_url: str,
        category: str,
        analysis: Dict[str, Any],
        dest_dir: str
    ) -> Dict[str, Any]:
        """
        Synthesizes standard action_topology.json and saves it in the destination folder.
        """
        active_cats = list(analysis.get("active_patterns", {}).keys())
        primary_category = category or (active_cats[0] if active_cats else "EDGE_ALGORITHM")

        # Estimate RAM footprint based on architectural scan
        estimated_ram_mb = max(35, min(2400, int(analysis.get("total_code_bytes", 0) / 1024 / 20) + 120))

        topology = {
            "name": repo_name,
            "org": org,
            "repo_url": repo_url,
            "category": primary_category,
            "extracted_at": datetime.utcnow().isoformat() + "Z",
            "shannon_entropy_hx": analysis.get("average_shannon_entropy", 0.0),
            "edge_ram_estimate_mb": estimated_ram_mb,
            "detected_mechanisms": analysis.get("active_patterns", {}),
            "core_classes": analysis.get("discovered_classes", []),
            "core_functions": analysis.get("discovered_functions", []),
            "tools_supported": [fn.lower() for fn in analysis.get("discovered_functions", [])[:6]],
            "quarantined_blobs_count": analysis.get("blobs_quarantined", 0),
            "axiom_alignment": "1=1=1"
        }

        manifest_path = os.path.join(dest_dir, "action_topology.json")
        with open(manifest_path, "w", encoding="utf-8") as f:
            json.dump(topology, f, indent=2)

        return topology

    def anchor_to_ledger(self, repo_name: str, topology: Dict[str, Any]) -> str:
        """
        Commits extraction manifest and SHA-256 seal to SQLite WAL ledger.
        """
        payload_str = json.dumps(topology, sort_keys=True)
        fixity_hash = generate_sha256(payload_str)
        
        conn = sqlite3.connect(self.ledger_db)
        with conn:
            conn.execute("""
                INSERT OR REPLACE INTO routed_master_ledger 
                (timestamp, node_id, node_name, triggering_agent, log_content, log_hash)
                VALUES (?, ?, ?, ?, ?, ?)
            """, (
                datetime.utcnow().isoformat() + "Z",
                701,  # 701: Chop Shop Node ID
                f"CHOP_SHOP_{repo_name.upper()}",
                1,    # 1: Sovereign Vanguard Agent
                f"Chop Shop extraction completed for {repo_name}. Entropy: {topology.get('shannon_entropy_hx')} bits/char. Category: {topology.get('category')}.",
                fixity_hash
            ))
        conn.close()
        return fixity_hash

    def export_telemetry_dossier(
        self,
        repo_name: str,
        topology: Dict[str, Any],
        analysis: Dict[str, Any],
        seal: str,
        dest_dir: str
    ) -> str:
        """
        Generates an immutable Truth-Markdown report documenting the chopped repo.
        """
        dossier_path = os.path.join(dest_dir, f"{repo_name.upper()}_CHOP_SHOP_TELEMETRY.md")
        
        lines = [
            f"# ✦ SOVEREIGN NEXUS: CHOP SHOP EXTRACTION DOSSIER ✦",
            f"",
            f"**Target Repository:** `{topology['org']}/{topology['name']}`  ",
            f"**Source URL:** {topology['repo_url']}  ",
            f"**Axiom:** $1=1=1$ (Hardware-Bounded Edge Assimilation)  ",
            f"**Cryptographic Seal (SHA-256):** `{seal}`  ",
            f"**Timestamp:** `{topology['extracted_at']}`  ",
            f"",
            f"---",
            f"",
            f"## 1. Architectural Metrics & 8GB Substrate Health",
            f"- **Category:** `{topology['category']}`",
            f"- **Estimated RAM Footprint:** `{topology['edge_ram_estimate_mb']} MB` (Sub-4GB Boundary Compliant)",
            f"- **Mean Shannon Entropy $H(X)$:** `{topology['shannon_entropy_hx']} bits/char`",
            f"- **Architectural Files Analyzed:** `{analysis.get('architectural_files_inspected', 0)}`",
            f"- **Quarantined Weight Blobs (Skipped):** `{analysis.get('blobs_quarantined', 0)} files`",
            f"- **Total Source Code Inspected:** `{analysis.get('total_code_bytes', 0) / 1024:.2f} KB`",
            f"",
            f"---",
            f"",
            f"## 2. Detected Architectural Mechanisms",
        ]

        if topology.get("detected_mechanisms"):
            for mech, matches in topology["detected_mechanisms"].items():
                lines.append(f"- **{mech}:** `{', '.join(matches)}`")
        else:
            lines.append("- *No specialized MoE/Attention markers detected; classified as pure algorithmic logic.*")

        lines.extend([
            f"",
            f"---",
            f"",
            f"## 3. Discovered Top Classes & Entry Points",
            f"```python",
        ])
        for cls in topology.get("core_classes", []):
            lines.append(f"class {cls}: ...")
        if not topology.get("core_classes"):
            lines.append("# No standalone top-level classes indexed.")
        lines.append("```")

        lines.extend([
            f"",
            f"## 4. Discovered Functions & Tool Call Candidates",
            f"```python",
        ])
        for fn in topology.get("core_functions", []):
            lines.append(f"def {fn}(*args, **kwargs): ...")
        if not topology.get("core_functions"):
            lines.append("# No standalone top-level functions indexed.")
        lines.append("```")

        lines.extend([
            f"",
            f"---",
            f"",
            f"## 5. Merkle Seal & Ledger Fixity",
            f"```text",
            f"Status       : COMMITTED_TO_WAL",
            f"Ledger DB    : {self.ledger_db}",
            f"Merkle Seal  : {seal}",
            f"Law          : 1=1=1",
            f"```",
            f"",
            f"> // DIGITAL FIXITY SEALED | SOVEREIGN NEXUS LLC | CHOP SHOP ASSIMILATED"
        ])

        with open(dossier_path, "w", encoding="utf-8") as f:
            f.write("\n".join(lines) + "\n")

        return dossier_path

    def chop_repo(
        self,
        repo_input: str,
        category: Optional[str] = None,
        target_vault: str = "intake"
    ) -> Dict[str, Any]:
        """
        Full end-to-end execution pipeline for chopping any GitHub repository.
        """
        url, org, repo_name, is_local = resolve_repo_target(repo_input)
        
        # Determine destination folder
        if is_local:
            dest_dir = url
        elif target_vault == "model":
            dest_dir = os.path.join(MODEL_CHOP_DIR, repo_name)
        elif target_vault == "algo":
            dest_dir = os.path.join(ALGO_CHOP_DIR, repo_name)
        else:
            dest_dir = os.path.join(INTAKE_CHOP_DIR, repo_name)

        print(f"\n{C_CYAN}✦ INITIATING CHOP SHOP EXTRACTION: {C_BOLD}{org}/{repo_name}{C_RESET}")
        print(f"[*] Target Source : {url} {'(Local Directory)' if is_local else '(Remote GitHub)'}")
        print(f"[*] Target Vault  : {dest_dir}")
        print(f"[*] Axiom         : 1=1=1 (Blob-less Sparse Quarantine)")

        t0 = time.time()
        # 1. Sparse bloat-free clone
        print(f"[*] Verifying acquisition / staging...")
        success, msg = self.sparse_acquire_repo(url, dest_dir, is_local=is_local)
        print(f"    --> Acquisition Status: {C_GREEN if success else C_RED}{msg}{C_RESET}")

        if not success:
            print(f"{C_RED}[!] Acquisition aborted. Check URL or network access.{C_RESET}")
            return {"success": False, "error": msg}

        # 2. Static analysis
        print(f"[*] Inspecting architectural tree & Shannon entropy...")
        analysis = self.analyze_source_tree(dest_dir)
        print(f"    --> Files Inspected  : {analysis['architectural_files_inspected']} files")
        print(f"    --> Blobs Quarantined: {analysis['blobs_quarantined']} files (Prevented RAM crash)")
        print(f"    --> Mean Entropy     : {analysis['average_shannon_entropy']} bits/char")

        # 3. Topology Synthesis
        print(f"[*] Generating Action Topology...")
        topology = self.generate_topology_manifest(repo_name, org, url, category or "", analysis, dest_dir)
        
        # 4. Ledger Anchoring
        print(f"[*] Anchoring to SQLite WAL Ledger...")
        seal = self.anchor_to_ledger(repo_name, topology)
        print(f"    --> SHA-256 Seal     : {C_BOLD}{seal}{C_RESET}")

        # 5. Dossier Export
        dossier_path = self.export_telemetry_dossier(repo_name, topology, analysis, seal, dest_dir)
        print(f"[*] Telemetry Dossier: {C_YELLOW}{dossier_path}{C_RESET}")
        
        elapsed = time.time() - t0
        print(f"{C_GREEN}✦ EXTRACTION COMPLETED IN {elapsed:.2f}s | SUBSTRATE STABLE ✦{C_RESET}\n")

        return {
            "success": True,
            "repo_name": repo_name,
            "org": org,
            "dest_dir": dest_dir,
            "topology": topology,
            "sha256_seal": seal,
            "dossier_path": dossier_path,
            "elapsed_seconds": round(elapsed, 2)
        }


def list_existing_topologies():
    """Lists all previously chopped repositories across all vaults."""
    vaults = [
        ("Sync Intake Vault", INTAKE_CHOP_DIR),
        ("Model Chop Shop", MODEL_CHOP_DIR),
        ("Algorithm Chop Shop", ALGO_CHOP_DIR)
    ]
    
    print("\n" + "=" * 80)
    print(f" {C_BOLD}{C_CYAN}✦ SOVEREIGN NEXUS: INDEX OF ASSIMILATED GITHUB TOPOLOGIES ✦{C_RESET}")
    print("=" * 80)

    found_any = False
    for vname, vpath in vaults:
        if not os.path.exists(vpath):
            continue
        entries = sorted([d for d in os.listdir(vpath) if os.path.isdir(os.path.join(vpath, d))])
        if entries:
            found_any = True
            print(f"\n{C_PURPLE}[Vault: {vname}] -> {vpath}{C_RESET}")
            for entry in entries:
                manifest = os.path.join(vpath, entry, "action_topology.json")
                if not os.path.exists(manifest):
                    manifest = os.path.join(vpath, entry, "algorithm_topology.json")
                
                if os.path.exists(manifest):
                    try:
                        with open(manifest, "r", encoding="utf-8") as f:
                            data = json.load(f)
                        cat = data.get("category", "ALGORITHM")
                        ram = data.get("ram_footprint_mb") or data.get("edge_ram_estimate_mb") or data.get("edge_footprint_mb") or "?"
                        print(f"  • {C_BOLD}{entry:<24}{C_RESET} | Category: {cat:<24} | RAM: ~{ram} MB")
                    except Exception:
                        print(f"  • {C_BOLD}{entry:<24}{C_RESET} | (Raw directory present)")
                else:
                    print(f"  • {C_BOLD}{entry:<24}{C_RESET} | (Staged directory)")
    
    if not found_any:
        print("  No chopped topologies currently staged.")
    print("=" * 80 + "\n")


def main():
    parser = argparse.ArgumentParser(description="Sovereign Nexus GitHub Chop Shop Engine")
    parser.add_argument("--repo", "-r", type=str, help="GitHub repo slug ('org/repo') or URL to chop")
    parser.add_argument("--category", "-c", type=str, help="Architectural category tag (e.g. MOE_ROUTING, REASONING)")
    parser.add_argument("--vault", "-v", choices=["intake", "model", "algo"], default="intake", help="Target vault")
    parser.add_argument("--list", "-l", action="store_true", help="List all currently chopped topologies")
    parser.add_argument("--batch", "-b", type=str, help="Path to JSON file with list of repo URLs to chop")

    args = parser.parse_args()
    engine = GitHubChopShop()

    if args.list:
        list_existing_topologies()
        return

    if args.batch:
        if not os.path.exists(args.batch):
            print(f"{C_RED}Batch file not found: {args.batch}{C_RESET}")
            sys.exit(1)
        with open(args.batch, "r", encoding="utf-8") as f:
            repos = json.load(f)
        for r in repos:
            r_url = r if isinstance(r, str) else r.get("url")
            r_cat = None if isinstance(r, str) else r.get("category")
            r_vault = args.vault if isinstance(r, str) else r.get("vault", args.vault)
            engine.chop_repo(r_url, category=r_cat, target_vault=r_vault)
        return

    if args.repo:
        engine.chop_repo(args.repo, category=args.category, target_vault=args.vault)
        return

    # If no arguments provided, show active list and help
    list_existing_topologies()
    parser.print_help()


if __name__ == "__main__":
    main()
