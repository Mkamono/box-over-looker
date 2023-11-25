from smtplib import SMTPRecipientsRefused

from flask import Flask, request
from requests.exceptions import InvalidURL, MissingSchema
from send_mail import send_email

app = Flask(__name__)


@app.route("/")
def hello_world() -> str:
    return "<p>Hello, World!</p>"


@app.route("/send_mail", methods=["POST"])
def post() -> str:
    mail: dict = request.get_json()
    if mail is None:
        raise MissingSchema("Request body is missing")
    for key in ["title", "body", "user_address"]:
        if key not in mail:
            raise InvalidURL(f"'{key}' is missing in the request body")
    try:
        send_email(mail["title"], mail["body"], mail["user_address"])
    except SMTPRecipientsRefused as e:
        return "Invalid email address"
    except Exception as e:
        return str(e)
    return "OK"
