"""Publish the verified custom Web image; never handles login credentials."""
import json
import re
import subprocess
from lab import config, ROOT, run, save, result
from progress import set_status

cfg = config()
namespace = cfg["DOCKERHUB_USERNAME"]
assert namespace == json.loads((ROOT / "project-info.json").read_text(encoding="utf-8"))["dockerhub_username"]
source = f"{namespace}/myminicloud-web:{cfg.get('IMAGE_TAG', 'local')}"
target = f"{namespace}/myminicloud-web:1.0.0"
run("docker", "tag", source, target)
print(f"Pushing verified image {target} ...", flush=True)
process = subprocess.run(["docker", "push", target], cwd=ROOT, capture_output=True, text=True, encoding="utf-8", errors="replace")
if process.returncode:
    set_status("R13", "CAN_FIX", "Docker Hub push chưa thành công; cần kiểm tra docker login và quyền namespace")
    raise RuntimeError((process.stdout + process.stderr)[-2000:])
manifest = json.loads(run("docker", "manifest", "inspect", target))
match = re.search(r"digest: (sha256:[a-f0-9]{64})", process.stdout)
assert match, "Registry did not return a digest"
evidence = save("R13-dockerhub.json", result("R13", {
    "image": target, "digest": match.group(1), "manifest_read_back": True,
    "repository_url": f"https://hub.docker.com/r/{namespace}/myminicloud-web",
    "tag_url": f"https://hub.docker.com/r/{namespace}/myminicloud-web/tags",
    "manifest_media_type": manifest.get("mediaType"), "push_output": process.stdout,
}))
set_status("R13", "DAT", evidence + f"; {target}; manifest verified from registry")
print("PASS: push succeeded and manifest read back from Docker Hub; " + evidence)
