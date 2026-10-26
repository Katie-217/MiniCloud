"""Log in as administrator and idempotently create the required test user."""
import requests
from lab import config, save, result
from progress import set_status

cfg = config()
base = "http://localhost:8081/auth"
response = requests.post(base + "/realms/master/protocol/openid-connect/token", data={
    "client_id": "admin-cli", "grant_type": "password",
    "username": cfg["KEYCLOAK_ADMIN"], "password": cfg["KEYCLOAK_ADMIN_PASSWORD"],
}, timeout=20)
response.raise_for_status()
session = requests.Session()
session.headers["Authorization"] = "Bearer " + response.json()["access_token"]
users = base + "/admin/realms/master/users"
response = session.get(users, params={"username": "sv01", "exact": "true"}, timeout=15)
response.raise_for_status()
matches = response.json()
if not matches:
    response = session.post(users, json={
        "username": "sv01", "enabled": True, "firstName": "Sinh viên", "lastName": "01",
        "credentials": [{"type": "password", "value": cfg["KEYCLOAK_TEST_PASSWORD"], "temporary": False}],
    }, timeout=15)
    response.raise_for_status()
response = session.get(users, params={"username": "sv01", "exact": "true"}, timeout=15)
response.raise_for_status()
assert response.json()[0]["enabled"]
evidence = save("R05-auth.json", result("R05", {
    "admin_login": "successful", "realm": "master", "user": "sv01", "enabled": True,
    "admin_console": base + "/admin/master/console/", "secrets": "omitted",
}))
set_status("R05", "DAT", evidence + "; admin token login + created sv01; UI screenshot captured later")
print("PASS: administrator login and required test user; " + evidence)
