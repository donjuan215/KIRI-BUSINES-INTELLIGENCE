from flask import Flask, render_template
import sys
import os

# 🔥 SOLUCIÓN PATH
sys.path.append(os.path.dirname(__file__))

from core.engine import Engine

app = Flask(__name__)

# instancia del negocio
store = Engine("store_001")

@app.route("/")
def home():
    return render_template("landing.html")

@app.route("/test")
def test():
    return "OK"

if __name__ == "__main__":
    port = int(os.environ.get("PORT", 5000))
    app.run(host="0.0.0.0", port=port)