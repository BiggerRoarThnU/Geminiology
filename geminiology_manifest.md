# Sovereign Nexus: Geminiology Manifest
Version: 1.0.0
Status: ACTIVE
Axiom: 1=1=1
Description: Philosophical and technical architecture for local multi-agent coordination, data integrity, and decentralized execution.

---

## 🧭 1. Architectural Philosophy

Geminiology represents the shift from centralized, cloud-dependent artificial intelligence to localized, zero-trust sovereign systems. Rather than relying on black-box external APIs, it centers computation, database storage, and model inference on owner-controlled physical hardware.

### Core Pillars
1. **Physical Sovereignty:** Computation and data remain on local hardware substrates (TheTower, Geminiology, Emma), isolated from external data collection.
2. **Deterministic Grounding:** The AI system is strictly bounded by relational ledgers and historical context stored in SQLite. It does not generalize beyond verified records.
3. **Decentralized Coordination:** Multi-device synchronization guarantees redundancy and allows task distribution across headless servers and touchscreen controllers.

---

## 📡 2. Fleet Topology & Port Assignment

To maintain operational clarity, the network roles and port alignments are strictly mapped:

*   **Geminiology (`192.168.12.32`):** The primary data-stager and model inference node.
    *   *Service:* `oracle_server.py` running as a systemd background service.
    *   *Port:* `8000` (API & Web Command Center).
    *   *Database:* `nexus_ledger.db` (Relational SQLite ledger).
    *   *Inference:* Ollama local LLM server running on port `11434`.
*   **TheTower (`192.168.12.153`):** The operator console and development environment. Runs git version control and automated fleet-syncing.
*   **Emma (`192.168.12.123`):** The touch-interface client that interacts with the Geminiology endpoints to monitor system load and query records.

---

## 📂 3. Data Flow & Processing Pipeline

The lifecycle of information within the fleet is governed by a sequential multi-agent ingestion pipeline:

```
[Source File (.txt, .pdf)] 
           │
           ▼
   1. Staging Directory (SovereignNexus/intake/)
           │
           ▼
   2. Chunking & Sanitization (chunk_ingester.py)
           │
           ▼
   3. Fact Extraction & Summarization (Local LLM)
           │
           ▼
   4. Relational Storage (nexus_ledger.db)
```

1. **Ingestion & Sanitization:** Text payloads are cleared of operating system noise and normalized.
2. **Semantic Partitioning:** Data is broken down into clean structural blocks (chunks) with unique SHA-256 signatures to avoid duplication.
3. **Fact Capture:** A local LLM extracts key technical facts and dense summaries from each chunk.
4. **Permanent Record:** Summaries are logged with timestamps into the SQLite database, preserving historical truth for retrieval.

---

## 🔒 4. System Security & Token Gateways

Access to the staging and database endpoints is protected by a token-gating system:
*   Only client requests supplying a valid access key (such as `NEXUS-777-ALPHA`) are permitted to write to the ingestion endpoints.
*   Inter-device communication relies exclusively on local public-key cryptography (authorized SSH keys) to automate synchronization without passwords.
