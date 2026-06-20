#!/bin/bash

# ==============================================================================
# Antigravity Environment Update & Initialization Script
# Focus: Educational Research, Simulations, AI Integration, and R Data Analysis
# ==============================================================================

echo "🚀 Initiating Antigravity System Update..."
echo "Updating core OS packages..."
sudo apt-get update -y && sudo apt-get upgrade -y

# 1. Install System Dependencies for R and Python
echo "📦 Installing core dependencies, Python 3, and R base..."
sudo apt-get install -y software-properties-common dirmngr build-essential
sudo apt-get install -y python3 python3-pip python3-venv python3-dev
sudo apt-get install -y r-base r-base-dev

# 2. Set up the Antigravity Virtual Environment
ENV_NAME="antigravity_env"
echo "🌌 Initializing isolated Python environment: $ENV_NAME..."
python3 -m venv $ENV_NAME

# Activate the environment
source $ENV_NAME/bin/activate

# 3. Upgrade pip and install core tools
echo "⬆️ Upgrading pip and build tools..."
pip install --upgrade pip wheel setuptools

# 4. Install Google AI SDKs (For NotebookLM-like intelligence)
echo "🧠 Installing Google Generative AI SDKs..."
pip install google-genai

# 5. Install Simulation & Data Science Libraries
# numpy/scipy: Core math and physics simulations
# pandas: Data manipulation
# simpy: Discrete-event simulation for process tracking
echo "🧪 Installing Simulation and Data Science tools..."
pip install numpy scipy pandas simpy matplotlib jupyterlab

# 6. Install R-to-Python Integration
# rpy2 allows Python to execute R code natively within your scripts
echo "📊 Installing R integration (rpy2)..."
pip install rpy2

# 7. Environment Variables Setup (Placeholder for API keys)
# Creates a .env file to securely store your keys
if [ ! -f .env ]; then
    echo "🔑 Creating .env file for secure credential storage..."
    echo "GEMINI_API_KEY=\"your_api_key_here\"" > .env
    echo "GOOGLE_APPLICATION_CREDENTIALS=\"/path/to/your/service-account-file.json\"" >> .env
    echo "Please update the .env file with your actual API keys."
fi
pip install python-dotenv

echo "=============================================================================="
echo "✅ Antigravity System leveled up successfully!"
echo "To activate your environment, run: source $ENV_NAME/bin/activate"
echo "To start your research notebook, run: jupyter lab"
echo "=============================================================================="