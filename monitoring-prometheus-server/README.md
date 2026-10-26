# Phạm vi metrics

Node Exporter thu thập CPU/RAM/kernel của môi trường Linux chạy Docker, với `/proc`, `/sys` và root filesystem được bind mount chỉ đọc. Trên Docker Desktop, đây là Linux VM của Docker, không phải toàn bộ máy Windows. Exporter vẫn nằm trong `cloud-net`; network counters phản ánh namespace mạng mà exporter quan sát được, không đại diện đầy đủ mọi card mạng Windows.

Không dùng `network_mode: host` để giữ yêu cầu mọi service trong `cloud-net`. Cấu hình này cũng chưa cung cấp metrics theo từng container như cAdvisor. Test CPU/RAM/Network trong đề được đối chiếu trên dữ liệu thực có sẵn; báo cáo giữ rõ giới hạn này.

Root bind mount dùng `ro` với propagation mặc định: Docker Desktop trên máy này từ chối `rslave` vì mount `/` không shared/slave. `/proc` và `/sys` vẫn được mount riêng chỉ đọc để exporter lấy metrics.

Tham khảo: https://github.com/prometheus/node_exporter#docker
