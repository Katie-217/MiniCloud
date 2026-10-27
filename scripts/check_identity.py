"""Provision the coursework realm and exercise signed token acceptance/rejection.

Only managed lab users are reset; credentials stay in .env, never in evidence.
"""
import copy
import json
import time
import requests
from lab import ROOT, config, save, result
from progress import set_status

cfg = config()
origin = cfg.get("PUBLIC_ORIGIN", "http://localhost").rstrip("/")
base = origin + "/auth"
realm = cfg.get("OIDC_REALM", "realm_521H0092")
response = requests.post(base + "/realms/master/protocol/openid-connect/token", data={
    "client_id": "admin-cli", "grant_type": "password", "username": cfg["KEYCLOAK_ADMIN"],
    "password": cfg["KEYCLOAK_ADMIN_PASSWORD"],
}, timeout=20)
response.raise_for_status()
admin = requests.Session()
admin.headers["Authorization"] = "Bearer " + response.json()["access_token"]
admin_base = base + "/admin/realms/" + realm

def call(method, path, **kwargs):
    response = admin.request(method, admin_base + path, timeout=20, **kwargs)
    response.raise_for_status()
    return response

template = json.loads((ROOT / "authentication-identity-server/realm-template.json").read_text(encoding="utf-8"))
template["realm"] = realm
template["clients"][0].update(redirectUris=[origin + "/*"], webOrigins=[origin])
response = admin.get(admin_base, timeout=20)
if response.status_code == 404:
    response = admin.post(base + "/admin/realms", json=template, timeout=20)
response.raise_for_status()

client = template["clients"][0]
clients = call("GET", "/clients", params={"clientId": "flask-app"}).json()
if not clients:
    call("POST", "/clients", json=client)
    clients = call("GET", "/clients", params={"clientId": "flask-app"}).json()
client_path = "/clients/" + clients[0]["id"]
call("PUT", client_path, json=client)
mappers = call("GET", client_path + "/protocol-mappers/models").json()
if not any(mapper["name"] == "flask-api-audience" for mapper in mappers):
    call("POST", client_path + "/protocol-mappers/models", json=client["protocolMappers"][0])

for username in ("sv01", "sv02"):
    profile = {"username": username, "enabled": True, "emailVerified": True,
        "email": username + "@example.test", "firstName": "Student", "lastName": username,
        "requiredActions": []}
    users = call("GET", "/users", params={"username": username, "exact": "true"}).json()
    if not users:
        call("POST", "/users", json=profile)
        users = call("GET", "/users", params={"username": username, "exact": "true"}).json()
    user_path = "/users/" + users[0]["id"]
    call("PUT", user_path, json=profile)
    call("PUT", user_path + "/reset-password", json={
        "type": "password", "value": cfg["KEYCLOAK_TEST_PASSWORD"], "temporary": False})

discovery = requests.get(base + "/realms/" + realm + "/.well-known/openid-configuration", timeout=15).json()
assert discovery["issuer"] == base + "/realms/" + realm

def token(username="sv01", client_id="flask-app"):
    response = requests.post(discovery["token_endpoint"], data={
        "grant_type": "password", "client_id": client_id, "username": username,
        "password": cfg["KEYCLOAK_TEST_PASSWORD"],
    }, timeout=20)
    response.raise_for_status()
    return response.json()["access_token"]

def secure(access_token=None):
    headers = {"Authorization": "Bearer " + access_token} if access_token else {}
    return requests.get(origin + "/api/secure", headers=headers, timeout=15)

checks = []
for username in ("sv01", "sv02"):
    response = secure(token(username))
    assert response.status_code == 200, (username, response.status_code, response.text)
    assert response.json() == {"message": "Secure resource OK", "preferred_username": username}
    checks.append({"case": "valid_" + username, "status": 200, "response": response.json()})
for case, value in (("missing", None), ("malformed", "invalid.token.value")):
    response = secure(value)
    assert response.status_code == 401
    checks.append({"case": case, "status": response.status_code})

# Real signed token with the wrong audience, then remove the temporary test client.
wrong_id = "minicloud-negative-audience-test"
existing = call("GET", "/clients", params={"clientId": wrong_id}).json()
assert not existing, "Temporary test client already exists; inspect it before reuse"
call("POST", "/clients", json={"clientId": wrong_id, "publicClient": True,
    "protocol": "openid-connect", "directAccessGrantsEnabled": True})
temporary_id = call("GET", "/clients", params={"clientId": wrong_id}).json()[0]["id"]
try:
    response = secure(token(client_id=wrong_id))
    assert response.status_code == 401
    checks.append({"case": "wrong_audience_signed", "status": 401})
finally:
    call("DELETE", "/clients/" + temporary_id)

# Briefly shorten only the managed client lifespan; always restore its configuration.
short_client = copy.deepcopy(client)
short_client["attributes"] = {"access.token.lifespan": "2"}
try:
    call("PUT", client_path, json=short_client)
    expired_token = token()
    time.sleep(3)
    response = secure(expired_token)
    assert response.status_code == 401, response.status_code
    checks.append({"case": "expired_signed", "status": 401})
finally:
    call("PUT", client_path, json=client)

path = save("E04-keycloak.json", result("E04", {"realm": realm,
    "users": ["sv01", "sv02"], "public_client": "flask-app", "issuer": discovery["issuer"],
    "token_endpoint": discovery["token_endpoint"], "checks": checks, "secrets": "omitted",
    "reproduction": "realm-template.json plus this script; passwords from ignored .env"}))
set_status("E04", "DAT", path + "; feat/student-identity; python scripts/check_identity.py")
print("PASS E04: two users accepted; missing, malformed, wrong audience and expired tokens rejected.")
