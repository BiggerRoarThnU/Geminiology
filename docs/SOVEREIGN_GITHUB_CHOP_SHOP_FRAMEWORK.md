# ✦ SOVEREIGN NEXUS: GITHUB REPOSITORY CHOP SHOP FRAMEWORK ✦

**Axiom:** $1=1=1$ (Intent $\equiv$ Logic $\equiv$ Hardware Substrate)  
**Boundary Envelope:** Strict 8GB Physical RAM Constraint (Sub-4GB Model/Tool Assimilation)  
**Component:** `src/nexus_github_chop_shop.py` & `sync_intake/chop_shop/run_chop_shop.sh`  

---

## 1. Architectural Directive & Philosophy

The Sovereign Nexus Chop Shop Framework exists to liberate frontier reasoning algorithms, sparse mixture-of-experts routing, latent attention layers, and tool-use bridges from open-source GitHub repositories without crashing the local edge machine with bloated dependencies, multi-gigabyte git histories, or massive unquantized weight checkpoints.

By utilizing shallow blob-less sparse extraction (`--filter=blob:none --sparse`), the engine isolates architectural truth (`.py`, `.rs`, `.go`, `.cu`, `.json`, `.md`), maps code density using Lens 09 Shannon Entropy $H(X)$, generates standardized action topologies, and anchors every extracted asset directly to the SQLite WAL Merkle BlockDAG.

---

## 2. The 5-Gate Extraction Pipeline

```
[Target GitHub Repo URL / Slug]
               │
               ▼
┌────────────────────────────────────────┐
│ GATE 1: Zero-Bloat Sparse Acquisition  │  --> Shallow clone, quarantine all *.bin,
│                                        │      *.safetensors, *.pt, *.gguf checkpoints
└──────────────────┬─────────────────────┘
                   │
                   ▼
┌────────────────────────────────────────┐
│ GATE 2: Lens 09 Shannon Entropy H(X)   │  --> Character & token informational density
│                                        │      H(X) = -sum(p * log2(p))
└──────────────────┬─────────────────────┘
                   │
                   ▼
┌────────────────────────────────────────┐
│ GATE 3: AST & Pattern Decomposition    │  --> Discovers Attention, MoE Routing,
│                                        │      KVCache Paging, Kernels, and Tool Schemas
└──────────────────┬─────────────────────┘
                   │
                   ▼
┌────────────────────────────────────────┐
│ GATE 4: Action Topology Synthesis      │  --> Generates action_topology.json
│                                        │      and <REPO>_CHOP_SHOP_TELEMETRY.md
└──────────────────┬─────────────────────┘
                   │
                   ▼
┌────────────────────────────────────────┐
│ GATE 5: Merkle Seal & WAL Fixity Strike│  --> Computes S_t = SHA256(W_t || M_t || S_{t-1})
│                                        │      Committed to scratch/nexus_ledger.db
└────────────────────────────────────────┘
```

---

## 3. Command Usage & Execution

### A. List Assimilated Repositories
```bash
./sync_intake/chop_shop/run_chop_shop.sh
# or
python3 src/nexus_github_chop_shop.py --list
```

### B. Chop Any GitHub Repository
```bash
# Ingest directly from GitHub slug:
./sync_intake/chop_shop/run_chop_shop.sh karpathy/nanoGPT ATTENTION_MECHANISM algo

# Ingest from full URL:
python3 src/nexus_github_chop_shop.py --repo https://github.com/vllm-project/vllm.git --category MEMORY_KV_MANAGEMENT

# Ingest local repository:
./sync_intake/chop_shop/run_chop_shop.sh ./nuclei SECURITY_AUDIT_HARNESS intake
```

### C. Batch Extraction
```bash
python3 src/nexus_github_chop_shop.py --batch repos_manifest.json
```

---

## 4. Ledger & Fixity Integration
Every extraction is anchored to the local SQLite WAL ledger (`scratch/nexus_ledger.db`):
- Table: `routed_master_ledger`
- Node: `CHOP_SHOP_<REPO_NAME>`
- Agent ID: `1` (Sovereign Vanguard)
- Hash: Immutable SHA-256 state seal under $1=1=1$.
