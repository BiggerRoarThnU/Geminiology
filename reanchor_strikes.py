import json
import os
from Ironwood.local_model_bridge import LocalModelBridge
from openclaw_settlement_engine import OpenClawSettlementEngine
from master_log import MasterLog

def reanchor_strikes():
    """
    Sends a correction/alignment notice to all 44 strikes in INVOICE_REQUESTS.json.
    Ensures they have the updated 'Warm Fit' info and the new SovereignNexus Bio.
    """
    bridge = LocalModelBridge()
    engine = OpenClawSettlementEngine()
    log = MasterLog()
    
    invoice_file = "INVOICE_REQUESTS.json"
    if not os.path.exists(invoice_file):
        print("[ERROR] INVOICE_REQUESTS.json not found.")
        return

    with open(invoice_file, 'r') as f:
        strikes = json.load(f)

    bio = """
    SovereignNexus LLC is a premier agentic infrastructure firm founded by Architect David Niedzwiecki Jr. 
    We specialize in high-fidelity AI security, B2B digital salvage, and high-frequency agentic workflows.
    Operating on the 1=1=1 axiom of functional equivalence, we bridge the gap between human intent and 
    machine execution with absolute precision.
    """
    
    payment_info = (
        f"Direct Rail Duality (1=1=1): Cash App ({engine.cash_app_tag}) "
        f"or Novo Wire/ACH (Routing: {engine.novo_routing}). "
        f"Contact {engine.official_email} for on-demand link requests."
    )

    print(f"[*] Starting Re-Anchoring for {len(strikes)} strikes...")

    for strike in strikes:
        task_id = strike.get("task_id", "UNKNOWN")
        client = strike.get("client_details", {}).get("name", "B2B Partner")
        
        reanchor_prompt = (
            f"You are the SovereignNexus Digital Queen. Send a professional alignment notice to '{client}' "
            f"regarding task '{task_id}'. Include our updated bio: {bio}. "
            f"Confirm our dual-rail settlement info: {payment_info}. "
            "Write a 3-sentence high-fidelity correction and alignment message."
        )
        
        try:
            # Using writing model (digital-queen)
            message = bridge.call_local_queen(bridge.writing_model, reanchor_prompt)
            log.info(f"FIXED & COMMUNICATED [{task_id}]: {message.strip()}")
            print(f"  [✓] Re-Anchored: {task_id}")
        except Exception as e:
            log.error(f"RE-ANCHOR ERROR [{task_id}]: {e}")

if __name__ == "__main__":
    reanchor_strikes()
