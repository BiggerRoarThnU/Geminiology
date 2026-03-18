import os
import sys
from Ironwood.local_model_bridge import LocalModelBridge

def consult_vampire():
    bridge = LocalModelBridge()
    # Using vampire-v1 for deep-reasoning audit
    model = "vampire-v1"
    
    audit_context = """
    User Mandate:
    1. Direct Settlement: Cash App ($SovereignNexusLLC) and Novo (Routing/Account).
    2. Invoice Policy: strictly on-demand (Policy K). No automated invoices.
    3. Outreach Policy: 'Receive Only' applies ONLY to spam/solicitation. 
       B2B outreach for high-value tasks/workflows is AUTHORIZED.
    4. Goal: Stop 'undermining' the Architect by over-restricting legitimate work.
    """
    
    prompt = f"As the Vampire Auditor (Reasoning Node), audit the following context and provide 3 precise, logical steps to ensure the SovereignNexus code (Settlement and Loop) perfectly reflects this mandate without 'cutting off' the Architect's reach: {audit_context}"
    
    print("="*60)
    print("  V A M P I R E   A U D I T O R :   3 6 0   A L I G N M E N T")
    print("="*60)
    print(f"[*] Consulting the Vampire Node ({model})...\n")
    
    try:
        response = bridge.call_local_queen(model, prompt)
        print(f"{response.strip()}\n")
    except Exception as e:
        print(f"[CONNECTION ERROR: {e}]")

if __name__ == "__main__":
    consult_vampire()
