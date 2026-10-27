"""Verify E07: Prometheus scraping Web server with real Nginx metrics."""
import time
import requests
from playwright.sync_api import sync_playwright

from browser import launch
from lab import ROOT, EVIDENCE, save, result
from progress import set_status

prom_url = "http://localhost:9090"

# Generate traffic to Web server
for _ in range(5):
    requests.get("http://localhost:8080/", timeout=5)
    requests.get("http://localhost:8080/blog/", timeout=5)

time.sleep(2)

def query(expr):
    res = requests.get(f"{prom_url}/api/v1/query", params={"query": expr}, timeout=10)
    res.raise_for_status()
    data = res.json()["data"]["result"]
    assert len(data) > 0, f"Query '{expr}' returned no results"
    return data[0]["value"][1]

up_val = query('up{job="web"}')
nginx_up_val = query('nginx_up{job="web"}')
requests_val = query('nginx_http_requests_total{job="web"}')

assert up_val == "1", f"Expected up{{job='web'}} == 1, got {up_val}"
assert nginx_up_val == "1", f"Expected nginx_up{{job='web'}} == 1, got {nginx_up_val}"

targets_res = requests.get(f"{prom_url}/api/v1/targets", timeout=10).json()
active_targets = targets_res["data"]["activeTargets"]
web_target = next((t for t in active_targets if t["labels"].get("job") == "web"), None)
assert web_target is not None, "Web target not found in active targets"
assert web_target["health"] == "up", f"Web target health is {web_target['health']}"

# Screenshots via Playwright
EVIDENCE.mkdir(parents=True, exist_ok=True)
with sync_playwright() as p:
    browser = launch(p)
    page = browser.new_page(viewport={"width": 1600, "height": 1100})

    # Targets page
    page.goto(f"{prom_url}/targets")
    page.get_by_text("web-frontend-server:80", exact=False).first.wait_for(timeout=30000)
    page.wait_for_timeout(2000)
    page.screenshot(path=str(EVIDENCE / "E07-web-targets.png"), full_page=True)

    # Query page querying nginx_up
    page.goto(f"{prom_url}/query?g0.expr=nginx_up%7Bjob%3D%22web%22%7D&g0.tab=1")
    page.wait_for_timeout(3000)
    page.screenshot(path=str(EVIDENCE / "E07-web-metrics.png"), full_page=True)

    browser.close()

details = {
    "job": "web",
    "target": "web-frontend-server:80",
    "health": "up",
    "up": up_val,
    "nginx_up": nginx_up_val,
    "requests_total": requests_val,
    "scrape_url": web_target["scrapeUrl"]
}

path = save("E07-web-metrics.json", result("E07", details))
set_status("E07", "DAT", f"{path}; feat/web-metrics; python scripts/check_web_metrics.py; E07-web-targets.png; E07-web-metrics.png")
print("PASS E07: web target is UP (1) with real nginx_up metric, Prometheus targets and graph screenshots captured.")
