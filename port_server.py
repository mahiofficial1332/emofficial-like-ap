# port_server.py
from flask import Flask
import os

app = Flask(__name__)

@app.route("/")
def home():
    return "✅ Flask Web Server Running!"

def run_server():
    port = int(os.getenv("PORT", 5000))
    app.run(host="0.0.0.0", port=port)
