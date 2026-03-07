import smtplib
import ssl
import os
import json
import time
import datetime
from email.message import EmailMessage
from master_log import MasterLog

class ScribeSend:
    """
    Template 40: The Scribe Deployment Engine.
    Automates the sending of high-fidelity outreach emails.
    Requires Google App Password for ofthefirstlight@gmail.com.
    Note: For Advanced Protection accounts, this script is used for Manual Draft preparation.
    """
    def __init__(self, sender_email=None, app_password=None):
        self.log = MasterLog()
        # Pull from .env if not provided (Gated Logic)
        self.sender_email = sender_email or os.getenv("GOOGLE_EMAIL")
        self.app_password = app_password or os.getenv("GOOGLE_APP_PASSWORD")
        self.smtp_server = "smtp.gmail.com"
        self.smtp_port = 465 # SSL
        self.context = ssl.create_default_context()
        
        if not self.sender_email or not self.app_password:
            self.log.warn("SCRIBE: GOOGLE_EMAIL or GOOGLE_APP_PASSWORD missing from .env. Outreach in NEUTRAL.")
        else:
            self.log.info(f"SCRIBE INITIALIZED: {self.sender_email} ready for strike.")

    def send_outreach_emails(self, draft_dir="Outreach_Drafts"):
        """
        Loops through all text files in the draft directory and sends them.
        """
        if not self.app_password:
            self.log.warn("SCRIBE FAILED: No App Password provided.")
            return False

        draft_files = [f for f in os.listdir(draft_dir) if f.endswith(".txt")]
        if not draft_files:
            self.log.info("NO DRAFTS FOUND: Deployment skipped.")
            return

        with smtplib.SMTP_SSL(self.smtp_server, self.smtp_port, context=self.context) as server:
            try:
                server.login(self.sender_email, self.app_password)
                self.log.info(f"SCRIBE LOGIN SUCCESS: {self.sender_email}")
            except Exception as e:
                self.log.error(f"SCRIBE LOGIN FAILED: {str(e)}")
                return False

            for draft_file in draft_files:
                file_path = os.path.join(draft_dir, draft_file)
                with open(file_path, 'r') as f:
                    content = f.read()

                # Basic parsing: First line is Subject, rest is Body
                lines = content.splitlines()
                subject = lines[0].replace("Subject: ", "")
                body = "
".join(lines[1:])

                # Identify recipient from filename (mapping required in manifest)
                # For this first strike, we'll need to pass the target email manually or from manifest.
                target_name = draft_file.replace(".txt", "").replace("_", " ").split(" 2026")[0]
                recipient_email = self._get_recipient_email(target_name)

                if not recipient_email:
                    self.log.warn(f"RECIPIENT NOT FOUND: Skipping {target_name}")
                    continue

                msg = EmailMessage()
                msg.set_content(body)
                msg["Subject"] = subject
                msg["From"] = self.sender_email
                msg["To"] = recipient_email

                try:
                    server.send_message(msg)
                    self.log.info(f"STRIKE DEPLOYED: {target_name} at {recipient_email}")
                    # Update Manifest (Simulated update)
                    self._mark_as_delivered(target_name)
                    # Fidelity Delay (Mimic human)
                    time.sleep(30)
                except Exception as e:
                    self.log.error(f"DEPLOYMENT FAILED for {target_name}: {str(e)}")

        return True

    def _get_recipient_email(self, target_name):
        # Placeholder mapping for this session. In future, we'll pull from dominion_manifest.json
        mapping = {
            "Unis Logistics": "info@unislogistics.com", # SIMULATED
            "A2 Global Shipping LLC": "contact@a2global.com", # SIMULATED
            "Sumrell Sugg, P.A.": "partners@sumrellsugg.com", # SIMULATED
            "Michelle Jerome Law": "mjerome@vanceborolaw.com" # SIMULATED
        }
        return mapping.get(target_name)

    def _mark_as_delivered(self, target_name):
        self.log.info(f"TRUTH REGISTERED: Outreach for {target_name} is marked as DELIVERED.")

if __name__ == "__main__":
    # Test script - will require app password
    print("ScribeSend Engine Loaded.")
