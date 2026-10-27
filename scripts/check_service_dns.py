"""Verify E06: Extended DNS records for App, MinIO, Keycloak, and Web."""
from lab import ROOT, run, save, result
from progress import set_status

records = [
    ("web-frontend-server.cloud.local", "10.10.10.10"),
    ("app-backend.cloud.local", "10.10.10.20"),
    ("minio.cloud.local", "10.10.10.30"),
    ("keycloak.cloud.local", "10.10.10.40"),
]

checks = []
zone_file = (ROOT / "internal-dns-server/db.cloud.local").read_text(encoding="utf-8")

for name, expected_ip in records:
    for server, port in [("internal-dns-server", "53"), ("host.docker.internal", "1053")]:
        value = run(
            "docker", "run", "--rm", "--network", "cloud-net",
            "myminicloud-tools:local", "dig", "@" + server, "-p", port, name, "+short"
        )
        actual_ip = value.strip()
        assert actual_ip == expected_ip, f"Query {name} on {server}:{port} expected {expected_ip}, got {actual_ip}"
        checks.append({
            "name": name,
            "expected_ip": expected_ip,
            "actual_ip": actual_ip,
            "server": server,
            "port": port,
            "matched": True
        })

details = {
    "records": records,
    "soa_serial": "2026102701",
    "checks": checks,
    "zone_file": zone_file
}

evidence = save("E06-dns.json", result("E06", details))
set_status("E06", "DAT", f"{evidence}; feat/service-dns-records; python scripts/check_service_dns.py")
print("PASS E06: all 4 DNS records (Web, App, MinIO, Keycloak) resolve correctly on internal:53 and host:1053.")
