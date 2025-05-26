from flask import Flask, jsonify
import os
import requests
from dotenv import load_dotenv

load_dotenv()
app = Flask(__name__)

@app.route('/')
def wake():
    token = os.getenv("RAILWAY_TOKEN")
    account_token = os.getenv("RAILWAY_PERSONAL_TOKEN")
    service_id = os.getenv("RAILWAY_SERVICE_ID")
    environment_id = os.getenv("RAILWAY_ENVIRONMENT_ID")

    if not token or not service_id or not environment_id:
        return jsonify({
            "error": "Missing required environment variables. Please set RAILWAY_TOKEN, RAILWAY_SERVICE_ID, and RAILWAY_ENVIRONMENT_ID."
        }), 400

    url = "https://backboard.railway.app/graphql/v2"
    headers = {
        # "Authorization": f"Project-Access-Token: {token}",
        "Authorization": f"Bearer {account_token}",
        "Content-Type": "application/json"
    }

    query = """
    mutation serviceInstanceRedeploy($environmentId: String!, $serviceId: String!) {
        serviceInstanceRedeploy(environmentId: $environmentId, serviceId: $serviceId)
    }
    """

    variables = {
	    "serviceId": service_id,
        "environmentId": environment_id,
    }
    try:
        response = requests.post(url, headers=headers, json={"query": query, "variables": variables}, timeout=10)
        response.raise_for_status()
        data = response.json()
    except Exception as e:
        return jsonify({
            "error": "Request to Railway API failed.",
            "details": str(e)
        }), 502

    if "errors" in data:
        return jsonify({
            "error": "Railway API returned errors.",
            "details": data["errors"]
        }), 502
    if not data.get("data", {}).get("serviceInstanceRedeploy"):
        return jsonify({
            "error": "Service redeployment failed or returned no result.",
            "details": data
        }), 500
    return jsonify({
        "message": "Service redeployment initiated successfully.",
        "data": data
    }), 200

if __name__ == '__main__':
    port = int(os.environ.get('PORT', 5000))
    app.run(host='0.0.0.0', port=port)
