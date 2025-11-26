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
        data = request.form.to_dict()

        if not data:
            return jsonify({"success": False, "error": "Нет данных"}), 400

        # IP лида
        forwarded = request.headers.get("X-Forwarded-For", "")
        ip = forwarded.split(",")[0] if forwarded else request.remote_addr

        # CRM принимает только form-data! НЕ JSON
        payload = {
            "name": data.get("name", ""),
            "lastname": data.get("lastname", ""),
            "phone": data.get("phone", ""),
            "email": data.get("email", ""),
            "losses": data.get("losses", ""),
            "start_date": data.get("start_date", ""),
            "last_contact": data.get("last_contact", ""),
            "other_lawyers": data.get("other_lawyers", ""),

            # обязательные для CRM
            "geo": "RU",
            "landing": "https://yrkaais.onrender.com",
            "ip": ip,
            "offer": 128   # ← КРИТИЧЕСКИ ВАЖНО: ID оффера вместо funnel
        }

        CRM_URL = "https://dmtraff.com/api/ext/add.json?id=119-88190c469be217ca48cb158d411b262d"

        response = requests.post(CRM_URL, data=payload)

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