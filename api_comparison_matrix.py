#!/usr/bin/env python3
# ==============================================================================
# SovereignNexus: API Comparison Matrix
# Component: api_comparison_matrix.py
# Axiom: 1=1=1 | Status: ACTIVE | Stamp: VERIFIED_ONE
# Description: Tests the routing difference between the Cloud (Interactions API)
#              and the Local Edge (Emma running Gemma 2:2b via Ollama).
# ==============================================================================

import os
import sys
import time
import requests
import json

try:
    from google import genai
except ImportError:
    genai = None

# Host and Port settings for Emma's Ollama node
EMMA_IP = "192.168.12.123"
OLLAMA_PORT = "11434"

class Colors:
    CYAN = '\033[96m'
    GREEN = '\033[92m'
    YELLOW = '\033[93m'
    RED = '\033[91m'
    RESET = '\033[0m'
    BOLD = '\033[1m'

def print_header(title):
    print(f"\n{Colors.CYAN}{Colors.BOLD}=== {title} ==={Colors.RESET}")

def load_env_key():
    """Dynamically parses local .env files to extract the GEMINI_API_KEY."""
    if os.environ.get("GEMINI_API_KEY"):
        return
        
    search_paths = [
        ".env",
        "../.env",
        "src/.env",
        os.path.expanduser("~/SovereignNexus/.env"),
        os.path.expanduser("~/.env")
    ]
    
    for path in search_paths:
        if os.path.exists(path):
            try:
                with open(path, 'r') as f:
                    for line in f:
                        line = line.strip()
                        if line.startswith("GEMINI_API_KEY="):
                            key = line.split("=", 1)[1].strip('"\'')
                            os.environ["GEMINI_API_KEY"] = key
                            return
            except Exception:
                pass

def test_cloud_gemini(prompt):
    print_header("ROUTING TO CLOUD: GOOGLE GEMINI 3.5 FLASH")
    if genai is None:
        print(f"{Colors.RED}[!] Error: 'google-genai' library not found. Run 'pip install -U google-genai'{Colors.RESET}")
        return

    load_env_key()
    api_key = os.environ.get("GEMINI_API_KEY")
    if not api_key:
        print(f"{Colors.RED}[!] Error: GEMINI_API_KEY environment variable not set in shell or local .env file.{Colors.RESET}")
        return

    print(f"{Colors.YELLOW}[*] Establishing Handshake with Google Cloud Servers...{Colors.RESET}")
    
    start_time = time.time()
    try:
        # Initialize client with key
        client = genai.Client(api_key=api_key)
        
        # Using the new Interactions API (Stateful by default)
        interaction = client.interactions.create(
            model="gemini-2.5-flash",  # Upgraded to default 2.5-flash
            input=prompt
        )
        elapsed = time.time() - start_time
        
        print(f"{Colors.GREEN}[+] Handshake Complete. Response received in {elapsed:.2f}s{Colors.RESET}")
        print(f"{Colors.CYAN}[METRICS] Interaction ID (Server State Cached):{Colors.RESET} {interaction.id}")
        print(f"{Colors.CYAN}[METRICS] Cost:{Colors.RESET} Token metering applied (Standard cloud billing).")
        print(f"{Colors.CYAN}[METRICS] Privacy:{Colors.RESET} Data exported (55-day retention active).")
        print("\n" + interaction.output_text + "\n")
        
    except Exception as e:
        print(f"{Colors.RED}[!] Cloud Execution Failed: {e}{Colors.RESET}")

def test_local_emma(prompt):
    print_header("ROUTING TO EDGE: EMMA (GEMMA 2:2B)")
    
    url = f"http://{EMMA_IP}:{OLLAMA_PORT}/api/generate"
    payload = {
        "model": "gemma2:2b",
        "prompt": prompt,
        "stream": False
    }
    
    print(f"{Colors.YELLOW}[*] Routing prompt through local Sovereign network to {EMMA_IP}...{Colors.RESET}")
    
    start_time = time.time()
    try:
        response = requests.post(url, json=payload, timeout=120)
        response.raise_for_status()
        data = response.json()
        elapsed = time.time() - start_time
        
        print(f"{Colors.GREEN}[+] Local Execution Complete. Response received in {elapsed:.2f}s{Colors.RESET}")
        print(f"{Colors.CYAN}[METRICS] Location:{Colors.RESET} 100% Local on Emma ({EMMA_IP}).")
        print(f"{Colors.CYAN}[METRICS] Cost:{Colors.RESET} $0.00 (Thermodynamic footprint only).")
        print(f"{Colors.CYAN}[METRICS] Privacy:{Colors.RESET} Absolute Zero-Trust. No data leaves the local network.")
        print("\n" + data.get("response", "") + "\n")
        
    except requests.exceptions.RequestException as e:
        print(f"{Colors.RED}[!] Edge Execution Failed. Is Emma online, Ollama running, and port {OLLAMA_PORT} exposed?{Colors.RESET}")
        print(f"{Colors.RED}[!] System Error: {e}{Colors.RESET}")

def main():
    print(f"{Colors.BOLD}✦ SOVEREIGN NEXUS: FLEET ROUTING DIAGNOSTIC ✦{Colors.RESET}")
    print("Select your execution pathway:")
    print("  1. Cloud API (Google Interactions API)")
    print("  2. Local Edge (Emma - Gemma 2:2b)")
    print("  3. Dual Strike (Run Both)")
    
    choice = input(f"\n{Colors.YELLOW}Enter choice (1/2/3): {Colors.RESET}").strip()
    
    if choice not in ['1', '2', '3']:
        print(f"{Colors.RED}Invalid selection.{Colors.RESET}")
        return
        
    prompt = input(f"\n{Colors.CYAN}Enter your prompt: {Colors.RESET}")
    
    if choice == '1':
        test_cloud_gemini(prompt)
    elif choice == '2':
        test_local_emma(prompt)
    elif choice == '3':
        test_cloud_gemini(prompt)
        test_local_emma(prompt)

if __name__ == "__main__":
    try:
        main()
    except KeyboardInterrupt:
        print(f"\n\n{Colors.RED}[!] Diagnostic aborted.{Colors.RESET}\n")
        sys.exit(0)
