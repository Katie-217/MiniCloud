import requests
from lab import save, result

checks = []
for headers in ({}, {"Authorization": "Bearer invalid-demo-token"}):
    response = requests.get("http://localhost:8085/secure", headers=headers, timeout=10)
    assert response.status_code == 401, response.status_code
    checks.append({"case": "missing token" if not headers else "malformed token", "status": response.status_code, "body": response.json()})
evidence = save("secure-negative-cases.json", result("OIDC endpoint preparation", checks))
print("PASS: protected endpoint rejects missing/malformed tokens; E04 valid-token flow remains pending; " + evidence)
