import os
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from smtplib import SMTP


def create_connection() -> SMTP:
    smtp_host: str = "smtp.gmail.com"
    smtp_port: int = 587
    # セキュリティ方式にSTARTTLSを採用したため、TLSポートである587を指定

    con = SMTP(smtp_host, smtp_port)
    con.set_debuglevel(True)
    con.starttls()
    con.login(os.environ["GMAIL_ADDRESS"], os.environ["GMAIL_PASSWORD"])
    return con


def createMailMessageMIME(title: str, body: str, user_address: str) -> MIMEMultipart:
    msg = MIMEMultipart()
    msg["Subject"] = title
    msg["From"] = os.environ["GMAIL_ADDRESS"]
    msg["To"] = user_address
    msg.attach(MIMEText(body, "plain", "utf-8"))

    return msg


def send_email(title, body: str, user_address: str) -> None:
    message = createMailMessageMIME(title, body, user_address)
    con = create_connection()
    con.send_message(message)
    con.close()
