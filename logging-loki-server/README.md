# Log hệ thống trong Grafana

Loki lưu log trong named volume `loki-data`, cấu hình retention 24 giờ và xóa theo chu kỳ compactor; Alloy đọc Docker logs và lưu vị trí đọc trong `alloy-data`. Cả hai chỉ dùng cho lab local.

Alloy lọc nhãn `com.docker.compose.project=myminicloud` trước khi thu thập; không thu log project khác. Docker socket được mount read-only để discovery/read logs; cấu hình không thực hiện thao tác quản lý container. Loki/Alloy chỉ mở cổng host loopback 3100/12345.

Grafana: dashboard `MyMiniCloud Service Logs`, UID `minicloud-service-logs`; datasource Loki. Query mẫu: `{project="myminicloud",service="application-backend-server"}`. Gọi `/api/hello` rồi refresh dashboard để xem access log thật.

Kiểm thử `scripts/check_logging.py` tạo request marker riêng, truy vấn marker qua Loki và Grafana proxy, chụp dashboard, đồng thời kiểm tra các stream chỉ thuộc project này. Số liệu đã thu từ lúc Alloy hoạt động, không phải toàn bộ lịch sử container trước đó.

Nguồn cấu hình: [Alloy Docker logs](https://grafana.com/docs/alloy/latest/reference/components/loki/loki.source.docker/), [Loki filesystem](https://grafana.com/docs/loki/latest/operations/storage/filesystem/). Version được ghim và kiểm thử trong Compose/release manifest.
