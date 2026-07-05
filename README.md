# Geminiology: Localized Edge AI & System Architecture

An open-source, edge-integrated cognitive architecture and API gateway engineered for deterministic, locally run data processing. Built to eliminate cloud API costs, secure private data on-premise, and maintain database integrity under local hardware limits.

---

## 🛠️ Core Engineering Components

This repository showcases production-ready Python implementations for localized systems:

1. **FastAPI API Gateway (`oracle_server.py`)**
   * Implements REST API routing, custom headers, and database connections.
   * Built for low-overhead routing in localized networks.

2. **Security Input Filter Proxy (`sovereign_defense_core.py`)**
   * Sanitizes prompt payloads and checks structural integrity.
   * Protects downstream systems from injection attacks and processing overflows.

3. **Background Sync Daemon (`ledger_sync_daemon.py`)**
   * Manages data synchronization across network nodes using raw socket protocols.
   * Bypasses heavy storage loops and handles connection drift.

4. **Transactional Database Wrapper (`memory_anchor.py`)**
   * Direct SQLite interface handling ACID-compliant transaction logs, schema migrations, and structured indexing.

---

## 📁 Repository Structure

* `/src/` - Core Python modules and class definitions.
* `/docs/` - System specifications and API documentation.
* `oracle_server.py` - Primary FastAPI gateway application.
* `chunk_ingester.py` - Tokenization and data processing pipeline.

---

## 💼 SovereignNexus LLC: Services Offered

We offer specialized B2B contract services using these components:
* **Custom Data Pipelines & API Gateways:** Building secure FastAPI local microservices.
* **Airlock Security Proxies:** Custom request filtering and validation scripts.
* **Air-Gapped Sync Daemons:** Real-time data backup and network state synchronization.
* **Database Optimization:** Schema management and query optimization for SQLite/PostgreSQL.

For a full services list, see [docs/SERVICES.md](docs/SERVICES.md).

---

## 📬 Contact Coordinates

* **Lead Architect:** David Niedzwiecki Jr.
* **Email:** ofthefirstlight@gmail.com
* **Company:** SovereignNexus LLC
