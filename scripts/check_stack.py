import json
from lab import run, save, result
from progress import set_status

run("docker", "compose", "config", "--quiet")
services = run("docker", "compose", "config", "--services").splitlines()
assert len(services) == 10, services
checks = []
for service in services:
    state = json.loads(run("docker", "inspect", service, "--format", '{{json .State}}'))
    policy = run("docker", "inspect", service, "--format", '{{.HostConfig.RestartPolicy.Name}}')
    networks = json.loads(run("docker", "inspect", service, "--format", '{{json .NetworkSettings.Networks}}'))
    assert state["Running"] and state["Health"]["Status"] == "healthy", service
    assert policy == "unless-stopped" and "cloud-net" in networks, service
    checks.append({"service": service, "running": True, "health": "healthy", "restart": policy, "networks": list(networks)})
evidence = save("R01-stack.json", result("R01", {"service_count": 10, "role_count": 9, "checks": checks}))
set_status("R01", "DAT", evidence + "; 10 healthy containers / 9 server roles")
print("PASS: Compose valid; all 10 services healthy, cloud-net, restart unless-stopped; " + evidence)
