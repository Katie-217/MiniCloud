import re
from playwright.sync_api import sync_playwright
from browser import launch
from lab import config, EVIDENCE
from progress import set_status

cfg = config()
with sync_playwright() as p:
    browser = launch(p)
    page = browser.new_page(viewport={"width": 1600, "height": 1100})
    page.goto("http://localhost:9090/targets")
    page.get_by_text("monitoring-node-exporter-server:9100", exact=False).first.wait_for(timeout=30000)
    page.screenshot(path=str(EVIDENCE / "R08-prometheus-targets.png"), full_page=True)
    page.goto("http://localhost:9090/query?g0.expr=node_cpu_seconds_total&g0.tab=1")
    page.wait_for_timeout(2000)
    page.screenshot(path=str(EVIDENCE / "R08-prometheus-query.png"), full_page=True)
    page.goto("http://localhost:3000/login")
    page.locator('input[name="user"]').fill(cfg["GRAFANA_ADMIN_USER"])
    page.locator('input[name="password"]').fill(cfg["GRAFANA_ADMIN_PASSWORD"])
    page.get_by_role("button", name=re.compile("log in|sign in", re.I)).click()
    page.wait_for_url(lambda url: "/login" not in url, timeout=30000)
    url = "http://localhost:3000/d/node-exporter-full/node-exporter-full?orgId=1&from=now-15m&to=now&var-datasource=prometheus&var-job=node&var-node=monitoring-node-exporter-server:9100"
    page.goto(url)
    page.get_by_text("CPU Busy", exact=True).first.wait_for(timeout=30000)
    page.wait_for_timeout(4000)
    page.screenshot(path=str(EVIDENCE / "R09-grafana-dashboard.png"), full_page=True)
    page.goto(url + "&viewPanel=74")
    page.wait_for_timeout(3000)
    page.screenshot(path=str(EVIDENCE / "R09-grafana-network.png"), full_page=True)
    browser.close()
set_status("R09", "DAT", "evidence/local/R09-grafana.json; R09-grafana-dashboard.png; R09-grafana-network.png")
print("PASS: Prometheus and Grafana browser screenshots saved; inspect images for visual verification.")
