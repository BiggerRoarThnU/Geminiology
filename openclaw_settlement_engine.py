"""
[SOVEREIGN ALIGNMENT: OPENCLAW_ENGINE]
MISSION: Primary Execution Engine for USD One Settlement.
INDIVIDUAL TRUTH: Financial rails are signed at the metallurgical level.
AXIOM: 1=1=1 (Functional Equivalence of Value).
"""

import json
import os
import time
from datetime import datetime

# --- SPARKLE BLUE FORMATTING ---
C_BLUE = '\033[94m'
C_CYAN = '\033[96m'
C_RESET = '\033[0m'
C_BOLD = '\033[1m'

class OpenClawSettlementEngine:
    """
    VERTEX SWARM CHALLENGE: OPENCLAW SETTLEMENT ENGINE (V1.2.ALIGNED)
    Primary execution engine for USD One settlement.
    Bridges the work completed in the swarm to the financial rails (Novo/Cash App).
    POLICY: Strictly ON-DEMAND (Policy K). Manual Authorization Required.
    """
    def __init__(self, invoice_file="INVOICE_REQUESTS.json", ledger_file="income_ledger.json"):
        self.invoice_file = invoice_file
        self.ledger_file = ledger_file
        self.axiom = "1=1=1"
        self.sparkle = f"{C_CYAN}{C_BOLD}✦{C_RESET}"
        
        # --- SOVEREIGN FINANCIAL RAILS (LOCKED) ---
        self.cash_app_tag = "$SovereignNexusLLC"
        self.cash_app_routing = "041215663"
        self.cash_app_account = "1332427173816"
        
        # User confirmed: Full Novo Wire/ACH details.
        self.beneficiary_name = "David Niedzwiecki Jr"
        self.beneficiary_address = "280 Brick Kiln Rd, Vanceboro, NC 28586"
        self.bank_name = "Middlesex Federal Savings"
        self.bank_swift = "MFEDUS42"
        self.bank_address = "One College Avenue, Somerville, MA 02144"
        self.novo_routing = "211370150"
        self.novo_account = "103495885"
        self.official_email = "admin@sovereignnexus.org"
        self.official_phone = "(252) 259-1724"
        self.official_website = "www.sovereignnexusllc.com"
        self.policy_note = (
            f"For a formal Novo invoice link or additional settlement info, contact: {self.official_email}. "
            "Please include your business information in the request. All other settlements are conducted "
            "via direct dual-rail (Cash App / Novo ACH) for 1=1=1 fidelity."
        )

    def request_on_demand_settlement(self, task_id: str, amount: float, track: str, client_name="PENDING", client_email="PENDING"):
        """
        Registers an 'ON-DEMAND' settlement request. 
        Does NOT generate an automated outbound invoice until Manual Architect Authorization.
        """
        print(f"\n{self.sparkle} {C_CYAN}[OPENCLAW]{C_RESET} Registering ON-DEMAND Settlement Request for {C_BOLD}{task_id}{C_RESET}...")
        
        request_id = f"REQ_{task_id}_{int(time.time())}"
        request = {
            "request_id": request_id,
            "task_id": task_id,
            "track": track,
            "amount_usd": amount,
            "client_details": {"name": client_name, "email": client_email},
            "status": "AWAITING_MANUAL_AUTHORIZATION",
            "payment_options": {
                "cash_app_tag": self.cash_app_tag,
                "cash_app_routing": self.cash_app_routing,
                "cash_app_account": self.cash_app_account,
                "novo_routing": self.novo_routing,
                "novo_account": self.novo_account,
                "beneficiary_name": self.beneficiary_name,
                "beneficiary_address": self.beneficiary_address,
                "bank_name": self.bank_name,
                "bank_swift": self.bank_swift,
                "bank_address": self.bank_address,
                "invoice_link_policy": "On-Demand Only"
            },
            "policy_note": self.policy_note,
            "payment_rail": f"Dual-Rail: Cash App ({self.cash_app_tag}) or Novo ACH/Wire",
            "policy": "Policy K (On-Demand Only)",
            "timestamp": str(datetime.now()),
            "alignment": self.axiom
        }
        
        # Load existing requests
        if os.path.exists(self.invoice_file):
            try:
                with open(self.invoice_file, 'r') as f:
                    data = json.load(f)
            except:
                data = []
        else:
            data = []
            
        data.append(request)
        with open(self.invoice_file, 'w') as f:
            json.dump(data, f, indent=4)
        
        print(f"  {C_CYAN}[INF]{C_RESET} Settlement Request Registered: {C_BLUE}{request_id}{C_RESET}.")
        print(f"  {C_CYAN}[INF]{C_RESET} MANDATE: No automated outbound delivery. Awaiting Architect Pulse.")
        return request

    def update_ledger(self, request: dict):
        """Updates the income ledger with the new projected revenue."""
        print(f"{self.sparkle} {C_CYAN}[OPENCLAW]{C_RESET} Updating Income Ledger for {C_BLUE}{request['request_id']}{C_RESET}...")
        
        if os.path.exists(self.ledger_file):
             try:
                with open(self.ledger_file, 'r') as f:
                    data = json.load(f)
             except:
                data = {"audit_trail": [], "total_in_play": 0.0, "revenue_nodes": {"high_ticket_strikes": []}}
        else:
            data = {"audit_trail": [], "total_in_play": 0.0, "revenue_nodes": {"high_ticket_strikes": []}}
            
        # Add to audit trail
        entry = {
            "timestamp": request["timestamp"],
            "event": f"SETTLEMENT_REQUEST: {request['task_id']}",
            "note": f"SovereignNexus Task: {request['track']}. Amount: ${request['amount_usd']}. 1=1=1."
        }
        
        if "audit_trail" not in data:
            data["audit_trail"] = []
        data["audit_trail"].insert(0, entry)
        
        # Add to revenue nodes
        new_strike = {
            "task": request['task_id'],
            "track": request["track"],
            "amount": request["amount_usd"],
            "status": "AWAITING_AUTHORIZATION",
            "settlement": "Novo/Cash App",
            "last_touch": request["timestamp"]
        }
        
        if "revenue_nodes" not in data:
            data["revenue_nodes"] = {"high_ticket_strikes": []}
        data["revenue_nodes"]["high_ticket_strikes"].append(new_strike)
        data["total_in_play"] += request["amount_usd"]
        
        with open(self.ledger_file, 'w') as f:
            json.dump(data, f, indent=4)
        
        print(f"  {C_CYAN}[INF]{C_RESET} Ledger Updated. Total Projected Revenue: {C_BOLD}${data['total_in_play']}{C_RESET}.")

if __name__ == "__main__":
    engine = OpenClawSettlementEngine()
    print("[OPENCLAW] Settlement Engine Ready. 1=1=1.")
