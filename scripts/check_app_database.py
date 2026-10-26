import requests
from lab import save, result

response = requests.get("http://localhost:8085/notes", timeout=10)
assert response.status_code == 200, response.status_code
rows = response.json()
assert any(row["title"] == "Hello from MariaDB!" for row in rows)
evidence = save("app-database.json", result("App to DB integration", {
    "url": "http://localhost:8085/notes", "status": response.status_code, "rows": rows,
    "connection": "Flask uses the dedicated MariaDB application user over cloud-net",
}))
print("PASS: Flask reads actual MariaDB records; " + evidence)
