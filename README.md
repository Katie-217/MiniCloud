# MiniCloud
xây dựng hệ thống Cloud thu nhỏ (MyMiniCloud) gồm 9 loại máy chủ cơ bản, mô phỏng các thành phần trong hạ tầng của một Cloud Platform (như AWS, Azure, GCP).

Nhóm: **Võ Thị Thiên Kim — 521H0092**, **Diệp Yến Nhi — chờ MSSV**.

Ưu tiên hiện tại: hoàn thành và kiểm thử phần bắt buộc trên local. AWS chờ thông tin từ người dùng; các mục mở rộng làm sau phần bắt buộc.

## Chuẩn bị

Docker Desktop dùng Linux containers, Docker Compose v2, Git và Python 3.11+ cho các script quản lý/kiểm thử.

```powershell
python scripts/setup.py
python -m venv .venv
.venv/Scripts/python -m pip install -r scripts/requirements-dev.txt
docker compose config --quiet
```

Mật khẩu local sinh ngẫu nhiên trong `.env`, không commit file này. Không ghi đè `.env` đã có khi chạy lại setup.

## Tài liệu và tiến độ

- [Yêu cầu theo PDF](KE_HOACH_MINICLOUD_2_NGAY.md)
- [Thứ tự triển khai và branch](KE_HOACH_TRIEN_KHAI_BAT_BUOC.md)
- [Output đã đạt, cần fix, chưa làm](TIEN_DO_OUTPUT.md)

Mỗi nhóm có branch riêng; mỗi chức năng/output có commit nhỏ, thông điệp tiếng Anh theo `type: summary`.

## Khởi động toàn hệ thống local

```powershell
docker compose up -d --build --wait
docker build -t myminicloud-tools:local tools
.venv/Scripts/python scripts/check_all.py --screenshots
```

Lần build MinIO đầu tải source chính thức và compile Go nên có thể mất vài phút. Tag nguồn và SHA256 archive đã ghim trong Dockerfile. Có **9 loại server / 10 container thường trực**; container công cụ chỉ chạy tạm khi kiểm thử.

| Dịch vụ | URL / cổng host | Thông tin đăng nhập trong `.env` |
|---|---|---|
| Gateway Web | http://localhost/ | — |
| Web trực tiếp / Blog | http://localhost:8080/ và http://localhost:8080/blog/ | — |
| API trực tiếp | http://localhost:8085/hello | — |
| API qua proxy | http://localhost/api/hello ; http://localhost/api/notes | — |
| MariaDB | 127.0.0.1:3306 hoặc exec trong container | MARIADB_USER / MARIADB_PASSWORD |
| Keycloak qua proxy | http://localhost/auth/admin/master/console/ | KEYCLOAK_ADMIN / KEYCLOAK_ADMIN_PASSWORD |
| Keycloak trực tiếp | http://localhost:8081/auth/admin/master/console/ | Cùng tài khoản trên |
| MinIO Console | http://localhost:9001/ | MINIO_ROOT_USER / MINIO_ROOT_PASSWORD |
| MinIO S3 API | http://localhost:9000/ | Cùng thông tin MinIO |
| Bind9 | UDP/TCP 1053 → 53 | Không cần tài khoản |
| Prometheus | http://localhost:9090/targets | — |
| Grafana | http://localhost:3000/d/node-exporter-full/node-exporter-full | GRAFANA_ADMIN_USER / GRAFANA_ADMIN_PASSWORD |
| Node Exporter | http://localhost:9100/metrics | — |

Kết quả đã kiểm chứng: Home/Blog 200; hello trực tiếp/proxy đúng JSON; DB có seed; admin Keycloak và sv01; MinIO upload/download khớp bytes; DNS đúng IP mẫu; Prometheus UP; Grafana CPU/RAM/Network; gateway Web/App/Auth; ping 10 service; volume giữ dữ liệu sau recreate. Log và ảnh cụ thể nằm ở `evidence/local/`.

## Chạy lại từng nhóm kiểm thử

```powershell
.venv/Scripts/python scripts/check_web.py --blog
.venv/Scripts/python scripts/check_app.py --proxy
.venv/Scripts/python scripts/check_database.py
.venv/Scripts/python scripts/check_app_database.py
.venv/Scripts/python scripts/check_auth.py
.venv/Scripts/python scripts/check_storage.py
.venv/Scripts/python scripts/check_dns.py
.venv/Scripts/python scripts/check_monitoring.py
.venv/Scripts/python scripts/check_grafana.py
.venv/Scripts/python scripts/check_gateway.py
.venv/Scripts/python scripts/check_network.py
.venv/Scripts/python scripts/check_stack.py
```

`check_auth.py` tạo user sv01 nếu chưa có, `check_storage.py` upload lại file HTML demo. Các script không xóa volume hay dừng project khác.

Kiểm chứng dữ liệu bền vững:

```powershell
.venv/Scripts/python scripts/check_persistence.py
```

Lệnh này tạo marker kiểm chứng và recreate đúng 5 service lưu dữ liệu của MyMiniCloud, có gián đoạn ngắn; không xóa named volume. Kết quả trong `R12-persistence.json`.

## Báo cáo, ảnh và video

- [Báo cáo local PDF](report/BaoCao_Local_521H0092.pdf), [DOCX](report/BaoCao_Local_521H0092.docx), [source Markdown](report/BaoCao_Local_521H0092.md).
- [Video walkthrough local](report/Demo_Local_521H0092.webm): không có giọng đọc, có chú thích từng chương; trình bày các kết quả thực tế.
- [Ảnh/log local](evidence/local/) và [trang xem kết quả lệnh](evidence/local/evidence.html).
- [Docker Hub Web image](https://hub.docker.com/r/katie217/myminicloud-web), tag `1.0.0`; digest trong `evidence/local/R13-dockerhub.json`.

Tạo lại tài liệu khi có thay đổi kết quả:

```powershell
.venv/Scripts/python scripts/collect_logs.py
.venv/Scripts/python scripts/capture_evidence.py
.venv/Scripts/python scripts/record_demo.py
.venv/Scripts/python scripts/build_report.py
```

Nếu chưa có browser dùng cho screenshot/video: `.venv/Scripts/python -m playwright install chromium`.

## Phần đang chờ

AWS EC2 chưa thực hiện theo yêu cầu người dùng. Hồ sơ hiện là **bản local**, cần bổ sung EC2/public IP và ảnh/video cloud trước khi đánh dấu toàn bộ phần bắt buộc hoàn tất. MSSV của Diệp Yến Nhi chưa được cung cấp. Các mục mở rộng hiện **0/10**.

Giới hạn monitoring: số liệu CPU/RAM của Linux VM Docker Desktop, network theo namespace exporter; chưa có số liệu từng container hoặc toàn bộ Windows. Một số panel tùy chọn (ví dụ Root FS) có thể N/A. Grafana đang hiển thị metrics Prometheus; chưa triển khai Loki/logging tập trung.

## Dừng project

```powershell
docker compose stop
```

Dữ liệu vẫn được giữ. Chỉ thao tác các service của project này; tránh `down -v` nếu muốn giữ dữ liệu demo.
