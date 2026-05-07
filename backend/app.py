from flask import Flask, request, jsonify
from flask_cors import CORS
import sqlite3
import os

app = Flask(__name__)
CORS(app) # Allows React to talk to Flask

def get_db():
    return sqlite3.connect("diona_system.db")

@app.route('/api/alert', methods=['POST'])
def receive_alert():
    data = request.get_json(force=True)
    # LOGIC: Validation (Proof of Data Integrity)
    if not data or 'ip' not in data:
        return jsonify({"status": "Error", "message": "Missing IP"}), 400

    # LOGIC: Save to Tier 3
    conn = get_db()
    conn.execute("INSERT INTO alerts (attack_type, attacker_ip, severity) VALUES (?, ?, ?)",
                 (data.get('type'), data.get('ip'), data.get('severity')))
    conn.commit()
    conn.close()
    return jsonify({"status": "Success", "message": "Logged to Tier 3"}), 201

@app.route('/api/alerts', methods=['GET'])
def send_to_dashboard():
    conn = get_db()
    conn.row_factory = sqlite3.Row
    rows = conn.execute("SELECT * FROM alerts ORDER BY id DESC").fetchall()
    conn.close()
    return jsonify([dict(ix) for ix in rows])

if __name__ == "__main__":
    app.run(port=5000, debug=True)