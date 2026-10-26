import time
import requests
from lab import save, result
from progress import set_status

base = "http://localhost:9090"
deadline = time.monotonic() + 60
while True:
    response = requests.get(base + "/api/v1/targets", timeout=10)
    response.raise_for_status()
    targets = response.json()["data"]["activeTargets"]
    if targets and all(target["health"] == "up" for target in targets):
        break
    if time.monotonic() >= deadline:
        raise AssertionError([(x["scrapeUrl"], x["health"], x["lastError"]) for x in targets])
    time.sleep(2)
metrics = {}
for query in ["up{job=\"node\"}", "node_cpu_seconds_total", "node_memory_MemAvailable_bytes", "node_network_receive_bytes_total"]:
    response = requests.get(base + "/api/v1/query", params={"query": query}, timeout=10)
    response.raise_for_status()
    rows = response.json()["data"]["result"]
    assert rows, query
    metrics[query] = {"series_count": len(rows), "sample": rows[0]}
evidence = save("R08-monitoring.json", result("R08", {
    "targets": [{"url": x["scrapeUrl"], "health": x["health"], "last_error": x["lastError"]} for x in targets],
    "queries": metrics,
    "scope": "Docker Desktop Linux VM CPU/memory; exporter-visible network namespace; not Windows host/per-container monitoring",
}))
set_status("R08", "DAT", evidence)
print("PASS: node target UP and CPU/memory/network metrics available; " + evidence)
