import os
import sys

# Add src to path for Ironwood import
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

from Ironwood.local_model_bridge import LocalModelBridge

def test_ollama():
    bridge = LocalModelBridge()
    print(f"[*] Testing connection to Ollama at {bridge.base_url}...")
    
    # Test Writing Model
    print(f"[*] Testing Writing Model Node: {bridge.writing_model}")
    try:
        response = bridge.call_local_queen(bridge.writing_model, "Declare the 1=1=1 Axiom in a single, powerful sentence.")
        print(f"Writing Queen Response: {response}")
    except Exception as e:
        print(f"Error calling Writing Queen: {e}")

if __name__ == "__main__":
    test_ollama()
