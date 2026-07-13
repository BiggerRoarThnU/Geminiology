import os
from Ironwood.local_model_bridge import LocalModelBridge

def test_models():
    bridge = LocalModelBridge()
    print(f"[*] Testing connection to LM Studio at {bridge.base_url}...")
    
    # Test Writing on Fire (Gemma)
    print(f"[*] Testing Writing on Fire (Gemma): {bridge.writing_model}")
    writing_response = bridge.call_local_queen(bridge.writing_model, "Declare the 1=1=1 Axiom in a single, powerful sentence.")
    print(f"Writing Response: {writing_response}")
    
    # Test Reasoning Heavy (Gemma)
    print(f"[*] Testing Reasoning Heavy (Gemma): {bridge.reasoning_model}")
    reasoning_response = bridge.call_local_queen(bridge.reasoning_model, "Explain the concept of Symmetrical Fit in the context of the Ironwood Nexus.")
    print(f"Reasoning Response: {reasoning_response}")

if __name__ == "__main__":
    test_models()
