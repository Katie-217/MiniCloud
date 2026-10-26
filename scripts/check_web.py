"""Verify static routes and capture real HTTP evidence."""
import argparse
import requests
from lab import save, result
from progress import set_status

parser = argparse.ArgumentParser()
parser.add_argument("--blog", action="store_true")
args = parser.parse_args()
routes = [("/", "MyMiniCloud – Home")]
if args.blog:
    routes.append(("/blog/", "MyMiniCloud – Blog"))
checks = []
for path, expected in routes:
    response = requests.get("http://localhost:8080" + path, timeout=10)
    response.encoding = "utf-8"
    assert response.status_code == 200, (path, response.status_code)
    assert expected in response.text, path
    checks.append({"path": path, "status": response.status_code, "expected_text": expected, "body": response.text})
evidence = save("R02-web.json", result("R02", checks))
set_status("R02", "DAT" if args.blog else "CHO_KIEM_THU", evidence + ("; Home + Blog" if args.blog else "; Home đạt, Blog chưa làm"))
print(f"PASS: {len(checks)} static routes; {evidence}")
