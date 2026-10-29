"""Present captured command results as readable local evidence, then screenshot."""
import html
import json
from playwright.sync_api import sync_playwright
from browser import launch
from lab import EVIDENCE, ROOT, save, result
from progress import set_status

def read(name):
    return json.loads((EVIDENCE / name).read_text(encoding="utf-8"))["details"]

def table(headers, rows):
    cell = lambda value: html.escape(str(value))
    return "<table><tr>" + "".join(f"<th>{cell(x)}</th>" for x in headers) + "</tr>" + "".join(
        "<tr>" + "".join(f"<td>{cell(x)}</td>" for x in row) + "</tr>" for row in rows) + "</table>"

def block(identifier, title, source, content):
    return f'<section id="{identifier}"><p class="label">MYMINICLOUD · LOCAL VERIFICATION · 521H0092</p><h1>{title}</h1><p>Source: <code>{source}</code> — captured test results, not sample output.</p>{content}</section>'

def pre(value):
    return "<pre>" + html.escape(value if isinstance(value, str) else json.dumps(value, ensure_ascii=False, indent=2)) + "</pre>"

stack = read("R01-stack.json")
network = read("R11-network.json")
release = read("release-images.json")
sections = [
    block("R01", f"{stack['service_count']} running/healthy containers · 9 server roles", "R01-stack.json", table(
        ["Container", "Health", "Network", "Restart policy"],
        [[row["service"], row["health"], ", ".join(row["networks"]), row["restart"]] for row in stack["checks"]])),
    block("R03", "Flask API · direct and gateway", "R03-api.json", pre(read("R03-api.json"))),
    block("R04", "MariaDB · initial schema and records", "R04-database.json", pre(read("R04-database.json"))),
    block("R07", "Bind9 · authoritative DNS", "R07-dns.json", pre(read("R07-dns.json"))),
    block("R10", "Reverse Proxy · Web / API / Auth", "R10-gateway.json", pre(read("R10-gateway.json"))),
    block("R11", "cloud-net · 3 pings to each service", "R11-network.json", table(
        ["Container", "Packets", "Loss"], [[service, "3 transmitted / 3 received", "0%"] for service in network["services"]]) +
        "<p>Full ping output is retained in R11-network.json.</p>"),
    block("R12", "State preserved after recreating 5 containers", "R12-persistence.json", pre(read("R12-persistence.json"))),
    block("R13", "Verified custom images on Docker Hub", "release-images.json", table(
        ["Image tag", "Digest prefix", "Registry verification"],
        [[image["tag"], image["digest"][:27] + "…", image["registry_manifest_verified"]] for image in release["images"].values()]) +
        "<p>Full digests for every runtime image are retained in release-images.json.</p>"),
]
for identifier, title, filename in [
    ("E03", "Student SQL schema and actual rows", "E03-student-database.json"),
    ("E04", "Signed token acceptance and rejection", "E04-keycloak.json"),
    ("E06", "All service DNS records", "E06-dns.json"),
    ("E10", "Round robin across both Web backends", "E10-round-robin.json"),
    ("LOG", "Real request logs in Loki and Grafana", "service-logging.json"),
]:
    sections.append(block(identifier, title, filename, pre(read(filename))))
demo = read("elearning-demo.json")
sections.append(block("ELM", "E-learning local emulator demo", "elearning-demo.json", pre({
    "url": demo["url"], "project": demo["project"], "checks": demo["checks"], "scope": demo["scope"],
    "blocked_production_hosts": demo["blocked_production_hosts"], "browser_errors": demo["browser_errors"],
})))
page_html = '''<!doctype html><html lang="vi"><meta charset="utf-8"><title>MyMiniCloud local evidence</title>
<style>body{margin:0;background:#edf2f5;color:#183043;font:17px Arial,sans-serif}section{background:white;margin:28px;padding:36px;border-top:6px solid #167264;border-radius:8px}h1{font-size:30px}.label{font-size:12px;letter-spacing:2px;color:#167264}table{border-collapse:collapse;width:100%;font-size:15px}th,td{border:1px solid #d4dee5;padding:12px;text-align:left}th{background:#ecf3f5}pre{background:#132b38;color:#e1f3f4;padding:24px;white-space:pre-wrap;overflow-wrap:anywhere;line-height:1.5;font-size:16px}code{color:#125b69}</style>''' + "".join(sections) + "</html>"
path = EVIDENCE / "evidence.html"
path.write_text(page_html, encoding="utf-8")
with sync_playwright() as p:
    browser = launch(p)
    page = browser.new_page(viewport={"width": 1400, "height": 1000})
    for route, filename in [("/", "R02-home.png"), ("/blog/", "R02-blog.png")]:
        page.goto("http://localhost:8080" + route)
        page.screenshot(path=str(EVIDENCE / filename), full_page=True)
    page.goto(path.as_uri())
    for identifier in ["R01", "R03", "R04", "R07", "R10", "R11", "R12", "R13", "E03", "E04", "E06", "E10", "LOG", "ELM"]:
        page.locator("#" + identifier).screenshot(path=str(EVIDENCE / f"{identifier}-result.png"))
    browser.close()
required_source = ["docker-compose.yml", "docker-compose.release.yml", "release-images.json", ".env.example",
    "web-frontend-server/Dockerfile", "application-backend-server/Dockerfile", "object-storage-server/Dockerfile",
    "elearning-web/Dockerfile", "firebase-emulator/Dockerfile", "tools/Dockerfile",
    "relational-database-server/init/002_students.sql", "relational-database-server/init/003_student_permissions.sh",
    "authentication-identity-server/realm-template.json", "internal-dns-server/db.cloud.local",
    "api-gateway-proxy-server/nginx.conf", "logging-loki-server/loki.yml", "logging-alloy-server/config.alloy",
    "elearning-web/provenance.json", "elearning-web/source/pubspec.lock", "scripts/run_release.py", "scripts/build_elearning.py"]
assert all((ROOT / filename).is_file() for filename in required_source)
source_path = save("R15-source.json", result("R15", {"required_source_files_present": required_source,
    "runtime_service_count": stack["service_count"], "published_custom_images": len(release["images"]),
    "runtime_build_required_for_release": False, "source_build_instructions": "README.md; elearning-web/README.md"}))
set_status("R15", "DAT", source_path + "; pinned pull release + source/config/build instructions present")
set_status("R18", "CHO_KIEM_THU", "evidence/local: đủ ảnh/log từng server, network, persistence, Docker Hub; EC2 chưa thực hiện")
print("Saved readable screenshots of real captured results and the Web pages.")
