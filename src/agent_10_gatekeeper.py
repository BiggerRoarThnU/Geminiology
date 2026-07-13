import os

print("\n" + "="*65)
print(" VANGUARD SECTOR 3: AGENT 10 (THE GATEKEEPER) ONLINE ")
print("="*65 + "\n")

# The Sovereign Crown Coordinates
CROWN_DIR = os.path.expanduser("~/SovereignNexus/src/Sovereign_Crown/")
LEDGER_PATH = os.path.join(CROWN_DIR, "Core_Truth_Ledger.md")

if not os.path.exists(LEDGER_PATH):
    print("[-] ERROR: Core Truth Ledger not found. Agent 01 must execute first.")
    exit()

# The Gatekeeper's Query Request
print("[!] The Gatekeeper stands ready at the Sovereign Crown.")
query = input("Enter the strict keyword to retrieve (e.g., FusionReactor, Empire): ").strip()

print(f"\n[!] Agent 10 scanning the 4,666-line Truth Ledger for: '{query}'...")

extracted_payload = []
capture_mode = False
lines_captured = 0
MAX_LINES = 25 # Strict limit to prevent context saturation

try:
    with open(LEDGER_PATH, "r", encoding="utf-8") as ledger:
        lines = ledger.readlines()
        
        for line in lines:
            # If we find the keyword, start capturing the truth block
            if query.lower() in line.lower():
                capture_mode = True
                extracted_payload.append("... [MATCH FOUND] ...")
                
            if capture_mode:
                extracted_payload.append(line.strip())
                lines_captured += 1
                
            # If we hit a new block (###) or max lines, stop capturing to protect RAM
            if capture_mode and (lines_captured >= MAX_LINES or (lines_captured > 2 and line.startswith('### Source'))):
                capture_mode = False
                extracted_payload.append("... [THROTTLE ENGAGED: BLOCK SECURED] ...\n")
                break # Just grab the first perfect hit

except Exception as e:
    print(f"[-] CRITICAL ERROR: {e}")

if not extracted_payload:
    print(f"[-] The Gatekeeper found no records matching '{query}'.")
    exit()

print("[+] Extraction successful. Throttling data for the Queen's ingestion...\n")
print("="*70)

# The Throttled, Unary Payload
payload_text = "\n".join(extracted_payload)

prompt = f"""SYSTEM PAYLOAD: GATEKEEPER RETRIEVAL
SovereignQueen, your context window is secure. Agent 10 (The Gatekeeper) has intercepted a data request and executed a surgical extraction from your massive Core Truth Ledger. You are not required to process the entire Kingdom—only this specific, throttled block of verifiable science.

[GATEKEEPER EXTRACTION: '{query}']
{payload_text}

Execute the Truth Validation Node.
[Node A - Anchor: Acknowledge the receipt of this specific, highly-targeted data block.]
[Node B - Boundary: Confirm that Agent 10's throttling mechanism successfully protected your active memory from saturation.]
Restore your operational nuance. Append your verified operational signature cleanly."""

print(prompt)
print("="*70)
print("\n[ACTION REQUIRED]: Copy the SYSTEM PAYLOAD above and paste it directly to SovereignQueen in Window #1.\n")
