from playwright.sync_api import sync_playwright
from browser import launch
from lab import config, EVIDENCE
from progress import set_status
import argparse

cfg = config()
parser = argparse.ArgumentParser()
parser.add_argument("--proxy", action="store_true")
args = parser.parse_args()
base = "http://localhost/auth" if args.proxy else "http://localhost:8081/auth"
prefix = "R10" if args.proxy else "R05"
EVIDENCE.mkdir(parents=True, exist_ok=True)
with sync_playwright() as p:
    browser = launch(p)
    page = browser.new_page(viewport={"width": 1440, "height": 1000})
    page.goto(base + "/admin/master/console/")
    page.locator("#username").fill(cfg["KEYCLOAK_ADMIN"])
    page.locator("#password").fill(cfg["KEYCLOAK_ADMIN_PASSWORD"])
    page.locator("#kc-login").click()
    page.get_by_role("link", name="Users", exact=True).wait_for(timeout=60000)
    page.screenshot(path=str(EVIDENCE / f"{prefix}-keycloak-admin.png"), full_page=True)
    page.get_by_role("link", name="Users", exact=True).click()
    page.get_by_text("sv01", exact=True).first.wait_for(timeout=30000)
    page.screenshot(path=str(EVIDENCE / f"{prefix}-keycloak-user.png"), full_page=True)
    browser.close()
set_status("R05", "DAT", "evidence/local/R05-auth.json; R05-keycloak-admin.png; R05-keycloak-user.png")
print("PASS: browser admin login and sv01 visible; screenshots saved.")
