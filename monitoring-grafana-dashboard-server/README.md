# Grafana Node Exporter Full

Dashboard import từ https://grafana.com/grafana/dashboards/1860-node-exporter-full/ revision **37**.
JSON nguồn: https://grafana.com/api/dashboards/1860/revisions/37/download

Điều chỉnh phục vụ provisioning: bỏ ID nội bộ và input import, đặt UID `node-exporter-full`, liên kết datasource Prometheus đã provision. Không tự nhận tác giả template; nội dung dashboard thuộc tác giả được ghi trong template gốc.

URL: http://localhost:3000/d/node-exporter-full/node-exporter-full

Đăng nhập bằng `GRAFANA_ADMIN_USER` / `GRAFANA_ADMIN_PASSWORD` trong `.env` local. Provisioning giúp dựng lại datasource/dashboard sau khi thay container; volume giữ dữ liệu Grafana. Các biểu đồ theo giới hạn metrics mô tả trong `monitoring-prometheus-server/README.md`.
