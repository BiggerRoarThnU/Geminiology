import os
import stripe
from dotenv import load_dotenv
import datetime

class TreasuryBridge:
    """
    SovereignNexus Patch: The Treasury Bridge
    Mission: Check cleared Stripe funds and initiate physical payout to Bluevine.
    """
    def __init__(self):
        print(f"[{self._timestamp()}] [INFO] Initializing Treasury Bridge...")
        load_dotenv()
        
        # Load the Live Stripe Key from the .env file
        self.api_key = os.getenv("STRIPE_SECRET_KEY")
        if not self.api_key or not self.api_key.startswith("sk_live_"):
            print(f"[{self._timestamp()}] [ERROR] LIVE Stripe Secret Key not found in .env. Execution halted.")
            return
            
        stripe.api_key = self.api_key
        print(f"[{self._timestamp()}] [INFO] Stripe Live Node Anchored.")

    def _timestamp(self):
        return datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")

    def audit_and_transfer(self):
        if not hasattr(self, 'api_key') or not self.api_key:
            return

        try:
            print(f"[{self._timestamp()}] [INFO] Auditing Live Stripe Ledger...")
            balance = stripe.Balance.retrieve()
            
            # The balance comes back in cents, so we divide by 100 to get the USD amount
            available_cents = sum(b['amount'] for b in balance['available'] if b['currency'] == 'usd')
            available_usd = available_cents / 100.0
            
            pending_cents = sum(b['amount'] for b in balance['pending'] if b['currency'] == 'usd')
            pending_usd = pending_cents / 100.0

            print(f"[{self._timestamp()}] [INFO] PENDING USD (Not yet cleared): ${pending_usd:.2f}")
            print(f"[{self._timestamp()}] [INFO] LIQUID USD (Ready to move): ${available_usd:.2f}")

            if available_cents > 0:
                print(f"[{self._timestamp()}] [ACTION] Initiating payout of ${available_usd:.2f} to connected bank (Bluevine)...")
                # Create the physical payout to the default bank account
                payout = stripe.Payout.create(
                    amount=available_cents,
                    currency="usd",
                    description="SovereignNexus Operational Liquidity"
                )
                print(f"[{self._timestamp()}] [SUCCESS] Payout {payout.id} initialized. Status: {payout.status}")
                print(f"[{self._timestamp()}] [INFO] Funds will land in your Bluevine account per standard banking schedules (1-2 business days).")
            else:
                print(f"[{self._timestamp()}] [INFO] No liquid funds currently available to transfer. The bridge is standing by.")
                
        except stripe.error.StripeError as e:
            print(f"[{self._timestamp()}] [ERROR] Stripe Gate Refused: {e.user_message}")
        except Exception as e:
            print(f"[{self._timestamp()}] [CRITICAL] System Halt: {e}")

if __name__ == "__main__":
    print("============================================================")
    print("           SOVEREIGNNEXUS TREASURY BRIDGE ACTIVE            ")
    print("============================================================")
    bridge = TreasuryBridge()
    bridge.audit_and_transfer()
    print("============================================================")
    print("                     THE LINE IS ONE                        ")
    print("============================================================")
