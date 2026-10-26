import json
from lab import run, save, result
from progress import set_status

services = run("docker", "compose", "config", "--services").splitlines()
assert len(services) == 10, services
network = json.loads(run("docker", "network", "inspect", "cloud-net"))[0]
members = {entry["Name"] for entry in network["Containers"].values()}
assert set(services) <= members, (services, members)
command = 'for service; do printf "\\n=== %s ===\\n" "$service"; ping -c 3 -W 3 "$service"; done'
output = run("docker", "run", "--rm", "--network", "cloud-net", "myminicloud-tools:local", "sh", "-ec", command, "sh", *services)
assert output.count("0% packet loss") == 10
evidence = save("R11-network.json", result("R11", {
    "network": "cloud-net", "services": services, "all_members_present": True,
    "ping_command": "ping -c 3 -W 3 <each service>", "output": output,
}))
set_status("R11", "DAT", evidence + "; ping 3 packets for each of 10 services, 0% loss")
print("PASS: all 10 containers resolve and respond to ping; " + evidence)
