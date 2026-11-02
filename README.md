# MyMiniCloud

Cloud thu nhỏ theo đề cuối kỳ: **9 vai trò máy chủ / 17 container**, network `cloud-net`, **10 mục mở rộng** và ứng dụng E-learning tái sử dụng. Nhóm: **Võ Thị Thiên Kim — 521H0092**, **Diệp Yến Nhi — chờ bổ sung MSSV**.

Mốc kiểm thử đã lưu: **29/10/2026**, 27 bước chức năng/UI đạt. Rà soát ngày **02/11/2026**: Docker engine chưa chạy nên chưa xác nhận lại runtime; báo cáo/video và tracker cần đồng bộ theo bản cuối. **AWS chỉ triển khai sau khi người dùng xác nhận local.** [Trạng thái output](TIEN_DO_OUTPUT.md), [kế hoạch bàn giao Gemini](BAN_GIAO_GEMINI.md).

## Chạy release

Cần Docker Desktop Linux engine, Compose v2 và Python 3.11+. Chạy trong PowerShell tại thư mục repo:

```powershell
python -m venv .venv
.venv/Scripts/python -m pip install -r scripts/requirements-dev.txt
.venv/Scripts/python -m playwright install chromium
.venv/Scripts/python scripts/run_release.py --verify
```

Nếu đã có môi trường thì bỏ qua bước tạo/cài đặt. Script tạo `.env` ngẫu nhiên nếu chưa có, giữ file đã có; kéo **17 runtime image ghim digest**, không build source. Lần đầu dùng `--verify` để thiết lập và kiểm tra đủ dữ liệu demo. Lần sau chỉ mở lại: `.venv/Scripts/python scripts/run_release.py`. Không cần Flutter để chạy release.

Release **local-20261029.1** có 6 image tùy chỉnh: Web/App/MinIO/E-learning/Firebase và tools (5 loại runtime + công cụ). Manifest/SHA256: [release-images.json](release-images.json), [Compose release](docker-compose.release.yml), [Docker Hub katie217](https://hub.docker.com/u/katie217).

Mật khẩu đọc từ `.env` local, khóa mẫu ở [.env.example](.env.example). Không commit bí mật/dữ liệu volume; không dùng `docker compose down -v` để sửa lỗi thông thường.

## Giao diện

| Chức năng | URL | Tài khoản / khóa .env |
|---|---|---|
| Portal, Blog, sinh viên, API bảo vệ, cân bằng tải | http://localhost/ | sv01/sv02 + KEYCLOAK_TEST_PASSWORD cho form bảo vệ |
| API | http://localhost/api/hello ; http://localhost/api/student ; http://localhost/student/ | /api/secure cần token |
| SQL students | http://localhost/api/students-db | 3 SQL; /student có 5 JSON riêng |
| Keycloak admin | http://localhost/auth/admin/master/console/ | KEYCLOAK_ADMIN / KEYCLOAK_ADMIN_PASSWORD |
| MinIO Console | http://localhost:9001/ | MINIO_ROOT_USER / MINIO_ROOT_PASSWORD |
| Avatar public | http://localhost:9000/profile-pics/avatar.jpg | Chữ K; documents PDF riêng tư |
| Prometheus | http://localhost:9090/targets | Job node và web UP |
| Grafana health | http://localhost:3000/d/system-health-521h0092 | GRAFANA_ADMIN_USER / GRAFANA_ADMIN_PASSWORD |
| Grafana logs | http://localhost:3000/d/minicloud-service-logs | Cùng tài khoản Grafana |
| E-learning | http://localhost/elearning/ | instructor@example.test / student@example.test; ELEARNING_INSTRUCTOR_PASSWORD / ELEARNING_STUDENT_PASSWORD |

Cổng trực tiếp: Web8080, App8085, Keycloak8081, Bind9 UDP/TCP1053. MariaDB3306, NodeExporter9100, Loki3100, Alloy12345, Firebase9099/8180/9199 bind loopback. **[Hướng dẫn từng bước và ảnh cần chụp](HUONG_DAN_TEST_LOCAL.md)**.

## Kiểm thử và phạm vi

`run_release.py --verify` chạy 27 bước chức năng/UI, core persistence, hai vai trò E-learning, Firebase persistence và Loki persistence. [Minh chứng](evidence/local/evidence.html), [log 29/10](evidence/local/final-verification-20261029.log). Không dừng container ngoài project hoặc xóa volume.

CPU/RAM phản ánh Linux VM Docker Desktop; mạng là namespace Node Exporter. Chưa đo riêng từng container. DNS lab 10.10.10.x là bản ghi theo đề, khác Docker DNS kết nối service. E-learning dùng Firebase Emulator `demo-minicloud`, dữ liệu giả; hai vai trò, khóa học, số ghi danh/F5 đã thử, chức năng khác của repo gốc chưa được xác nhận.

## Build source khi phát triển

Release không cần bước này. Nếu thay E-learning, dùng Flutter **3.35.7**; script build trong thư mục tạm ASCII để tránh lỗi đường dẫn Unicode Windows:

```powershell
.venv/Scripts/python scripts/setup.py
.venv/Scripts/python scripts/build_elearning.py
docker compose build
docker build -t myminicloud-tools:local tools
docker compose up -d --wait
.venv/Scripts/python scripts/check_all.py --screenshots
.venv/Scripts/python scripts/check_elearning.py
```

MinIO build source chính thức ghim tag/checksum, giữ AGPL license. E-learning provenance/bản vá SDK: [README riêng](elearning-web/README.md), [provenance](elearning-web/provenance.json). Không push ngược repo ứng dụng gốc.

## Hồ sơ

- [Trạng thái R01–R18, E01–E10](TIEN_DO_OUTPUT.md)
- [Kế hoạch local](KE_HOACH_HOAN_THIEN_LOCAL.md), [đối chiếu PDF](KE_HOACH_MINICLOUD_2_NGAY.md)
- [Báo cáo PDF](report/BaoCao_Local_521H0092.pdf), [DOCX](report/BaoCao_Local_521H0092.docx), [Markdown](report/BaoCao_Local_521H0092.md) — đang chờ cập nhật theo bản 17 container
- [Video](report/Demo_Local_521H0092.webm), [trang xem](report/Demo_Local_521H0092.html) — đang chờ quay lại bản cuối

Mỗi chức năng một branch; commit tiếng Anh `type: summary` với 4–5 từ sau tiền tố. Gemini bàn giao branch/commit để Codex kiểm thử trước khi tích hợp main.
