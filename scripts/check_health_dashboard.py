"""Verify E08: Grafana System Health of 521H0092 with 3 panels having real data."""
import re
import requests
from playwright.sync_api import sync_playwright

from browser import launch
from lab import ROOT, EVIDENCE, config, save, result
from progress import set_status

cfg = config()
admin_user = cfg["GRAFANA_ADMIN_USER"]
admin_pass = cfg["GRAFANA_ADMIN_PASSWORD"]

# Wait for Grafana to be ready
session = requests.Session()
session.auth = (admin_user, admin_pass)

resp = session.get("http://localhost:3000/api/dashboards/uid/system-health-521h0092", timeout=15)
resp.raise_for_status()
data = resp.json()["dashboard"]

assert data["title"] == "System Health of 521H0092", f"Unexpected title: {data['title']}"
panels = [p for p in data["panels"] if p.get("type") == "timeseries"]
assert len(panels) >= 3, f"Expected at least 3 timeseries panels, got {len(panels)}"

panel_titles = [p["title"] for p in panels]
assert any("CPU" in t for t in panel_titles), f"Missing CPU panel: {panel_titles}"
assert any("Memory" in t for t in panel_titles), f"Missing Memory panel: {panel_titles}"
assert any("Network" in t for t in panel_titles), f"Missing Network panel: {panel_titles}"

# Verify Prometheus metrics have real data
for panel in panels:
    expr = panel["targets"][0]["expr"]
    prom_res = requests.get("http://localhost:9090/api/v1/query", params={"query": expr}, timeout=10).json()
    assert prom_res["status"] == "success"
    assert len(prom_res["data"]["result"]) > 0, f"Expression '{expr}' returned no results"

# Playwright screenshot
EVIDENCE.mkdir(parents=True, exist_ok=True)
with sync_playwright() as p:
    browser = launch(p)
    page = browser.new_page(viewport={"width": 1600, "height": 1100})
    page.goto("http://localhost:3000/login")
    page.locator('input[name="user"]').fill(admin_user)
    page.locator('input[name="password"]').fill(admin_pass)
    page.get_by_role("button", name=re.compile("log in|sign in", re.I)).click()
    page.wait_for_url(lambda url: "/login" not in url, timeout=30000)

    url = "http://localhost:3000/d/system-health-521h0092/system-health-of-521h0092?orgId=1&from=now-15m&to=now"
    page.goto(url)
    page.get_by_text("System Health of 521H0092", exact=True).first.wait_for(timeout=30000)
    page.wait_for_timeout(4000)
    page.screenshot(path=str(EVIDENCE / "E08-system-health.png"), full_page=True)
    browser.close()

details = {
    "dashboard_title": data["title"],
    "dashboard_uid": data["uid"],
    "panels": [
        {"id": p["id"], "title": p["title"], "expr": p["targets"][0]["expr"]}
        for p in panels
    ],
    "datasource": "Prometheus",
    "verified_queries": True
}

path = save("E08-system-health.json", result("E08", details))
set_status("E08", "DAT", f"{path}; feat/personal-health-dashboard; python scripts/check_health_dashboard.py; E08-system-health.png")
print("PASS E08: System Health of 521H0092 dashboard provisioned with CPU, Memory, and Network panels; screenshot captured.")
