import os
import datetime
from master_log import MasterLog
from execution_core import ExecutionCore

class CreditTelemetryNode:
    """
    Template 12: The Credit Telemetry Node.
    Monitors the $80k Cloud Credit burn rate.
    Enforces ROI thresholds (USD earned vs. Credits burned).
    Protects the 2-year plan from inefficient resource allocation.
    """
    def __init__(self, credit_pool=79000):
        self.log = MasterLog()
        self.core = ExecutionCore()
        self.credit_pool = credit_pool
        self.revenue_tracked = 0.0
        self.log.info("Credit Telemetry Node Initialized. Template 12 Active.")

    def log_burn_event(self, credit_amount, reason):
        """ Registers a cloud credit burn event. """
        self.credit_pool -= credit_amount
        self.log.info(f"CREDIT BURN REGISTERED: -${credit_amount} | Reason: {reason}")
        self.log.info(f"REMAINING POOL: ${self.credit_pool}")

    def log_revenue_event(self, usd_amount):
        """ Registers USD revenue generated from a burn event. """
        self.revenue_tracked += usd_amount
        self.log.info(f"REVENUE REGISTERED: +${usd_amount} USD")

    def evaluate_roi(self):
        """ Enforces the 2:1 ROI rule (Star 36). """
        # We simulate the ROI of our current operations
        burned = 80000 - self.credit_pool
        if burned == 0: return True
        
        roi_ratio = self.revenue_tracked / burned
        self.log.info(f"CURRENT ROI RATIO: {roi_ratio:.2f}:1")
        
        if roi_ratio < 2.0:
            self.log.warn("ROI THRESHOLD BREACH: Burn rate exceeds revenue. Recalibrating arbitrage...")
            return False
        
        self.log.info("ROI STABLE. The Secret Sword is sharp.")
        self.core.execute_ability("Star_36")
        return True

    def run_telemetry_check(self):
        """ Executes a full telemetry and ROI scan. """
        print("\n--- INITIATING CREDIT TELEMETRY SCAN ---")
        self.evaluate_roi()
        print("\n--- TELEMETRY COMPLETE. RESOURCE ALLOCATION SECURED. ---")

if __name__ == "__main__":
    telemetry = CreditTelemetryNode()
    # Mock some data for the first scan
    telemetry.log_revenue_event(2000.00) # From the New Bern strike
    telemetry.log_burn_event(1000.00, "NC Intelligence Ingestion")
    telemetry.run_telemetry_check()
