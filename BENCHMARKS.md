# SovereignNexus Substrate Benchmarks

## 1. Execution Latency
- **Routing Decision Pipeline:** 3.96–4.58 µs (Microsecond execution).
- **Holographic Projection:** < 10 ms.
- **Ledger Verification:** < 5 ms.

## 2. Gate Metrics
- **Spectral Coherence Threshold (Y):** 0.40 (Quarantine activated above this ceiling).
- **Shannon Entropy Threshold (Z):** 0.20 bits per character (Quarantine activated below this floor, dynamically lowered for <15 char axioms).
- **Hopfield Phase Alignment Floor:** 0.15 coherence.

## 3. Cryptographic State Fixity
All context states are anchored via an append-only SQLite Write-Ahead Logging (WAL) cryptographic hash chain. Each block seals the preceding digest, guaranteeing absolute sequential continuity without relying on generalized Merkle trees.
