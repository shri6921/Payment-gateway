from flask import Flask, render_template, request, jsonify
import requests
import os
from dotenv import load_dotenv

load_dotenv()

app = Flask(__name__)

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/create_payment', methods=['POST'])
def create_payment():
    data = request.get_json()
    customer_name = data.get('name')
    customer_email = data.get('email')
    amount = data.get('amount')

    url = "https://sandbox.cashfree.com/pg/orders"
    headers = {
        "x-api-version": "2022-09-01",
        "Content-Type": "application/json",
        "x-client-id": os.getenv("APP_ID"),
        "x-client-secret": os.getenv("SECRET_KEY")
    }
    payload = {
        "order_amount": amount,
        "order_currency": "INR",
        "customer_details": {
            "customer_id": "cust001",
            "customer_email": customer_email,
            "customer_name": customer_name,
        }
    }

    response = requests.post(url, json=payload, headers=headers)
    return jsonify(response.json())

@app.route('/webhook', methods=['POST'])
def webhook():
    data = request.json
    print("Webhook received:", data)
    # You can log or store this info in DB
    return '', 200

if __name__ == '__main__':
    app.run(debug=True)
