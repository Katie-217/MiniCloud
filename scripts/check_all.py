"""Run functional integration checks; does not remove containers or volumes."""
import argparse
import subprocess
import sys
from pathlib import Path

parser = argparse.ArgumentParser()
parser.add_argument("--screenshots", action="store_true")
args = parser.parse_args()
root = Path(__file__).resolve().parents[1]

# Mandatory local requirements (R01-R13)
checks = [
    ["check_web.py", "--blog"],
    ["check_app.py", "--proxy"],
    ["check_database.py"],
    ["check_app_database.py"],
    ["check_auth.py"],
    ["check_storage.py"],
    ["check_dns.py"],
    ["check_monitoring.py"],
    ["check_grafana.py"],
    ["check_gateway.py"],
    ["check_stack.py"],
    ["check_network.py"],
]

# All 10 coursework extensions (E01-E10)
extensions = [
    ["check_blog.py"],
    ["check_students.py"],
    ["check_student_database.py"],
    ["check_identity.py"],
    ["check_profile_storage.py"],
    ["check_service_dns.py"],
    ["check_web_metrics.py"],
    ["check_health_dashboard.py"],
    ["check_student_proxy.py"],
    ["check_round_robin.py"],
]

checks.extend(extensions)
checks.append(["check_secure_portal.py"])
checks.append(["check_logging.py"])

if args.screenshots:
    checks.extend([
        ["capture_auth.py", "--proxy"],
        ["capture_storage.py"],
        ["capture_monitoring.py"],
    ])

print(f"Starting test suite: {len(checks)} verification steps...")
for check in checks:
    script_name = check[0]
    print(f"--> Running {script_name}...")
    subprocess.run([sys.executable, str(root / "scripts" / script_name), *check[1:]], cwd=root, check=True)

print(f"SUCCESS: All {len(checks)} mandatory and extension checks passed completely!")
