from playwright.sync_api import sync_playwright
from browser import launch
from lab import config, EVIDENCE
from progress import set_status

cfg = config()
with sync_playwright() as p:
    browser = launch(p)
    page = browser.new_page(viewport={"width": 1440, "height": 1000})
    page.goto("http://localhost:9001/")
    page.locator("#accessKey").fill(cfg["MINIO_ROOT_USER"])
    page.locator("#secretKey").fill(cfg["MINIO_ROOT_PASSWORD"])
    page.get_by_role("button", name="Login", exact=True).click()
    bucket = page.get_by_text("demo", exact=True).first
    bucket.wait_for(timeout=30000)
    page.screenshot(path=str(EVIDENCE / "R06-minio-bucket.png"), full_page=True)
    bucket.click()
    page.get_by_text("index.html", exact=True).first.wait_for(timeout=30000)
    page.screenshot(path=str(EVIDENCE / "R06-minio-object.png"), full_page=True)
    browser.close()
set_status("R06", "DAT", "evidence/local/R06-storage.json; R06-minio-bucket.png; R06-minio-object.png")
print("PASS: MinIO Console login, bucket and object visible.")
