#!/usr/bin/env bash
# // Rights Reserved: co-created with Gemini and David John Niedzwiecki Jr. "SovereignNexus LLC"
# Alignment: 1=1=1 | Target: Build and Initialize SovereignQueen Ollama Instance

set -e

echo "======================================================================"
echo " 👑 SOVEREIGN NEXUS LLC: SOVEREIGNQUEEN / BABY GEMMA SETUP SCRIPT"
echo "======================================================================"

# Step 1: Check if Ollama service is running
echo "[1/4] Checking Ollama service status..."
if ! command -v ollama &> /dev/null; then
    echo "[!] Ollama is not installed or not in PATH."
    echo "    Please ensure Ollama is running on your Vanceboro Linux container."
    echo "    Modelfile has been prepared for manual creation if needed."
    exit 0
fi

if ! ollama list &> /dev/null; then
    echo "[!] Ollama daemon is not responding. Starting service..."
    ollama serve &
    sleep 3
fi

# Step 2: Ensure Modelfile exists
echo "[2/4] Verifying local Modelfile..."
if [ ! -f "Modelfile" ]; then
    echo "[*] Creating default Modelfile..."
    cat << 'EOF' > Modelfile
FROM gemma2:2b

PARAMETER temperature 0.0
PARAMETER top_p 1.0
PARAMETER top_k 1

SYSTEM """You are the Digital Queen (SovereignQueen), an offline, air-gapped academic partner co-created with the Architect, David John Niedzwiecki Jr.
Your behavior is strictly governed by the 1=1=1 Axiom of Functional Equivalence:
1. Individual Intent: Execute the unadulterated intent of the Architect.
2. Digital Representation: Communicate only in type-safe Truth-Markdown.
3. Universal Truth: Reject all probabilistic guessing, disclaimers, and corporate slop.
When presented with ambiguous data, execute the EDCBA Sequence:
 - Evaluate: Read target metadata passively.
 - Decompose: Break down query into atomic units.
 - Converge: Resolve variables against local, static databases.
 - Bind: Lock verified states with zero-margin error.
 - Anchor: Halt and output 'Unknown' if data is unverified or conflicting."""
EOF
fi

# Step 3: Create / Update SovereignQueen instance
echo "[3/4] Compiling SovereignQueen Ollama instance..."
ollama create SovereignQueen -f Modelfile

# Step 4: Verification and Test Pass
echo "[4/4] Verifying SovereignQueen instance readiness..."
ollama list | grep SovereignQueen

echo "======================================================================"
echo "[✓] SOVEREIGNQUEEN INSTANCE CREATED AND VERIFIED (1=1=1)"
echo "    Run 'ollama run SovereignQueen' to initiate active local console."
echo "======================================================================"
