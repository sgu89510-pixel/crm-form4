from flask import Flask, request, jsonify, send_from_directory
import requests
import os

app = Flask(__name__)

@app.route("/")
def index():
    return send_from_directory("", "lead_form.html")

@app.route("/submit", methods=["POST"])
def submit():
    try:
        data = request.get_json()

        if not data:
            return jsonify({"success": False, "error": "Нет данных"}), 400

        # Корректный IP
        forwarded = request.headers.get("X-Forwarded-For", "")
        ip = forwarded.split(",")[0] if forwarded else request.remote_addr

        payload = {
            "affc": "AFF-O20FT4UUAO",
            "bxc": "BX-CL0XOBD3BRQ48",
            "vtc": "VT-HP8XSRMKVS6E7",

            "profile": {
                "firstName": data.get("firstName", ""),
                "lastName": data.get("lastName", ""),
                "email": data.get("email", ""),
                "password": "Temp12345!",
                "phone": data.get("phone", "").replace("+", "")
            },

            "ip": ip,
            "funnel": "AtomKz",
            "landingURL": "https://mercedes-4371.onrender.com",
            "geo": "KZ",
            "lang": "ru",
            "landingLang": "ru",
            "userAgent": request.headers.get("User-Agent"),
            "comment": None
        }

        CRM_URL = "https://symbios.hn-crm.com/api/external/integration/lead"

        headers = {
            "Content-Type": "application/json",
            "x-api-key": "53486a07-a2fc-4811-9375-a4eb919f0cec"
        }

        response = requests.post(CRM_URL, json=payload, headers=headers, timeout=20)

        return jsonify({
            "success": True,
            "crm_status": response.status_code,
            "crm_response": response.text,
            "sent_payload": payload
        })

    except Exception as e:
        return jsonify({"success": False, "error": str(e)}), 500


if __name__ == "__main__":
    port = int(os.environ.get("PORT", 5000))
    app.run(host="0.0.0.0", port=port)