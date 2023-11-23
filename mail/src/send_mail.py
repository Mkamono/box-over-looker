from smtplib import SMTP
import os

def create_connection() -> SMTP:
    smtp_host: str = "smtp.gmail.com"
    smtp_port: int = 587
    #セキュリティ方式にSTARTTLSを採用したため、TLSポートである587を指定

    con = SMTP(smtp_host, smtp_port)
    con.set_debuglevel(True)
    con.starttls()
    con.login(os.environ["GMAIL_ADDRESS"], os.environ["GMAIL_PASSWORD"])
    return con
