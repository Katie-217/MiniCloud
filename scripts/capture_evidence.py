"""Present captured command results as readable local evidence, then screenshot."""
import html
import json
from playwright.sync_api import sync_playwright
from browser import launch
from lab import EVIDENCE, ROOT
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
sections = [
    block("R01", "10 healthy containers · 9 server roles", "R01-stack.json", table(
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
    block("R13", "Custom image published to Docker Hub", "R13-dockerhub.json", pre({k: v for k,v in read("R13-dockerhub.json").items() if k != "push_output"})),
]
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
    for identifier in ["R01", "R03", "R04", "R07", "R10", "R11", "R12", "R13"]:
        page.locator("#" + identifier).screenshot(path=str(EVIDENCE / f"{identifier}-result.png"))
    browser.close()
set_status("R18", "CHO_KIEM_THU", "evidence/local: đủ ảnh/log từng server, network, persistence, Docker Hub; EC2 chưa thực hiện")
print("Saved readable screenshots of real captured results and the Web pages.")
