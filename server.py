from flask import Flask, request, send_file, jsonify
import requests
import random
import string

app = Flask(__name__)

# ================= НАСТРОЙКИ =================
API_URL = "https://rgnarads.com/api/external/integration/lead"
API_KEY = "7c787507-6e62-45cd-b1b4-f3973f248b5a"

AFFC = "AFF-SCBWWGQO2I"
BXC = "BX-P33D1QLLBBXXK"
VTC = "VT-HP8XSRMKVS6E7"

FUNNEL = "tkapital"
LANDING_URL = "https://rgnarads.com"

GEO = "KZ"
LANG = "ru"

# ================= ГЕНЕРАЦИЯ ПАРОЛЯ =================
def generate_password():
    return (
        random.choice(string.ascii_uppercase) +
        random.choice(string.ascii_lowercase) +
        random.choice(string.digits) +
        random.choice("!@#$%^&*") +
        ''.join(random.choices(string.ascii_letters + string.digits, k=6))
    )

# ================= ROUTES =================
@app.route("/", methods=["GET"])
def index():
    return send_file("lead_form.html")

@app.route("/submit", methods=["POST"])
def submit():
    payload = {
        "affc": AFFC,
        "bxc": BXC,
        "vtc": VTC,
        "profile": {
            "firstName": request.form.get("first_name"),
            "lastName": request.form.get("last_name"),
            "email": request.form.get("email"),
            "password": generate_password(),
            "phone": request.form.get("phone").replace("+", "")
        },
        "ip": request.headers.get("X-Forwarded-For", request.remote_addr),
        "funnel": FUNNEL,
        "landingURL": LANDING_URL,
        "geo": GEO,
        "lang": LANG,
        "landingLang": LANG,
        "userAgent": request.headers.get("User-Agent"),
        "comment": "Lead from landing"
    }

    headers = {
        "x-api-key": API_KEY,
        "Content-Type": "application/json"
    }

    try:
        response = requests.post(
            API_URL,
            json=payload,
            headers=headers,
            timeout=15
        )
        api_response = response.json()
    except Exception as e:
        return jsonify({
            "success": False,
            "error": str(e),
            "request": payload
        }), 500

    return jsonify({
        "request": payload,
        "response": api_response
    })


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=10000)