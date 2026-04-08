from flask import Flask, request, jsonify
from core.engine import Engine

app = Flask(__name__)

@app.route("/event", methods=["POST"])
def event():
    data = request.json
    
    tenant = data["tenant"]
    event_name = data["event"]
    payload = data.get("payload", {})

    store = Engine(tenant)
    store.handle_event(event_name, payload)

    return jsonify({"status": "ok"})

if __name__ == "__main__":
    app.run(port=6000)