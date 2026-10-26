"""Common local demo helpers; never print secrets or tokens."""
import json
from pathlib import Path
import subprocess
from datetime import datetime, timezone

ROOT = Path(__file__).resolve().parents[1]
EVIDENCE = ROOT / "evidence" / "local"

def config():
    values = {}
    for line in (ROOT / ".env").read_text(encoding="utf-8").splitlines():
        if line and not line.startswith("#") and "=" in line:
            key, value = line.split("=", 1)
            values[key] = value
    return values

def run(*args, input=None):
    result = subprocess.run(args, cwd=ROOT, input=input, capture_output=True,
                            text=True, encoding="utf-8", errors="replace")
    if result.returncode:
        raise RuntimeError(f"{args[0]} failed ({result.returncode}): {result.stderr[-1500:]}")
    return result.stdout.strip()

def save(name, value):
    EVIDENCE.mkdir(parents=True, exist_ok=True)
    path = EVIDENCE / name
    path.write_text(value if isinstance(value, str) else json.dumps(value, indent=2, ensure_ascii=False), encoding="utf-8")
    return str(path.relative_to(ROOT)).replace("\\", "/")

def result(output, details):
    return {"output": output, "verified_at_utc": datetime.now(timezone.utc).isoformat(), "details": details}
