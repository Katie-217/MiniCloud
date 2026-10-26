import requests
from lab import save, result
from progress import set_status

checks = []
for path in ["/", "/blog/", "/api/hello", "/api/notes"]:
    response = requests.get("http://localhost" + path, timeout=15)
    assert response.status_code == 200, (path, response.status_code)
    checks.append({"path": path, "status": response.status_code, "content_type": response.headers.get("Content-Type")})
response = requests.get("http://localhost/auth/", allow_redirects=False, timeout=15)
assert response.status_code == 302, (response.status_code, response.headers)
checks.append({"path": "/auth/", "status": response.status_code, "location": response.headers["Location"]})
response = requests.get("http://localhost/auth/admin/master/console/", timeout=15)
assert response.status_code == 200 and "Keycloak" in response.text
discovery = requests.get("http://localhost/auth/realms/master/.well-known/openid-configuration", timeout=15).json()
assert discovery["issuer"] == "http://localhost/auth/realms/master", discovery["issuer"]
checks.append({"oidc_issuer": discovery["issuer"], "token_endpoint": discovery["token_endpoint"]})
evidence = save("R10-gateway.json", result("R10", checks))
set_status("R10", "DAT", evidence + "; Web/App/Auth + correct public OIDC issuer")
print("PASS: unified web/API/auth routes and issuer; " + evidence)
