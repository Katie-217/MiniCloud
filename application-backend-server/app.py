"""MyMiniCloud application server."""
from flask import Flask, jsonify, request
import os
import time
import pymysql
import requests
from jose import jwt, JWTError

app = Flask(__name__)
_jwks_cache = {"expires": 0, "keys": None}

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

@app.get("/secure")
def secure():
    authorization = request.headers.get("Authorization", "")
    if not authorization.startswith("Bearer "):
        return jsonify(error="Missing Bearer token"), 401
    token = authorization[7:].strip()
    try:
        jwt.get_unverified_header(token)
        if time.monotonic() >= _jwks_cache["expires"]:
            response = requests.get(os.environ["OIDC_JWKS_URL"], timeout=5)
            response.raise_for_status()
            _jwks_cache.update(keys=response.json(), expires=time.monotonic() + 600)
        payload = jwt.decode(token, _jwks_cache["keys"], algorithms=["RS256"],
            audience=os.environ["OIDC_AUDIENCE"], issuer=os.environ["OIDC_ISSUER"])
        return jsonify(message="Secure resource OK", preferred_username=payload.get("preferred_username"))
    except (JWTError, ValueError):
        return jsonify(error="Invalid access token"), 401
    except requests.RequestException:
        return jsonify(error="Identity provider unavailable"), 503
