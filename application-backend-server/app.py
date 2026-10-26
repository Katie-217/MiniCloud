"""MyMiniCloud application server."""
from flask import Flask, jsonify
import os
import pymysql

app = Flask(__name__)

@app.get("/hello")
def hello():
    return jsonify(message="Hello from App Server!")

@app.get("/healthz")
def health():
    return jsonify(status="ok")

@app.get("/notes")
def notes():
    try:
        with pymysql.connect(
            host=os.environ["DB_HOST"], user=os.environ["DB_USER"],
            password=os.environ["DB_PASSWORD"], database="minicloud",
            connect_timeout=5, read_timeout=5,
            cursorclass=pymysql.cursors.DictCursor,
        ) as connection:
            with connection.cursor() as cursor:
                cursor.execute("SELECT id, title FROM notes ORDER BY id")
                return jsonify(cursor.fetchall())
    except pymysql.MySQLError:
        app.logger.exception("Database query failed")
        return jsonify(error="Database unavailable"), 503
