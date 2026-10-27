import requests
from lab import save, result
from progress import set_status

response = requests.get("http://localhost/student/", timeout=10)
reference = requests.get("http://localhost/api/student", timeout=10)
assert response.status_code == reference.status_code == 200
assert response.json() == reference.json() and len(response.json()) == 5
path = save("E09-student-proxy.json", result("E09", {
    "url": response.url, "status": response.status_code, "json": response.json(),
    "matches_api_student": True,
}))
set_status("E09", "DAT", path + "; feat/student-proxy-route; python scripts/check_student_proxy.py")
print("PASS E09: /student/ matches the five-student Flask response.")
