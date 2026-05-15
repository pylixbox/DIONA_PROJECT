from flask import Flask, request, jsonify
from flask_cors import CORS
import os
import requests
import datetime
from dotenv import load_dotenv

# Import database functions from your database.py file
from database import get_db_connection, init_db 

# 1. Load environment variables (.env)
load_dotenv()

# 2. DEFINE THE APP (This fixes the "app is not defined" error)
app = Flask(__name__)

# 3. CONFIGURE CORS (This fixes the "Backend Offline" browser error)
CORS(app, resources={r"/api/*": {"origins": "*"}})

# 4. INITIALIZE DATABASE
init_db()

# --- TIER 2 ROUTES ---

@app.route('/api/alerts', methods=['GET'])
def get_all_alerts():
    try:
        conn = get_db_connection()
        rows = conn.execute('SELECT * FROM alerts ORDER BY id DESC').fetchall()
        conn.close()
        # Convert SQLite rows to a list of dictionaries
        return jsonify([dict(row) for row in rows]), 200
    except Exception as e:
        return jsonify({"status": "Error", "message": str(e)}), 500

@app.route('/api/alert', methods=['POST'])
def receive_new_alert():
    # Force parse JSON even if headers are missing
    data = request.get_json(force=True)
    
    # Validation Logic (Proof of Integrity)
    if not data or 'ip' not in data or 'type' not in data:
        return jsonify({"status": "Error", "message": "Missing Data (ip or type)"}), 400

    attack_type = data.get('type')
    attacker_ip = data.get('ip')
    severity = data.get('severity', 'Medium')

    # Save to TIER 3 (Database)
    try:
        conn = get_db_connection()
        conn.execute('INSERT INTO alerts (attack_type, attacker_ip, severity) VALUES (?, ?, ?)',
                     (attack_type, attacker_ip, severity))
        conn.commit()
        conn.close()
        print(f"✅ Alert Logged: {attack_type} from {attacker_ip}")
    except Exception as e:
        print(f"❌ DB Storage Error: {e}")
        return jsonify({"status": "Error", "message": "DB Storage Failed"}), 500

    # --- TELEGRAM INTEROPERABILITY ---
    token = os.getenv('TELEGRAM_TOKEN')
    chat_id = os.getenv('ADMIN_CHAT_ID')
    
    if token and chat_id:
        message = (
            f"🚨 DIONA SECURITY ALERT 🚨\n"
            f"━━━━━━━━━━━━━━━━━━\n"
            f"TYPE: {attack_type}\n"
            f"SOURCE IP: {attacker_ip}\n"
            f"SEVERITY: {severity}\n"
            f"TIME: {datetime.datetime.now().strftime('%H:%M:%S')}"
        )
        
        telegram_url = f"https://api.telegram.org/bot{token}/sendMessage"
        try:
            requests.post(telegram_url, json={"chat_id": chat_id, "text": message})
            print("🚀 Telegram Alert Sent!")
        except Exception as e:
            print(f"❌ Telegram API Error: {e}")

    return jsonify({"status": "Success", "message": "Alert processed"}), 201

# --- START SERVER ---
if __name__ == "__main__":
    # Using 127.0.0.1 to match your React Dashboard config
    app.run(host='127.0.0.1', port=5000, debug=True)