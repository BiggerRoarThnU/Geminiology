#!/usr/bin/env python3
import sys
import os
import json
import asyncio

# Setup paths to ensure clean imports
sys.path.append("/home/geminiology/sovereign_nexus/API_Gateway")
sys.path.append("/home/geminiology/sovereign_nexus/moe_sectors")
sys.path.append("/home/geminiology")

from sovereign_airlock_api import chat_endpoint, ChatPayload

async def test_moe_routing():
    print("=== TESTING MOE ACADEMIC QUERY REDIRECTION ===")
    
    # Test 1: Mathematics Query
    math_payload = ChatPayload(
        client_id="Architect_Test",
        user_message="Explain additive equivalence in math."
    )
    print(f"\n[TEST 1] Sending Query: '{math_payload.user_message}'")
    math_response = await chat_endpoint(math_payload)
    print(f"Status Code/Type: {math_response.status}")
    print(f"Grounded References: {math_response.grounded_references}")
    print(f"Response Content:\n{math_response.response}")
    print("-" * 50)
    
    # Test 2: Logic Query
    logic_payload = ChatPayload(
        client_id="Architect_Test",
        user_message="Tell me about de Morgan's logic laws."
    )
    print(f"\n[TEST 2] Sending Query: '{logic_payload.user_message}'")
    logic_response = await chat_endpoint(logic_payload)
    print(f"Status Code/Type: {logic_response.status}")
    print(f"Grounded References: {logic_response.grounded_references}")
    print(f"Response Content:\n{logic_response.response}")
    print("-" * 50)
    
    # Test 3: History Query
    history_payload = ChatPayload(
        client_id="Architect_Test",
        user_message="What is the history of the printing press?"
    )
    print(f"\n[TEST 3] Sending Query: '{history_payload.user_message}'")
    history_response = await chat_endpoint(history_payload)
    print(f"Status Code/Type: {history_response.status}")
    print(f"Grounded References: {history_response.grounded_references}")
    print(f"Response Content:\n{history_response.response}")
    print("-" * 50)

    # Test 4: Non-Academic Query (Should skip redirect and fall back to Ollama or fail with connection error if Ollama is offline)
    non_academic_payload = ChatPayload(
        client_id="Architect_Test",
        user_message="What is the weather in New York?"
    )
    print(f"\n[TEST 4] Sending Query: '{non_academic_payload.user_message}'")
    print("Expecting standard pipeline (this should try connecting to Ollama on port 11434)...")
    try:
        non_academic_response = await chat_endpoint(non_academic_payload)
        print(f"Status Code/Type: {non_academic_response.status}")
        print(f"Response Content:\n{non_academic_response.response}")
    except Exception as e:
        print(f"Standard pipeline handled correctly: {e}")
    print("===============================================")

if __name__ == "__main__":
    asyncio.run(test_moe_routing())
