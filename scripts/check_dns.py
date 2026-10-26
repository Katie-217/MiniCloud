from lab import run, save, result
from progress import set_status

name = "web-frontend-server.cloud.local"
checks = []
for server, port in [("internal-dns-server", "53"), ("host.docker.internal", "1053")]:
    value = run("docker", "run", "--rm", "--network", "cloud-net",
                "myminicloud-tools:local", "dig", "@" + server, "-p", port, name, "+short")
    assert value.strip() == "10.10.10.10", value
    checks.append({"server": server, "port": port, "name": name, "answer": value})
evidence = save("R07-dns.json", result("R07", checks))
set_status("R07", "DAT", evidence + "; dig internal 53 + published host 1053")
print("PASS: authoritative DNS over internal and published ports; " + evidence)
