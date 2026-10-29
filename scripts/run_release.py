"""Pull and launch the pinned local release without Flutter or source builds."""
import argparse
import os
import subprocess
import sys
import time
import requests
import json
from lab import ROOT

parser = argparse.ArgumentParser()
parser.add_argument("--verify", action="store_true", help="Run the complete UI/functional checks after startup")
args = parser.parse_args()
assert (ROOT / "docker-compose.release.yml").exists(), "Publish the release first"
os.environ["COMPOSE_FILE"] = os.pathsep.join(str(ROOT / file) for file in
    ["docker-compose.yml", "docker-compose.release.yml"])
subprocess.run([sys.executable, "scripts/setup.py"], cwd=ROOT, check=True)
subprocess.run(["docker", "compose", "config", "--quiet"], cwd=ROOT, check=True)
subprocess.run(["docker", "compose", "up", "-d", "--no-build", "--pull", "always", "--wait",
    "--wait-timeout", "240"], cwd=ROOT, check=True)
if args.verify:
    release = json.loads((ROOT / "release-images.json").read_text(encoding="utf-8"))
    tools = release["images"]["tools"]["pinned"]
    subprocess.run(["docker", "pull", tools], cwd=ROOT, check=True)
    subprocess.run(["docker", "tag", tools, "myminicloud-tools:local"], cwd=ROOT, check=True)
    # A fresh Prometheus volume needs two scrapes before rate() panels have data.
    deadline = time.monotonic() + 90
    while True:
        response = requests.get("http://127.0.0.1:9090/api/v1/query", params={
            "query": 'rate(node_cpu_seconds_total{job="node",mode="idle"}[1m])'}, timeout=10)
        if response.ok and response.json().get("data", {}).get("result"): break
        if time.monotonic() >= deadline: raise RuntimeError("Node CPU rate not ready after 90 seconds")
        time.sleep(2)
    subprocess.run([sys.executable, "scripts/check_all.py", "--screenshots"], cwd=ROOT, check=True)
    subprocess.run([sys.executable, "scripts/check_persistence.py"], cwd=ROOT, check=True)
    subprocess.run([sys.executable, "scripts/check_elearning.py"], cwd=ROOT, check=True)
    subprocess.run([sys.executable, "scripts/check_elearning_persistence.py"], cwd=ROOT, check=True)
    subprocess.run([sys.executable, "scripts/check_logging.py", "--recreate"], cwd=ROOT, check=True)
print("Pinned local release ready: http://localhost/ and http://localhost/elearning/")
