from flask import Flask, request
import requests

app = Flask(__name__)

FAZER_API_KEY = "fc_f4406b74730011bb6f2a6ec2"
DIGI_API_KEY = "0E37AD25107B4385B6402A7D4259B9FF"

# استقبال الطلب
@app.route('/digi', methods=['POST'])
def digi():
    data = request.json

    amount = data.get("quantity")
    order_id = data.get("order_id")

    # شراء من fazercards
    r = requests.post(
        "https://api.fzr.cards/api/v2/steam-topup/order",
        json={"amount": amount, "currency": "RUB"},
        headers={"X-API-Key": FAZER_API_KEY}
    )

    return {"ok": True}


# استقبال الكود
@app.route('/fazer', methods=['POST'])
def fazer():
    data = request.json

    if data.get("status") == "completed":
        code = data.get("code")
        order_id = data.get("order_id")

        # ارسال للزبون
        requests.post(
            "https://api.digiseller.com/api/seller/deliver",
            json={
                "token": DIGI_API_KEY,
                "order_id": order_id,
                "text": code
            }
        )

    return {"ok": True}


app.run(host="0.0.0.0", port=3000)
