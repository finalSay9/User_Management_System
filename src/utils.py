import smtplib
from email.mime.text import MIMEText

def send_reset_email(email: str, reset_token: str, company_name: str = "YourCompany"):
    reset_url = f"https://yourapp.com/reset-password?token={reset_token}"
    msg = MIMEText(f"Click to set your password: {reset_url}\nThis link expires in 24 hours.")
    msg['Subject'] = f"Set Your {company_name} Account Password"
    msg['From'] = "no-reply@company.com"
    msg['To'] = email

    with smtplib.SMTP("smtp.gmail.com", 587) as server:
        server.starttls()
        server.login("your_email@gmail.com", "your_app_password")
        server.send_message(msg)