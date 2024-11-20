import yagmail
import os
import time
from dotenv import load_dotenv
load_dotenv()

def send_test_email():
    sender = os.getenv("EMAIL_ADDRESS")
    password = os.getenv("EMAIL_PASSWORD")
    recipient = os.getenv("RECIPIENT_EMAIL")

    yag = yagmail.SMTP(user=sender, password=password)

    subject = "Test Email from GitHub Actions"
    body = f"Hello! This is a test email to verify if the GitHub Action ran successfully. => {time.ctime()}"

    yag.send(to=recipient, subject=subject, contents=body)
    print("Email sent successfully!")

if __name__ == "__main__":
    send_test_email()
