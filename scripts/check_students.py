"""Verify the packaged student fixture directly and through the gateway."""
import json
import requests
from lab import ROOT, save, result
from progress import set_status

expected = json.loads((ROOT / "application-backend-server/students.json").read_text(encoding="utf-8"))
assert len(expected) == 5 and len({row["id"] for row in expected}) == 5
assert all(set(row) == {"id", "name", "major", "gpa"} and 0 <= row["gpa"] <= 4 for row in expected)
checks = []
for url in ("http://localhost:8085/student", "http://localhost/api/student"):
    response = requests.get(url, timeout=10)
    assert response.status_code == 200 and response.json() == expected, (url, response.status_code)
    checks.append({"url": url, "status": response.status_code, "students": response.json()})
path = save("E02-student-api.json", result("E02", {"checks": checks, "data_is_synthetic": True}))
set_status("E02", "DAT", path + "; feat/student-json-api; python scripts/check_students.py")
print("PASS E02: five packaged students, direct and gateway responses match.")
