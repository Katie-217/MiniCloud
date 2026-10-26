"""Run functional integration checks; does not remove containers or volumes."""
import argparse
import subprocess
import sys
from pathlib import Path

parser = argparse.ArgumentParser()
parser.add_argument("--screenshots", action="store_true")
args = parser.parse_args()
root = Path(__file__).resolve().parents[1]
checks = [
    ["check_web.py", "--blog"], ["check_app.py", "--proxy"], ["check_database.py"],
    ["check_app_database.py"], ["check_auth.py"], ["check_secure.py"], ["check_storage.py"],
    ["check_dns.py"], ["check_monitoring.py"], ["check_grafana.py"], ["check_gateway.py"],
    ["check_stack.py"], ["check_network.py"],
]
if args.screenshots:
    checks.extend([["capture_auth.py", "--proxy"], ["capture_storage.py"], ["capture_monitoring.py"]])
for check in checks:
    subprocess.run([sys.executable, str(root / "scripts" / check[0]), *check[1:]], cwd=root, check=True)
print("All requested local checks passed.")
