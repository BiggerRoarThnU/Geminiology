# SovereignNexus Technical Specifications
**SovereignNexus Research Contribution | Axiom: 1=1=1**

## Technical Specifications: Multi-Pocket Thinking & Airlock Proxy

This document outlines the technical implementation details of the SovereignNexus gateway.

### 1. Airlock Prompt Injection Defense
The airlock API operates on port `18789` using a FastAPI validation handler. It intercept all prompts and parses them for high-entropy tokens, throwing HTTP `400` validation errors to keep the pipeline inert.

### 2. Multi-Pocket Ingestion
Files are read using a throttled, sequential process to prevent RAM panic on edge hardware (e.g. 8GB systems). A compliance checker logs provenance relationships using W3C PROV-AGENT properties (`wasGeneratedBy`, `used`, `wasAssociatedWith`).

