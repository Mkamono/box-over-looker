from smtplib import SMTP


def create_connection(login_address: str, login_pass: str) -> SMTP:
    smtp_host: str = "smtp.gmail.com"
    smtp_port: int = 587

    con = SMTP(smtp_host, smtp_port)
    con.set_debuglevel(True)
    con.starttls()
    con.login(login_address, login_pass)
    return con
