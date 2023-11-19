import os
from email.mime.multipart import MIMEMultipart
from smtplib import SMTP


def create_message() -> MIMEMultipart:
    return MIMEMultipart()


def create_connection() -> SMTP:
    con = SMTP("smtp.gmail.com", 587)
    con.set_debuglevel(True)
    con.starttls()
    con.login(os.environ["FROM_ADDRESS"], os.environ["LOGIN_PASSWORD"])
    return con


def send_email() -> None:
    message = create_message()
    con = create_connection()
    con.send_message(message)
    con.close()
