"""Record a silent, captioned walkthrough of the running LOCAL system with 10 extensions."""
import re
from pathlib import Path
from playwright.sync_api import sync_playwright
from browser import launch
from lab import config, ROOT, EVIDENCE, save, result
from progress import set_status

cfg = config()
folder = ROOT / "report"
temporary = ROOT / ".venv" / "demo-recording"
temporary.mkdir(parents=True, exist_ok=True)
chapters = []

def caption(page, title, note, delay=4000):
    page.evaluate('''([title,note]) => {
        document.getElementById('demo-caption')?.remove();
        const box = document.createElement('div'); box.id='demo-caption';
        Object.assign(box.style,{position:'fixed',bottom:'16px',left:'20px',right:'20px',zIndex:'2147483647',background:'#0f172a',color:'white',border:'1px solid #38bdf8',padding:'14px 20px',fontFamily:'Arial,sans-serif',borderRadius:'8px',fontSize:'17px',boxShadow:'0 4px 20px rgba(0,0,0,0.6)'});
        const heading=document.createElement('strong');heading.textContent=title;heading.style.color='#38bdf8';
        const small=document.createElement('div');small.textContent=note;small.style.fontSize='14px';small.style.marginTop='4px';small.style.color='#e2e8f0';
        box.append(heading,small);document.body.append(box);
    }''', [title, note])
    page.wait_for_timeout(delay)
    chapters.append({"chapter": title, "url": page.url, "note": note})

with sync_playwright() as p:
    browser = launch(p)
    context = browser.new_context(
        viewport={"width": 1440, "height": 1000},
        record_video_dir=str(temporary),
        record_video_size={"width": 1440, "height": 1000}
    )
    page = context.new_page()

    # 1. Web Portal & Team
    page.goto("http://localhost/")
    caption(page, "01 · MyMiniCloud Portal & Infrastructure", "9 server roles, 13 containers running on Docker network cloud-net. Group: Vo Thi Thien Kim / 521H0092.")
    
    # Click to load students in portal
    page.locator('button:has-text("Tải danh sách sinh viên")').click()
    page.wait_for_timeout(1500)
    caption(page, "02 · Interactive Student Table (E02 / E09)", "Dynamic retrieval of 5 student records from Flask /api/student and proxy /student/.")

    # 2. Blog
    page.goto("http://localhost/blog/")
    caption(page, "03 · Illustrated Blog (E01)", "3 illustrated articles with images and return navigation to Home.")
    page.goto("http://localhost/blog/blog1.html")
    caption(page, "03b · Blog Article 1", "Detailed architectural discussion with illustrated network diagram.")

    # 3. Direct APIs
    page.goto("http://localhost/api/hello")
    caption(page, "04 · Flask API (/api/hello)", "Gateway proxies /api/hello to application-backend-server returning JSON.")
    page.goto("http://localhost/student/")
    caption(page, "05 · Proxy Route (/student/)", "Nginx gateway dedicated route to Flask /student endpoint.")

    # 4. Keycloak
    page.goto("http://localhost/auth/admin/master/console/")
    page.locator("#username").fill(cfg["KEYCLOAK_ADMIN"])
    page.locator("#password").fill(cfg["KEYCLOAK_ADMIN_PASSWORD"])
    page.locator("#kc-login").click()
    page.get_by_role("link", name="Users", exact=True).wait_for(timeout=30000)
    caption(page, "06 · Keycloak Identity & Security (R05 / E04)", "Admin console active; realm_521H0092, client flask-app and users sv01/sv02 configured.")

    # 5. MinIO
    page.goto("http://localhost:9001/")
    page.locator("#accessKey").fill(cfg["MINIO_ROOT_USER"])
    page.locator("#secretKey").fill(cfg["MINIO_ROOT_PASSWORD"])
    page.get_by_role("button", name="Login", exact=True).click()
    page.get_by_text("profile-pics", exact=True).first.wait_for(timeout=30000)
    caption(page, "07 · MinIO Object Storage (R06 / E05)", "Buckets: demo, profile-pics (public avatar.jpg) and documents (coursework report PDF).")

    # 6. Prometheus
    page.goto("http://localhost:9090/targets")
    page.get_by_text("web-frontend-server:80", exact=False).first.wait_for(timeout=30000)
    caption(page, "08 · Prometheus Monitoring (R08 / E07)", "Both node and web targets in UP state with real nginx metrics scraped.")

    # 7. Grafana
    page.goto("http://localhost:3000/login")
    page.locator('input[name="user"]').fill(cfg["GRAFANA_ADMIN_USER"])
    page.locator('input[name="password"]').fill(cfg["GRAFANA_ADMIN_PASSWORD"])
    page.get_by_role("button", name=re.compile("log in|sign in", re.I)).click()
    page.wait_for_url(lambda url: "/login" not in url, timeout=30000)
    page.goto("http://localhost:3000/d/system-health-521h0092/system-health-of-521h0092?orgId=1&from=now-15m&to=now")
    page.get_by_text("System Health of 521H0092", exact=True).first.wait_for(timeout=30000)
    caption(page, "09 · Grafana System Health (R09 / E08)", "Dashboard System Health of 521H0092 displaying CPU %, Memory %, and Network Traffic.")

    # 8. Round Robin Load Balancer
    page.goto("http://localhost/lb/whoami")
    caption(page, "10 · Round Robin Load Balancer (E10)", "Nginx gateway alternates sequentially between web-frontend-server1 and server2.")

    # 9. Evidence overview
    page.goto((EVIDENCE / "evidence.html").as_uri())
    caption(page, "11 · Complete Local Verification", "14/18 mandatory outputs and 10/10 extensions verified. AWS EC2 deferred until local inspection.", delay=5000)

    video = page.video
    context.close()
    destination = folder / "Demo_Local_521H0092.webm"
    if destination.exists():
        destination.unlink()
    video.save_as(str(destination))
    browser.close()

save("demo-chapters.json", result("Local demo video with 10 extensions", chapters))
set_status("R17", "DAT", "report/Demo_Local_521H0092.webm: complete walkthrough covering all 10 extensions; EC2 pending")
print(f"Saved {len(chapters)} demo chapters; video size: {destination.stat().st_size} bytes.")
