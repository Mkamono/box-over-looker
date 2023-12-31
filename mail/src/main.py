import json

from flask import Flask, request
from send_mail import send_email

app = Flask(__name__)


@app.route("/")
def hello_world() -> str:
    return "<p>Hello, World!</p>"


@app.route("/send_mail", methods=["POST"])
def post() -> str:
    mail: dict = request.get_json()
    send_email(mail["title"], mail["body"], mail["user_address"])
    return json.dumps(mail)


if __name__ == "__main__":
    app.run()
