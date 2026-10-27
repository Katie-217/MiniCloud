"""Verify E10: Nginx Round Robin load balancing across 2 Web servers."""
import requests
from lab import ROOT, save, result
from progress import set_status

base_url = "http://localhost/lb"

# 1. Sequential whoami requests
whoami_results = []
for i in range(1, 9):
    res = requests.get(f"{base_url}/whoami", timeout=5)
    assert res.status_code == 200, f"Request {i} failed with status {res.status_code}"
    server_header = res.headers.get("X-Backend-Server")
    body = res.text.strip()
    whoami_results.append({
        "request": i,
        "status": res.status_code,
        "server_header": server_header,
        "body": body
    })

# Check alternating servers
servers_seen = [r["server_header"] for r in whoami_results]
assert "web-frontend-server1" in servers_seen and "web-frontend-server2" in servers_seen, "Not both servers served traffic"
for i in range(len(servers_seen) - 1):
    assert servers_seen[i] != servers_seen[i+1], f"Round robin broken at step {i}: {servers_seen[i]} followed by {servers_seen[i+1]}"

# 2. Sequential HTML requests
html_results = []
for i in range(1, 5):
    res = requests.get(f"{base_url}/", timeout=5)
    assert res.status_code == 200, f"HTML Request {i} failed with status {res.status_code}"
    html_results.append({
        "request": i,
        "status": res.status_code,
        "server_header": res.headers.get("X-Backend-Server")
    })

details = {
    "upstream": "web_lb",
    "servers": ["web-frontend-server1:80", "web-frontend-server2:80"],
    "whoami_requests": whoami_results,
    "html_requests": html_results,
    "distribution": {
        "web-frontend-server1": servers_seen.count("web-frontend-server1"),
        "web-frontend-server2": servers_seen.count("web-frontend-server2")
    }
}

path = save("E10-round-robin.json", result("E10", details))
set_status("E10", "DAT", f"{path}; feat/round-robin-balancing; python scripts/check_round_robin.py")
print("PASS E10: Round robin load balancing alternating strictly between web-frontend-server1 and web-frontend-server2.")
