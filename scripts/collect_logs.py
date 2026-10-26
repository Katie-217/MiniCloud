"""Save sanitized service logs and the exact running image inventory."""
import json
from lab import config, run, save, result

cfg = config()
log = run("docker", "compose", "logs", "--no-color", "--tail", "80")
for key, value in cfg.items():
    if "PASSWORD" in key and value:
        log = log.replace(value, "[REDACTED]")
save("service-logs.txt", log)
inventory = []
for service in run("docker", "compose", "config", "--services").splitlines():
    image = run("docker", "inspect", service, "--format", '{{.Config.Image}}')
    image_id = run("docker", "inspect", service, "--format", '{{.Image}}')
    digests = json.loads(run("docker", "image", "inspect", image_id, "--format", '{{json .RepoDigests}}'))
    inventory.append({"service": service, "image": image, "image_id": image_id, "repo_digests": digests})
save("image-inventory.json", result("Runtime image inventory", inventory))
print("Saved sanitized service logs and exact image inventory.")
