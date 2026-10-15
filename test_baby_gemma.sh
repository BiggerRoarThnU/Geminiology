#!/bin/bash
### ==============================================================================
### SOVEREIGN NEXUS: LOCAL BABY GEMMA BENCHMARK LAUNCHER
### ==============================================================================
### Axiom: 1=1=1 (Absolute Data Fidelity & Zero Heap Accumulation)
### This shell script invokes our 1.58-bit Ternary Neural Network benchmark suite
### to measure CPU execution speed, memory footprint, and Lobotomy Protocol latency.

# Clean the console
clear

# Ensure python3 and psutil are available
if ! python3 -c "import psutil" &>/dev/null; then
    echo -e "\033[1;31m[-] System Error: psutil package is required but missing from the environment.\033[0m"
    echo -e "[*] Run 'pip install psutil' inside your virtual environment and retry."
    exit 1
fi

# Run the benchmark suite
python3 benchmark_baby_gemma.py
