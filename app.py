from flask import Flask, jsonify
import os
import requests
from dotenv import load_dotenv

load_dotenv()
app = Flask(__name__)

@app.route('/')
def wake():
    token = os.getenv("RAILWAY_TOKEN")
    project_id = os.getenv("RAILWAY_PROJECT_ID")
    service_name = os.getenv("RAILWAY_SERVICE_NAME")

    url = f"https://backboard.railway.app/project/{project_id}/service/{service_name}/deploy"
    headers = {
        "Authorization": f"Bearer {token}",
        "Content-Type": "application/json"
    }

    res = requests.post(url, headers=headers)
    if res.status_code == 200:
        return jsonify({"message": "🚀 Bot is waking up!"})
    else:
        return jsonify({"error": "❌ Failed to trigger deploy", "status": res.status_code}), 500

if __name__ == '__main__':
    app.run()
