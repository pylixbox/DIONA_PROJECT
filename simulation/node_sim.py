import requests
import time
import random

def trigger_mock_detection():
    # Mimics Snort seeing an attack
    payload = {
        "type": random.choice(["Port Scan", "Brute Force"]),
        "ip": f"192.168.1.{random.randint(2, 254)}",
        "severity": "High"
    }
    try:
        r = requests.post("http://localhost:5000/api/alert", json=payload)
        print(f"Mock Node: Alert Sent! Status: {r.status_code}")
    except:
        print("Error: Logic Hub (Backend) is offline.")

while True:
    trigger_mock_detection()
    time.sleep(10) # Sends an attack every 10 seconds