import json
from lab import run, save, result
from progress import set_status

run("docker", "compose", "config", "--quiet")
services = run("docker", "compose", "config", "--services").splitlines()
assert len(services) >= 10, services
checks = []
for service in services:
    state = json.loads(run("docker", "inspect", service, "--format", '{{json .State}}'))
    policy = run("docker", "inspect", service, "--format", '{{.HostConfig.RestartPolicy.Name}}')
    networks = json.loads(run("docker", "inspect", service, "--format", '{{json .NetworkSettings.Networks}}'))
    assert state["Running"], f"{service} is not running"
    if "Health" in state:
        assert state["Health"]["Status"] == "healthy", f"{service} health is {state['Health']['Status']}"
        health_status = "healthy"
    else:
        health_status = "running"
    assert policy == "unless-stopped" and "cloud-net" in networks, service
    checks.append({"service": service, "running": True, "health": health_status, "restart": policy, "networks": list(networks)})
evidence = save("R01-stack.json", result("R01", {"service_count": len(services), "role_count": 9, "checks": checks}))
set_status("R01", "DAT", evidence + f"; {len(services)} running/healthy containers / 9 server roles")
print(f"PASS: Compose valid; all {len(services)} services healthy/running, cloud-net, restart unless-stopped; {evidence}")
