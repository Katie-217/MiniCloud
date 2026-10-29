"""Publish the tested custom runtime images and pin their registry digests."""
import json
import re
import subprocess
import argparse
from lab import ROOT, config, run, save, result
from progress import set_status

cfg = config()
namespace = cfg["DOCKERHUB_USERNAME"]
assert namespace == "katie217"
parser = argparse.ArgumentParser()
parser.add_argument("--version", default="local-20261029.1")
tag = parser.parse_args().version
assert re.fullmatch(r"[A-Za-z0-9][A-Za-z0-9_.-]{0,127}", tag), "Invalid image tag"
sources = {
    "web": f"{namespace}/myminicloud-web:{cfg.get('IMAGE_TAG', 'local')}",
    "app": f"{namespace}/myminicloud-app:{cfg.get('IMAGE_TAG', 'local')}",
    "minio": f"{namespace}/myminicloud-minio:source-2025-04-22",
    "elearning": f"{namespace}/myminicloud-elearning:{cfg.get('IMAGE_TAG', 'local')}",
    "firebase": f"{namespace}/myminicloud-firebase:{cfg.get('IMAGE_TAG', 'local')}",
    "tools": "myminicloud-tools:local",
}
images = {}
for name, source in sources.items():
    target = f"{namespace}/myminicloud-{name}:{tag}"
    image_id = run("docker", "image", "inspect", source, "--format", "{{.Id}}")
    run("docker", "tag", source, target)
    print("Publishing " + target, flush=True)
    response = subprocess.run(["docker", "push", target], cwd=ROOT, capture_output=True,
        text=True, encoding="utf-8", errors="replace")
    if response.returncode:
        raise RuntimeError("Image push failed for " + target + ": " + response.stderr[-800:])
    match = re.search(r"digest: (sha256:[a-f0-9]{64})", response.stdout + response.stderr)
    assert match, "Missing registry digest for " + target
    digest = match.group(1)
    pinned = target.split(":")[0] + "@" + digest
    manifest = json.loads(run("docker", "manifest", "inspect", pinned))
    assert manifest.get("mediaType"), "Registry manifest not readable"
    images[name] = {"tag": target, "pinned": pinned, "digest": digest, "local_image_id": image_id,
        "registry_manifest_verified": True, "repository": f"https://hub.docker.com/r/{namespace}/myminicloud-{name}"}
    print("Verified " + name + " " + digest, flush=True)

mapping = {"web-frontend-server": "web", "web-frontend-server1": "web", "web-frontend-server2": "web",
    "application-backend-server": "app", "object-storage-server": "minio",
    "elearning-web-server": "elearning", "firebase-emulator-server": "firebase"}
runtime = {service: images[name]["pinned"] for service, name in mapping.items()}
official = {"api-gateway-proxy-server": "nginx:1.28-alpine", "relational-database-server": "mariadb:11.4",
    "authentication-identity-server": "quay.io/keycloak/keycloak:26.1.4",
    "internal-dns-server": "internetsystemsconsortium/bind9:9.18",
    "monitoring-node-exporter-server": "prom/node-exporter:v1.9.1",
    "monitoring-web-exporter-server": "nginx/nginx-prometheus-exporter:1.4.1",
    "monitoring-prometheus-server": "prom/prometheus:v3.2.1",
    "monitoring-grafana-dashboard-server": "grafana/grafana:11.6.0",
    "logging-loki-server": "grafana/loki:3.7.9", "logging-alloy-server": "grafana/alloy:v1.21.3"}
for service, source in official.items():
    print("Pinning official image " + source, flush=True)
    digests = json.loads(run("docker", "image", "inspect", source, "--format", "{{json .RepoDigests}}")) or []
    repository = source.rsplit(":", 1)[0]
    pinned = next((digest for digest in digests if digest.startswith(repository + "@")), None)
    assert pinned, "Missing pulled digest for " + source
    run("docker", "manifest", "inspect", pinned)
    runtime[service] = pinned
release = {"version": tag, "source_commit": run("git", "rev-parse", "HEAD"), "images": images,
    "custom_image_platform": run("docker", "image", "inspect", sources["web"], "--format", "{{.Os}}/{{.Architecture}}"),
    "runtime_images": runtime}
(ROOT / "release-images.json").write_text(json.dumps(release, indent=2) + "\n", encoding="utf-8")
override = "# Generated from verified Docker Hub manifests; no credentials.\nservices:\n"
override += "".join(f"  {service}:\n    image: {pinned}\n" for service, pinned in runtime.items())
(ROOT / "docker-compose.release.yml").write_text(override, encoding="utf-8")
path = save("release-images.json", result("Docker Hub local release", release))
set_status("R13", "DAT", path + f"; chore/local-release-images; {len(images)} custom images pushed and manifests verified")
print(f"PASS: all {len(images)} custom images published and pinned; " + path)
