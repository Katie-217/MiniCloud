# Kiểm tra giao diện và chụp minh chứng local

Hướng dẫn dựa trên kết quả **29/10/2026**: 9 vai trò, **17 container**, 10 mở rộng. Rà soát **02/11/2026**: Docker engine chưa chạy; cần kiểm thử lại trước khi nghiệm thu. Báo cáo/video còn cần cập nhật theo [bản bàn giao Gemini](BAN_GIAO_GEMINI.md). AWS chờ bạn kiểm tra local. MSSV Diệp Yến Nhi bổ sung sau; avatar chữ **K** theo lựa chọn của bạn.

## 1. Khởi động

Mở Docker Desktop, đợi Linux engine chạy. Trong PowerShell tại thư mục repo:

```powershell
python -m venv .venv
.venv/Scripts/python -m pip install -r scripts/requirements-dev.txt
.venv/Scripts/python -m playwright install chromium
.venv/Scripts/python scripts/run_release.py --verify
```

Nếu `.venv` đã có thì bỏ qua tạo/cài đặt. Lần đầu dùng `--verify`: kéo image ghim digest, thiết lập fixture, kiểm tra 27 bước và persistence/E-learning/logging. Cuối cùng phải hiện `Pinned local release ready`. Không cần Flutter hoặc build source. Các lần sau chỉ mở lại: `.venv/Scripts/python scripts/run_release.py`.

Không dùng `docker compose down -v` vì xóa dữ liệu volume. Test persistence chỉ tạo lại container của project và giữ volume. Lưu ảnh bạn tự chụp vào `evidence/manual/`; bộ kiểm tra tự động có thể ghi lại ảnh ở `evidence/local/`.

## 2. Tài khoản

Mở `.env` trên máy để đọc các khóa dưới đây. Chụp ảnh sau đăng nhập, tránh đưa mật khẩu/token vào báo cáo.

| Giao diện | Username | Khóa mật khẩu trong `.env` |
|---|---|---|
| Keycloak quản trị | Giá trị `KEYCLOAK_ADMIN` | `KEYCLOAK_ADMIN_PASSWORD` |
| Form API bảo vệ | `sv01` hoặc `sv02` | `KEYCLOAK_TEST_PASSWORD` |
| MinIO Console | Giá trị `MINIO_ROOT_USER` | `MINIO_ROOT_PASSWORD` |
| Grafana | Giá trị `GRAFANA_ADMIN_USER` | `GRAFANA_ADMIN_PASSWORD` |
| E-learning giảng viên | `instructor@example.test` | `ELEARNING_INSTRUCTOR_PASSWORD` |
| E-learning sinh viên | `student@example.test` | `ELEARNING_STUDENT_PASSWORD` |

Hai vai trò E-learning trên cùng máy: dùng **một cửa sổ thường và một cửa sổ ẩn danh**. Hai cửa sổ ẩn danh có thể chia sẻ phiên đăng nhập. Đây là tài khoản giả trên Firebase Emulator local.

## 3. Kiểm tra theo thứ tự

Ảnh và JSON tham khảo nằm trong `evidence/local/`.

| Bước / output | Thao tác | Kết quả phải thấy / minh chứng |
|---|---|---|
| 1 — R01, R11 | Docker Desktop → Containers → `myminicloud` | 17 container Running; service có healthcheck là healthy. Exporter/agent không có healthcheck chỉ Running. `R01-stack.json`, `R11-network.json`: 17 service, ping 0% loss. |
| 2 — R02, E01 | http://localhost/ → Blog → mở cả 3 bài | Home, danh sách 3 bài, mỗi bài có ảnh và link quay lại. `R02-home.png`, `E01-blog1.png`… |
| 3 — E02, E09 | Portal → Tải danh sách sinh viên; http://localhost/api/student ; http://localhost/student/ | Đúng 5 bản ghi đủ id/name/major/gpa, dữ liệu API/proxy giống nhau. `E02-student-api.json`, `E09-student-proxy.json`. |
| 4 — R03, R04, E03 | http://localhost/api/hello ; http://localhost/api/notes ; http://localhost/api/students-db | Hello JSON, notes từ SQL, 3 sinh viên SQL. **5 JSON và 3 SQL là hai bộ dữ liệu khác nhau theo đề.** Schema SQL trong `E03-result.png`/`E03-student-database.json`. |
| 5 — R05, E04 | http://localhost/auth/admin/master/console/ → chọn realm_521H0092 → Users | Có sv01/sv02. Clients → flask-app → Settings → Client authentication Off (public client). `E04-realm-users.png`, `E04-public-client.png`. Master realm có sv01 cho bài cơ bản. |
| 6 — E04 | http://localhost/#secure-demo → chọn sv01, nhập mật khẩu → Gọi API có bảo vệ; thử sv02; bấm Gọi không có token | Hợp lệ: HTTP 200, Secure resource OK, username đúng. Thiếu token: **401 là đúng**. Form xóa mật khẩu, không in JWT. `portal-secure-success.png`, `portal-secure-missing-token.png`. |
| 7 — R06, E05 | http://localhost:9001/ → Buckets; http://localhost:9000/profile-pics/avatar.jpg | demo/profile-pics/documents; avatar chữ K công khai. documents chứa PDF riêng tư: ẩn danh 403 là đúng, tải bằng Console sau đăng nhập. `E05-minio-buckets.png`, `E05-minio-avatar.png`. |
| 8 — R07, E06 | `evidence/local/evidence.html` → R07/E06 hoặc chạy check_service_dns.py | 4 bản ghi A; Web 10.10.10.10, App 10.10.10.20. Đây là **IP mẫu zone lab**, không phải IP Docker thực để mở trình duyệt. `E06-dns.json` chứa lệnh dig/kết quả. |
| 9 — R08, E07 | http://localhost:9090/targets ; http://localhost:9090/query | Job node/web UP; web target đúng web-frontend-server:80. Query nginx_up = 1; nginx_http_requests_total tăng khi truy cập. Hai target không phải số container. `E07-web-targets.png`. |
| 10 — R09, E08 | http://localhost:3000/ → đăng nhập → http://localhost:3000/d/system-health-521h0092 | System Health of 521H0092: CPU %, Memory %, Network Traffic. Last 15 minutes, Refresh 10s; đợi ≥2 scrape khi mới chạy. CPU/RAM 0–100%, B/s ≥0. `E08-system-health.png`. |
| 11 — Logging | http://localhost:3000/d/minicloud-service-logs → gọi http://localhost/api/hello → Refresh | Có log HTTP mới, nhãn service MyMiniCloud. Stat là **số dòng log**, không phải số lỗi. `logging-grafana.png`, `service-logging.json`. |
| 12 — E10 | Portal → thử cân bằng tải nhiều lần; hoặc http://localhost/lb/whoami | Body và header X-Backend-Server khớp server1/server2. Test 8 request tuần tự xen kẽ, mỗi server 4 lần. Request đồng thời khác có thể làm thứ tự nhìn thấy khác. `E10-result.png`. |
| 13 — E-learning | http://localhost/elearning/ → instructor → Teaching | Teacher Dashboard, Cloud Computing Lab/CLOUD101, Students: 1 từ Firestore; MiniCloud UI Demo Course/DEMOUI29 đã tạo qua UI. Có thể Create Course với code riêng, semester HK1_2026. `elearning-instructor-courses.png`. |
| 14 — E-learning | Cửa sổ ẩn danh → student → Courses → F5 | Hello Demo Student, CLOUD101, số sinh viên thật; F5 vẫn giữ phiên. `elearning-student-courses.png`, `elearning-demo.json`. |
| 15 — R12, R13, R15 | `evidence/local/evidence.html`, `release-images.json`, Docker Hub | Persistence core5/Firebase/Loki; 6 image tùy chỉnh tag local-20261029.1; 17 runtime image ghim digest. `release-pull-startup.json`: 17 image ID khớp, không build source khi chạy. |

Portal đầy đủ dùng **gateway cổng 80**. Web 8080 chỉ dùng kiểm tra nội dung tĩnh, không thử form API ở đó.

## 4. Lệnh kiểm tra khi cần

```powershell
docker compose ps
.venv/Scripts/python scripts/check_service_dns.py
.venv/Scripts/python scripts/check_network.py
.venv/Scripts/python scripts/check_student_database.py
.venv/Scripts/python scripts/check_round_robin.py --recreate
curl.exe -i http://localhost/lb/whoami
```

Không cần chạy lại full suite nếu chỉ chụp màn hình. Sau test riêng có recreate, `scripts/run_release.py` thống nhất lại image reference theo release.

## 5. Phạm vi số liệu

- CPU/RAM của **Linux VM Docker Desktop**, mạng của namespace Node Exporter; không ghi thành Windows host hay CPU/RAM riêng của 17 container. Dashboard Node Exporter Full có thể có Root FS N/A; ba panel bắt buộc trên dashboard cá nhân đã có dữ liệu thật.
- Loki chỉ thu project myminicloud. Retention 24h, xóa theo chu kỳ compactor. Loki persistence đã thử; volume Alloy có cấu hình nhưng resume positions chưa có bài test riêng.
- E-learning main `9e9ebd539c7f08092ea6855c9aceafe645bd28e0`, Auth/Firestore/Storage Emulator `demo-minicloud`. Hai vai trò, đọc/tạo khóa học, số ghi danh, F5 đã thử. Google Sign-In, Cloud Functions, link preview và chức năng gốc khác chưa được xác nhận.
- 8 named volume: db, keycloak, minio, prometheus, grafana, firebase, loki, alloy. Container phụ trợ làm tổng số thành 17; không cần 17 VM.

## 6. Hồ sơ

- [Bàn giao công việc](BAN_GIAO_GEMINI.md), [trạng thái theo đề](TIEN_DO_OUTPUT.md). File tổng hợp output cuối sẽ được tạo trong task G04.
- [PDF báo cáo](report/BaoCao_Local_521H0092.pdf), [DOCX](report/BaoCao_Local_521H0092.docx).
- [Video local](report/Demo_Local_521H0092.webm), [trang xem](report/Demo_Local_521H0092.html).
- [Minh chứng đọc được](evidence/local/evidence.html).

R14 (EC2) và phần cloud của R16–R18 còn chờ sau khi bạn kiểm tra local. Local không thay thế bằng chứng EC2/public IP trong đề.
