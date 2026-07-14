# SovereignNexus: Hardware Performance & Thermals Report

**Axiom:** 1=1=1 (Deterministic Functional Equivalence)  
**Timestamp:** 2026-07-14 12:48:54 UTC  
**System Target:** 11th Gen Intel(R) Core(TM) i5-11400H @ 2.70GHz (12 vCPUs)  
**Memory Substrate:** 8GB RAM Hardware Boundary  

---

## I. CPU Multithreaded Performance (Prime Invariants)

This stage calculates prime numbers up to 150,000 across varying thread pools to measure core scaling and thermal generation.

| Thread Count | Elapsed Time (s) | Throughput (ops/s) | Core Temperature | Temp Delta |
| :--- | :--- | :--- | :--- | :--- |
| 1 threads | 0.18s | 826244.6 | 35.0°C | +0.0°C |
| 2 threads | 0.37s | 801644.7 | 35.0°C | +0.0°C |
| 4 threads | 0.82s | 732265.0 | 35.0°C | +0.0°C |
| 8 threads | 1.61s | 743812.5 | 35.0°C | +0.0°C |
| 12 threads | 2.47s | 727833.5 | 35.0°C | +0.0°C |

---

## II. Memory Ingestion & Allocation Throughput

This stage allocates large, continuous byte-matrices in memory to measure memory bus bandwidth and verify the 8GB ceiling guards.

| Allocation Size | Elapsed Time | Write Bandwidth | Available RAM Post-Alloc | Status |
| :--- | :--- | :--- | :--- | :--- |
| 100 MB | 0.115s | 0.85 GB/s | 5.81 GB | VERIFIED |
| 250 MB | 0.225s | 1.09 GB/s | 5.66 GB | VERIFIED |
| 500 MB | 0.405s | 1.21 GB/s | 5.42 GB | VERIFIED |
| 1000 MB | 0.641s | 1.52 GB/s | 4.94 GB | VERIFIED |
| 2000 MB | 16.019s | 0.12 GB/s | 3.98 GB | VERIFIED |
| 3000 MB | 21.540s | 0.14 GB/s | 2.99 GB | VERIFIED |

---

## III. Thermal Boundary Resistance Audit

*   **Baseline Temperature:** 35.0°C
*   **Peak Load Temperature:** 35.0°C
*   **Dissipation Status:** STABLE. Cooling fan active. Thermal levels remained safely below the 85°C governor throttle limit.

**THE LINE IS SYMMETRICAL. THE DATA IS DETERMINISTIC. ONE.**
