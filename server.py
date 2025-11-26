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

        # Получаем IP клиента
        forwarded = request.headers.get("X-Forwarded-For", "")
        ip = forwarded.split(",")[0] if forwarded else request.remote_addr

        # Формируем comment из 4 полей
        comment = (
            "1. Как давно начали работать с брокером?\n- " + data.get("start_date", "") + "\n\n"
            "2. Когда у вас был последний контакт с брокером?\n- " + data.get("last_contact", "") + "\n\n"
            "3. Обращались ли вы уже к юристам?\n- " + data.get("other_lawyers", "") + "\n\n"
            "4. Сумма потери ваших личных средств?\n- " + data.get("losses", "")
        )

        # Финальный payload
        payload = {
            "name": data.get("name", ""),
            "lastname": data.get("lastname", ""),
            "phone": data.get("phone", ""),
            "email": data.get("email", ""),
            "geo": "RU",
            "offer_id": 128,
            "ip": ip,
            "comment": comment
        }

        # ⚠️ ВАЖНО: landing НЕ отправляем!
        # payload["landing"] = "..."  ← ЭТО УДАЛЕНО

        CRM_URL = "https://dmtraff.com/api/ext/add.json?id=119-88190c469be217ca48cb158d411b262d"

        response = requests.post(CRM_URL, data=payload, timeout=20)

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