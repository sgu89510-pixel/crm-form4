from flask import Flask, request, send_file, jsonify
import requests
import os
import random
import string

app = Flask(__name__)

def generate_password():
    return (
        random.choice(string.ascii_uppercase) +
        random.choice(string.ascii_lowercase) +
        random.choice(string.digits) +
        random.choice("!@#$%^&*") +
        ''.join(random.choices(string.ascii_letters + string.digits, k=6))
    )
    
# === CONFIG ===
API_URL = "https://rgnarads.com/api/external/integration/lead"
API_KEY = "7c787507-6e62-45cd-b1b4-f3973f248b5a"

AFFC = "AFF-SCBWWGQO2I"
BXC = "BX-P33D1QLLBBXXK"
VTC = "VT-HP8XSRMKVS6E7"

FUNNEL = "tkapital"
GEO = "RU"
LANG = "ru"

# === ROUTES ===

@app.route("/", methods=["GET"])
def index():
    return send_file("lead_form.html")

@app.route("/submit", methods=["POST"])
def submit():
    try:
        data = {
            "affc": AFFC,
            "bxc": BXC,
            "vtc": VTC,
            "profile": {
                "firstName": request.form.get("first_name"),
                "lastName": request.form.get("last_name"),
                "email": request.form.get("email"),
                "password": generate_password(),
                "phone": request.form.get("phone")
            },
            "ip": request.remote_addr,
            "funnel": FUNNEL,
            "landingURL": "https://rgnarads.com",
            "geo": GEO,
            "lang": LANG,
            "landingLang": LANG,
            "userAgent": request.headers.get("User-Agent")
        }

        headers = {
            "x-api-key": API_KEY,
            "Content-Type": "application/json"
        }

        response = requests.post(API_URL, json=data, headers=headers, timeout=10)

        return jsonify({
            "request": data,
            "response": response.json(),
            "status_code": response.status_code
        })

    except Exception as e:
        return jsonify({
            "error": str(e)
        }), 500


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000)