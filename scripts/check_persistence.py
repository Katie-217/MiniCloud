"""Verify custom data across container recreation without removing volumes."""
import json
import time
import boto3
import requests
from botocore.config import Config
from lab import config, run, save, result
from progress import set_status

cfg = config()
services = ["relational-database-server", "authentication-identity-server", "object-storage-server",
            "monitoring-prometheus-server", "monitoring-grafana-dashboard-server"]

def volumes():
    return {service: json.loads(run("docker", "inspect", service, "--format", '{{json .Mounts}}')) for service in services}

def sql(query):
    return run("docker", "compose", "exec", "-T", "relational-database-server", "sh", "-c",
        'MYSQL_PWD="$MARIADB_ROOT_PASSWORD" mariadb -N -uroot -e "$1"', "sh", query)

marker = "Persistence verification 521H0092"
sql(f"INSERT INTO minicloud.notes(title) SELECT '{marker}' WHERE NOT EXISTS (SELECT 1 FROM minicloud.notes WHERE title='{marker}');")
session = requests.Session()
session.auth = (cfg["GRAFANA_ADMIN_USER"], cfg["GRAFANA_ADMIN_PASSWORD"])
folder = "http://localhost:3000/api/folders/persistence521h0092"
if session.get(folder, timeout=10).status_code == 404:
    response = session.post("http://localhost:3000/api/folders", json={"uid": "persistence521h0092", "title": "Persistence Verification"}, timeout=10)
    response.raise_for_status()
snapshot_time = time.time() - 2
params = {"query": "node_memory_MemTotal_bytes", "time": snapshot_time}
before = requests.get("http://localhost:9090/api/v1/query", params=params, timeout=10).json()["data"]["result"]
assert before, "Prometheus needs at least one completed scrape"
mounts_before = volumes()
ids_before = {service: run("docker", "inspect", service, "--format", '{{.Id}}') for service in services}
print("Recreating only the 5 MyMiniCloud stateful services; preserving named volumes.", flush=True)
run("docker", "compose", "up", "-d", "--force-recreate", "--no-deps", "--wait", "--wait-timeout", "180", *services)
assert marker in sql("SELECT title FROM minicloud.notes;"), "DB marker lost"
response = session.get(folder, timeout=15)
response.raise_for_status()
assert response.json()["uid"] == "persistence521h0092", "Grafana folder lost"
client = boto3.client("s3", endpoint_url="http://localhost:9000", aws_access_key_id=cfg["MINIO_ROOT_USER"],
    aws_secret_access_key=cfg["MINIO_ROOT_PASSWORD"], region_name="us-east-1", config=Config(signature_version="s3v4"))
assert b"MyMiniCloud" in client.get_object(Bucket="demo", Key="index.html")["Body"].read()
after = requests.get("http://localhost:9090/api/v1/query", params=params, timeout=10).json()["data"]["result"]
assert after == before, "Prometheus historical sample lost"
run(".venv/Scripts/python" if __import__("os").name == "nt" else ".venv/bin/python", "scripts/check_auth.py")
ids_after = {service: run("docker", "inspect", service, "--format", '{{.Id}}') for service in services}
assert all(ids_before[service] != ids_after[service] for service in services)
mounts_after = volumes()
named = lambda mounts: {service: sorted(x["Name"] for x in rows if x["Type"] == "volume") for service, rows in mounts.items()}
assert named(mounts_before) == named(mounts_after)
evidence = save("R12-persistence.json", result("R12", {
    "all_five_container_ids_changed": True, "named_volumes_unchanged": named(mounts_after),
    "database_custom_marker_preserved": marker, "keycloak_sv01_preserved": True,
    "minio_demo_object_preserved": True, "grafana_custom_folder_preserved": True,
    "prometheus_historical_sample_preserved": True, "historical_sample_time": snapshot_time,
}))
set_status("R12", "DAT", evidence + "; custom data preserved across all 5 stateful service recreations")
print("PASS: database/auth/storage/Prometheus/Grafana persistence; " + evidence)
