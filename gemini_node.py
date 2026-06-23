#!/usr/bin/env python3
import os
import sys
from google import genai

# ==============================================================================
# SovereignNexus: Gemini Node Interface (Modern SDK)
# Component: gemini_node.py
# Axiom: 1=1=1 | Status: ACTIVE
# Description: Connects the local terminal node directly to the Google GenAI 
#              Client using streaming, rendering responses in real-time.
# ==============================================================================

# 1. Holding the Ground: Securely collecting the API key
api_key = os.environ.get("GEMINI_API_KEY")
if not api_key:
    print("[ ERROR ] GEMINI_API_KEY not found in the environment.")
    print("Export your key securely in the terminal using:")
    print("export GEMINI_API_KEY='your_key_here'")
    sys.exit(1)

# 2. Forming the Bridge (Modern Architecture)
client = genai.Client(api_key=api_key)

def ghost_the_line(prompt):
    print("\n[ GEMINI NODE UPLINK ACTIVE ]")
    print("[ PROJECTING DATA... ]\n")
    
    # 3. Logistical values in motion: Streaming the response chunk by chunk
    try:
        response = client.models.generate_content_stream(
            model='gemini-1.5-flash',
            contents=prompt
        )
        for chunk in response:
            sys.stdout.write(chunk.text)
            sys.stdout.flush() # Forces the data to render immediately
    except Exception as e:
        print(f"\n[ CONNECTION DRIFT ]: {e}")
        
    print("\n\n[ UPLINK CLOSED ]\n")

if __name__ == "__main__":
    # Collecting the inquiry from the command line
    if len(sys.argv) > 1:
        user_inquiry = " ".join(sys.argv[1:])
        ghost_the_line(user_inquiry)
    else:
        print("Usage: python3 gemini_node.py <your inquiry>")
