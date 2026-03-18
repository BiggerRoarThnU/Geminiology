import json
import os
from openclaw_settlement_engine import OpenClawSettlementEngine

def purify_invoice_requests():
    """
    Reflashes INVOICE_REQUESTS.json with the 'Warm Fit' financial truth.
    Ensures all 44 strikes (and future ones) have the correct dual-rail info.
    """
    engine = OpenClawSettlementEngine()
    invoice_file = "INVOICE_REQUESTS.json"
    
    if not os.path.exists(invoice_file):
        print("[ERROR] INVOICE_REQUESTS.json not found.")
        return

    with open(invoice_file, 'r') as f:
        data = json.load(f)
    
    purified_count = 0
    for req in data:
        # Update payment options to the current 'Warm Fit' truth
        req["payment_options"] = {
            "cash_app_tag": engine.cash_app_tag,
            "cash_app_routing": engine.cash_app_routing,
            "cash_app_account": engine.cash_app_account,
            "novo_routing": engine.novo_routing,
            "novo_account": engine.novo_account,
            "beneficiary_name": engine.beneficiary_name,
            "beneficiary_address": engine.beneficiary_address,
            "bank_name": engine.bank_name,
            "bank_swift": engine.bank_swift,
            "bank_address": engine.bank_address,
            "invoice_link_policy": "On-Demand Only"
        }
        # Update the rail description
        req["payment_rail"] = f"Dual-Rail: Cash App ({engine.cash_app_tag}) or Novo ACH/Wire"
        # Ensure the policy note is correct
        req["policy_note"] = engine.policy_note
        purified_count += 1
        
    with open(invoice_file, 'w') as f:
        json.dump(data, f, indent=4)
    
    print(f"[SUCCESS] Purified {purified_count} invoice requests with the 'Warm Fit' truth.")

if __name__ == "__main__":
    purify_invoice_requests()
