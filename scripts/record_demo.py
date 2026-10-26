"""Record a silent, captioned walkthrough of the running LOCAL system."""
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

def caption(page, title, note):
    page.evaluate('''([title,note]) => {
        document.getElementById('demo-caption')?.remove();
        const box = document.createElement('div'); box.id='demo-caption';
        Object.assign(box.style,{position:'fixed',bottom:'16px',left:'20px',right:'20px',zIndex:'2147483647',background:'#123b42',color:'white',padding:'15px 20px',fontFamily:'Arial',borderRadius:'8px',fontSize:'18px',boxShadow:'0 2px 15px #0005'});
        const heading=document.createElement('strong');heading.textContent=title;
        const small=document.createElement('div');small.textContent=note;small.style.fontSize='14px';small.style.marginTop='5px';
        box.append(heading,small);document.body.append(box);
    }''', [title, note])
    page.wait_for_timeout(4500)
    chapters.append({"chapter": title, "url": page.url, "note": note})

with sync_playwright() as p:
    browser = launch(p)
    context = browser.new_context(viewport={"width": 1440, "height": 1000},
        record_video_dir=str(temporary), record_video_size={"width": 1440, "height": 1000})
    page = context.new_page()

    def evidence(identifier, title, note):
        page.goto((EVIDENCE / "evidence.html").as_uri() + "#" + identifier)
        page.locator("#" + identifier).scroll_into_view_if_needed()
        caption(page, title, note)

    evidence("R01", "01 · Docker Compose / cloud-net", "9 server roles, 10 healthy containers; local verification only.")
    page.goto("http://localhost/")
    caption(page, "02 · Web Home through Gateway", "HTTP 200. Group: Vo Thi Thien Kim / 521H0092 and Diep Yen Nhi.")
    page.get_by_role("link", name=re.compile("Blog")).click()
    caption(page, "03 · Static Blog", "Nginx serves /blog/; navigation back to Home is available.")
    evidence("R03", "04 · Flask API", "Direct :8085/hello and gateway /api/hello return matching JSON.")
    evidence("R04", "05 · MariaDB", "Actual SHOW TABLES / SELECT output, including initial seed and persistence marker.")
    page.goto("http://localhost/auth/admin/master/console/")
    page.locator("#username").fill(cfg["KEYCLOAK_ADMIN"])
    page.locator("#password").fill(cfg["KEYCLOAK_ADMIN_PASSWORD"])
    page.locator("#kc-login").click()
    page.get_by_role("link", name="Users", exact=True).wait_for(timeout=30000)
    page.get_by_role("link", name="Users", exact=True).click()
    page.get_by_text("sv01", exact=True).first.wait_for(timeout=30000)
    caption(page, "06 · Keycloak through /auth/", "Administrator login succeeds and sv01 exists in master realm.")
    page.goto("http://localhost:9001/")
    page.locator("#accessKey").fill(cfg["MINIO_ROOT_USER"])
    page.locator("#secretKey").fill(cfg["MINIO_ROOT_PASSWORD"])
    page.get_by_role("button", name="Login", exact=True).click()
    page.get_by_text("demo", exact=True).first.click()
    page.get_by_text("index.html", exact=True).first.wait_for(timeout=30000)
    caption(page, "07 · MinIO Object Storage", "demo/index.html is uploaded; download was verified byte-for-byte and by SHA256.")
    evidence("R07", "08 · Bind9 DNS", "dig returns 10.10.10.10 on internal port 53 and published host port 1053.")
    page.goto("http://localhost:9090/targets")
    page.get_by_text("monitoring-node-exporter-server:9100", exact=False).first.wait_for(timeout=30000)
    caption(page, "09 · Prometheus", "Node Exporter target is UP; CPU, memory and network metrics are available.")
    page.goto("http://localhost:3000/login")
    page.locator('input[name="user"]').fill(cfg["GRAFANA_ADMIN_USER"])
    page.locator('input[name="password"]').fill(cfg["GRAFANA_ADMIN_PASSWORD"])
    page.get_by_role("button", name=re.compile("log in|sign in", re.I)).click()
    page.wait_for_url(lambda url: "/login" not in url, timeout=30000)
    page.goto("http://localhost:3000/d/node-exporter-full/node-exporter-full?from=now-5m&to=now&var-datasource=prometheus&var-job=node&var-node=monitoring-node-exporter-server:9100")
    page.get_by_text("CPU Busy", exact=True).first.wait_for(timeout=30000)
    page.wait_for_timeout(3000)
    caption(page, "10 · Grafana Node Exporter Full", "CPU / RAM / Network charts use real Linux Docker metrics; this is not Windows host monitoring.")
    evidence("R10", "11 · Unified Reverse Proxy", "Web 200, API JSON, Auth 302 and public OIDC issuer verified.")
    evidence("R11", "12 · Internal Network", "3 ICMP packets to each of 10 services; 0% packet loss.")
    evidence("R12", "13 · Persistent Volumes", "Five containers recreated; DB, user, object, Grafana folder and historical samples preserved.")
    evidence("R13", "14 · Docker Hub / Remaining Work", "katie217/myminicloud-web:1.0.0 published. AWS EC2 and final cloud evidence remain pending; 0/10 extensions.")
    video = page.video
    context.close()
    destination = folder / "Demo_Local_521H0092.webm"
    if destination.exists():
        destination.unlink()
    video.save_as(str(destination))
    browser.close()
save("demo-chapters.json", result("Local demo video", chapters))
set_status("R17", "CHO_KIEM_THU", "report/Demo_Local_521H0092.webm: silent captioned local walkthrough; EC2 segment pending")
print(f"Saved {len(chapters)} demo chapters; video bytes: {destination.stat().st_size}; AWS segment pending.")
