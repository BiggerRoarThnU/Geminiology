import os
from Ironwood.local_model_bridge import LocalModelBridge

def test_models():
    bridge = LocalModelBridge()
    print(f"[*] Testing connection to LM Studio at {bridge.base_url}...")
    
    # Test Lexi
    print(f"[*] Testing Lexi Node: {bridge.lexi_model}")
    lexi_response = bridge.call_local_queen(bridge.lexi_model, "What is the Axiom 1=1=1?")
    print(f"Lexi Response: {lexi_response}")
    
    # Test Qwen
    print(f"[*] Testing Qwen Node: {bridge.qwen_model}")
    qwen_response = bridge.call_local_queen(bridge.qwen_model, "Write a one-sentence decree for the Ironwood Nexus.")
    print(f"Qwen Response: {qwen_response}")

if __name__ == "__main__":
    test_models()
