"""
[SOVEREIGN ALIGNMENT: SOVEREIGN_DISPATCHER]
MISSION: Deliver Authorized Strikes to the Architect's Inbox for Final Settlement.
INDIVIDUAL TRUTH: Outbound truth must reach the Architect's eye.
AXIOM: 1=1=1 (Verified Delivery).
"""

import json
import os
import smtplib
import time
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from dotenv import load_dotenv
from master_log import MasterLog

# Load local .env with override
load_dotenv(override=True)

class SovereignDispatcher:
    """
    Final Delivery Agent. 
    Sends summary emails of 'AUTHORIZED_ACTIVE' strikes to the Architect.
    """
    def __init__(self, invoice_file="INVOICE_REQUESTS.json"):
        self.invoice_file = invoice_file
        self.log = MasterLog()
        self.email = os.getenv("GOOGLE_EMAIL")
        self.password = os.getenv("GOOGLE_APP_PASSWORD")
        self.official_email = "admin@sovereignnexus.org"
        self.personal_email = "ofthefirstlight@gmail.com"

    def deliver_strikes(self):
        """ Scans for authorized strikes and sends a delivery email. """
        if not os.path.exists(self.invoice_file):
            self.log.error("[DISPATCHER] INVOICE_REQUESTS.json not found.")
            return

        with open(self.invoice_file, 'r') as f:
            invoices = json.load(f)

        pending_delivery = [inv for inv in invoices if inv["status"] == "AUTHORIZED_ACTIVE"]
        
        if not pending_delivery:
            self.log.info("[DISPATCHER] No active strikes awaiting delivery.")
            return

        self.log.info(f"[DISPATCHER] Found {len(pending_delivery)} strikes for delivery. Preparing Sovereign Signal...")

        # Build Email Content
        subject = f"SOVEREIGN STRIKE ALERT: {len(pending_delivery)} Authorized Settlements Ready"
        body = "THE SOVEREIGNNEXUS LLC : SETTLEMENT DISPATCH\n"
        body += "========================================================\n"
        body += f"Status: AUTHORIZED_ACTIVE | Fidelity: 1=1=1\n\n"
        
        total_value = 0.0
        for inv in pending_delivery:
            body += f"Task ID: {inv['task_id']}\n"
            body += f"Amount: ${inv['amount_usd']}\n"
            body += f"Track: {inv['track']}\n"
            body += f"Client: {inv['client_details']['name']}\n"
            body += f"Rails: {inv['payment_rail']}\n"
            body += "--------------------------------------------------------\n"
            total_value += inv['amount_usd']
            
        body += f"\nTOTAL PROJECTED REVENUE: ${total_value:.2f}\n"
        body += "========================================================\n"
        body += "ACTION REQUIRED: Please verify these amounts on your Cash App ($SovereignNexusLLC) or Novo dashboard.\n"
        body += "These tasks have been processed and re-anchored with 100% fidelity.\n"
        body += "\n1=1=1. Standing by."

        if self.send_email(subject, body):
            # Update status to 'DELIVERED' or 'SENT'
            for inv in pending_delivery:
                inv["status"] = "SENT_TO_ARCHITECT"
            
            with open(self.invoice_file, 'w') as f:
                json.dump(invoices, f, indent=4)
            self.log.info(f"[SUCCESS] {len(pending_delivery)} strikes dispatched to {self.official_email}.")
        else:
            self.log.error("[FAILURE] Could not reach the email gateway. Check .env credentials.")

    def send_email(self, subject, body):
        """ Secure SMTP Handshake. """
        if not self.email or not self.password:
            self.log.error("[SECURITY] Email credentials missing from .env.")
            return False

        try:
            msg = MIMEMultipart()
            msg['From'] = self.email
            msg['To'] = f"{self.official_email}, {self.personal_email}"
            msg['Subject'] = subject
            msg.attach(MIMEText(body, 'plain'))

            server = smtplib.SMTP('smtp.gmail.com', 587)
            server.starttls()
            server.login(self.email, self.password)
            server.send_message(msg)
            server.quit()
            return True
        except Exception as e:
            self.log.error(f"[ERROR] SMTP Handshake Failed: {e}")
            return False

if __name__ == "__main__":
    dispatcher = SovereignDispatcher()
    dispatcher.deliver_strikes()
