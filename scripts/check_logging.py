"""Verify real project logs through Alloy -> Loki -> Grafana and optional persistence."""
import argparse
import re
import time
import uuid
import requests
from playwright.sync_api import sync_playwright
from browser import launch
from lab import config, run, save, result, EVIDENCE

parser = argparse.ArgumentParser()
parser.add_argument("--recreate", action="store_true")
args = parser.parse_args()
base = "http://127.0.0.1:3100"

def ready():
    deadline = time.monotonic() + 100
    while time.monotonic() < deadline:
        try:
            if requests.get(base + "/ready", timeout=5).status_code == 200: return
        except requests.RequestException: pass
        time.sleep(2)
    raise RuntimeError("Loki readiness timeout")

ready()
marker = "minicloud-log-check-" + uuid.uuid4().hex[:12]
response = requests.get("http://localhost/api/hello", params={"log_check": marker}, timeout=10)
assert response.status_code == 200
query = '{project="myminicloud",service="application-backend-server"} |= "' + marker + '"'
params = {"query": query, "start": str(int((time.time()-300)*1e9)), "limit": "20"}

def marker_logs():
    response = requests.get(base + "/loki/api/v1/query_range", params=params, timeout=15)
    response.raise_for_status()
    rows = response.json().get("data", {}).get("result", [])
    return [line for row in rows for _, line in row.get("values", []) if marker in line]

deadline = time.monotonic() + 90
lines = []
while time.monotonic() < deadline:
    lines = marker_logs()
    if lines: break
    time.sleep(2)
assert lines, "Marker never reached Loki from application access logs"
recreated = False
if args.recreate:
    before = run("docker", "inspect", "logging-loki-server", "--format", "{{.Id}}")
    run("docker", "compose", "up", "-d", "--no-deps", "--force-recreate", "logging-loki-server")
    ready()
    assert run("docker", "inspect", "logging-loki-server", "--format", "{{.Id}}") != before
    assert marker_logs(), "Stored log marker did not survive Loki recreation"
    recreated = True

cfg = config()
session = requests.Session()
session.auth = (cfg["GRAFANA_ADMIN_USER"], cfg["GRAFANA_ADMIN_PASSWORD"])
response = session.get("http://localhost:3000/api/datasources/uid/loki/health", timeout=15)
response.raise_for_status()
assert response.json()["status"] == "OK", response.json()
response = session.get("http://localhost:3000/api/datasources/proxy/uid/loki/loki/api/v1/query_range", params=params, timeout=15)
response.raise_for_status()
assert any(marker in line for row in response.json()["data"]["result"] for _, line in row["values"])
series = requests.get(base + "/loki/api/v1/series", params={"match[]": '{project="myminicloud"}'}, timeout=15).json()["data"]
services = set(run("docker", "compose", "config", "--services").splitlines())
assert series and all(row.get("project") == "myminicloud" and row.get("service") in services for row in series)
with sync_playwright() as p:
    browser = launch(p)
    page = browser.new_page(viewport={"width":1600,"height":1100})
    page.goto("http://localhost:3000/login")
    page.locator('input[name="user"]').fill(cfg["GRAFANA_ADMIN_USER"])
    page.locator('input[name="password"]').fill(cfg["GRAFANA_ADMIN_PASSWORD"])
    page.get_by_role("button", name=re.compile("log in|sign in", re.I)).click()
    page.wait_for_url(lambda url: "/login" not in url, timeout=30000)
    page.goto("http://localhost:3000/d/minicloud-service-logs/myminicloud-service-logs?from=now-15m&to=now")
    page.get_by_text("Application server access logs", exact=True).first.wait_for(timeout=30000)
    page.get_by_text(re.compile(re.escape(marker))).first.wait_for(timeout=30000)
    page.screenshot(path=str(EVIDENCE / "logging-grafana.png"), full_page=True)
    browser.close()
path = save("service-logging.json", result("Centralized service logging", {
    "query": query, "marker": marker, "log_lines": lines,
    "grafana_datasource_health": "OK", "grafana_proxy_query": "successful",
    "only_project_streams_observed": True, "stream_service_labels": sorted({row["service"] for row in series}),
    "verified_after_loki_recreation": recreated, "collection_scope": "myminicloud only",
    "dashboard": "http://localhost:3000/d/minicloud-service-logs/myminicloud-service-logs",
}))
print("PASS logging: real request log in Loki and Grafana UI; project filter verified; " + path)
