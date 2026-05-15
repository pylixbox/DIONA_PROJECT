import os
import requests  # This fixes the "requests is not defined" error
import datetime  # This fixes the "datetime is not defined" error
import sqlite3
from flask import Flask, request, jsonify
from flask_cors import CORS
from database import get_db_connection, init_db
from dotenv import load_dotenv

# Load your .env file
load_dotenv()

app = Flask(__name__)
CORS(app) # Allows React to talk to Flask

def get_db():
    return sqlite3.connect("diona_system.db")

@app.route('/api/alert', methods=['POST'])
@app.route('/api/alert', methods=['POST'])
def receive_new_alert():
    data = request.get_json(force=True)
    
    # ... (Your existing validation and database storage code here) ...

    # --- TELEGRAM INTEROPERABILITY LOGIC ---
    token = os.getenv('TELEGRAM_TOKEN')
    chat_id = os.getenv('ADMIN_CHAT_ID')
    
    if token and chat_id:
        message = (
            f"🚨 DIONA SECURITY ALERT 🚨\n"
            f"━━━━━━━━━━━━━━━━━━\n"
            f"TYPE: {data.get('type')}\n"
            f"SOURCE IP: {data.get('ip')}\n"
            f"SEVERITY: {data.get('severity')}\n"
            f"TIME: {datetime.datetime.now().strftime('%H:%M:%S')}"
        )
        
        telegram_url = f"https://api.telegram.org/bot"
        try:
            requests.post(telegram_url, json={"chat_id": chat_id, "text": message})
            print("🚀 Telegram Alert Disseminated!")
        except Exception as e:
            print(f"❌ Telegram Failed: {e}")

    return jsonify({"status": "Success"}), 201

if __name__ == "__main__":
    app.run(port=5000, debug=True)

    