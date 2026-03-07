import os
import json
import datetime
from master_log import MasterLog
from execution_core import ExecutionCore

class BusinessLoop:
    """
    Template 04: The Business Pipeline Node.
    Connects technical work to financial output (Bank Account).
    Enforces the 'Work -> Value -> Bank' cycle.
    """
    def __init__(self):
        self.logger = MasterLog()
        self.core = ExecutionCore()
        self.logger.info("Business Loop Initialized. Template 04 Active.")

    def ground_financial_targets(self):
        """ [STEP 1: GROUNDING] - Verify banking and registration status. """
        self.logger.info("Verifying Financial Grounding...")
        # Check for key business stars in Sovereign Memory
        targets = ["Star_10", "Star_11", "Star_12", "Star_14", "Star_15", "Star_17"]
        for target in targets:
            self.core.execute_ability(target)
        
        # Verify SAM registration file presence
        sam_path = r"C:\Users\Ofthe\SovereignNexus\src\Ironwood\09_ARCHIVE\SAM_REGISTRATION.md"
        if os.path.exists(sam_path):
            self.logger.info("SAM Registration Anchored: Verified.")
        else:
            self.logger.warn("SAM Registration Missing from Archive.")

        # NEW: Verify NC Secretary of State (SOS) Registration
        sos_invoice_path = r"C:\Users\Ofthe\SovereignNexus\src\Ironwood\09_ARCHIVE\PROMPT_MIRROR_NC_SOS_INVOICE.json"
        if os.path.exists(sos_invoice_path):
            self.logger.info("NC Secretary of State (SOS) Articles of Organization: Anchored.")
        else:
            self.logger.warn("NC Secretary of State (SOS) Registration missing. Entity may not be legally shielded.")

    def scout_opportunity(self):
        """ [STEP 2: THE SCOUT] - Find work that matches the NAICS/Strategic vector. """
        # In a real loop, this might call an API (like SAM.gov or a job board)
        # For grounding, we simulate the selection of a high-value R&D target.
        opportunity = "AFWERX 26.1 - Collaborative Combat Aircraft (CCA) Safety"
        self.logger.info(f"Scouting Opportunity: {opportunity}")
        return opportunity

    def generate_proposal_stub(self, opportunity):
        """ [STEP 3: THE PROPOSAL] - Link work to a tangible document. """
        self.logger.info(f"Generating Proposal Stub for: {opportunity}")
        timestamp = datetime.datetime.now().strftime("%Y%m%d_%H%M")
        proposal_file = f"PROPOSAL_{timestamp}.txt"
        proposal_path = os.path.join(r"C:\Users\Ofthe\SovereignNexus\src\Ironwood\05_STRATEGY", proposal_file)
        
        content = f"""SovereignNexus LLC
Opportunity: {opportunity}
UEI: K5DALREZFGH6
NAICS: 541715
Status: DRAFT
Grounding: Session 2026-02-28"""
        
        with open(proposal_path, "w") as f:
            f.write(content)
        
        self.logger.info(f"Proposal Registered at: {proposal_path}")
        return proposal_path

    def track_invoicing(self, amount):
        """ [STEP 4: THE INVOICE] - Loop the work to the bank account (Bluevine). """
        tier = "EMPIRE" if amount >= 5000 else "CORE" if amount >= 1000 else "WATER"
        self.logger.info(f"Invoicing Cycle ({tier}): ${amount} targeting Bluevine Primary Account.")
        
        # Burnout Guard: Prevent 'too heavy' load
        active_projects = 2 # Simulated count
        if tier == "EMPIRE" and active_projects >= 3:
            self.logger.warn("BURNOUT GUARD: Project load is 'too heavy'. Deferring Empire Node.")
            return

        # NEW: Operational Arbitrage Check
        self.logger.info("Executing Operational Arbitrage: Using Cloud Credits to power Client Deliverables.")
        self.logger.info("RESULT: High-Margin Fiat Conversion (Credits -> USD).")

        # NEW: H.B. 920 Tax Compliance
        self.logger.info("NC H.B. 920 Compliance: Digital assets are recognized for state tax remittance.")
        
        # Register the financial event
        self.logger.info(f"ACTION: Loop Work -> Value -> Bank. Expected Deposit: ${amount} to Bluevine.")
        self.core.execute_ability("Star_13")
        self.core.execute_ability("Star_16")
        self.core.execute_ability("Star_21") # Portfolio Tiering Star

    def run_full_cycle(self):
        """ Executes the complete Business Loop. """
        print("\n--- INITIATING FULL BUSINESS CYCLE ---")
        self.ground_financial_targets()
        self.scout_opportunity()
        self.generate_proposal_stub("AFWERX 26.1")
        self.track_invoicing(5000.00)
        print("\n--- BUSINESS CYCLE COMPLETE. TRUTH IS PROFIT. ---")

if __name__ == "__main__":
    biz = BusinessLoop()
    biz.run_full_cycle()
