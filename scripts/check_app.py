import argparse
import requests
from lab import save, result
from progress import set_status

parser = argparse.ArgumentParser()
parser.add_argument("--proxy", action="store_true")
args = parser.parse_args()
urls = ["http://localhost:8085/hello"]
if args.proxy:
    urls.append("http://localhost/api/hello")
checks = []
for url in urls:
    response = requests.get(url, timeout=10)
    assert response.status_code == 200, (url, response.status_code)
    assert response.json() == {"message": "Hello from App Server!"}
    checks.append({"url": url, "status": response.status_code, "json": response.json()})
evidence = save("R03-api.json", result("R03", checks))
set_status("R03", "DAT" if args.proxy else "CHO_KIEM_THU", evidence + ("; direct + proxy" if args.proxy else "; direct đạt, chờ proxy"))
print(f"PASS: {len(checks)} API paths; {evidence}")
