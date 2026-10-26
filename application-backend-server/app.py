"""MyMiniCloud application server."""
from flask import Flask, jsonify

app = Flask(__name__)

@app.get("/hello")
def hello():
    return jsonify(message="Hello from App Server!")

@app.get("/healthz")
def health():
    return jsonify(status="ok")
