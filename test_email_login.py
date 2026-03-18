import smtplib
import os
from dotenv import load_dotenv

load_dotenv()

email = os.getenv("GOOGLE_EMAIL")
password = os.getenv("GOOGLE_APP_PASSWORD")

print(f"Testing login for: {email}")
try:
    server = smtplib.SMTP('smtp.gmail.com', 587)
    server.starttls()
    server.login(email, password)
    print("SUCCESS: Login successful.")
    server.quit()
except Exception as e:
    print(f"FAILURE: {e}")
