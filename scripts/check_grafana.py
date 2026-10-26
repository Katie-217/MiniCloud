import requests
from lab import config, save, result
from progress import set_status

cfg = config()
session = requests.Session()
session.auth = (cfg["GRAFANA_ADMIN_USER"], cfg["GRAFANA_ADMIN_PASSWORD"])
base = "http://localhost:3000"
response = session.get(base + "/api/datasources/uid/prometheus/health", timeout=15)
response.raise_for_status()
assert response.json()["status"] == "OK", response.json()
response = session.get(base + "/api/dashboards/uid/node-exporter-full", timeout=15)
response.raise_for_status()
dashboard = response.json()["dashboard"]
assert dashboard["title"] == "Node Exporter Full"
queries = {
    "cpu": '100 * (1 - avg(rate(node_cpu_seconds_total{job="node",mode="idle"}[5m])))',
    "memory": '100 * (1 - node_memory_MemAvailable_bytes{job="node"}/node_memory_MemTotal_bytes{job="node"})',
    "network": 'sum(rate(node_network_receive_bytes_total{job="node",device!="lo"}[5m]))',
}
values = {}
for name, query in queries.items():
    response = session.get(base + "/api/datasources/proxy/uid/prometheus/api/v1/query", params={"query": query}, timeout=15)
    response.raise_for_status()
    rows = response.json()["data"]["result"]
    assert rows, (name, response.text)
    values[name] = rows
evidence = save("R09-grafana.json", result("R09", {
    "datasource_health": "OK", "dashboard": dashboard["title"], "uid": dashboard["uid"],
    "metric_queries_through_grafana": values,
}))
set_status("R09", "CHO_KIEM_THU", evidence + "; datasource + queries đạt; chờ kiểm tra hình ảnh dashboard")
print("PASS: dashboard provisioned and CPU/RAM/network queries through Grafana return data; " + evidence)
