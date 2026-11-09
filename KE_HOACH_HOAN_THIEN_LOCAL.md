# Kế hoạch hoàn thiện local trước khi thuê EC2

> **Ưu tiên mới nhất 09/11:** giao [G11 gỡ bỏ E-learning](handoff/G11_REMOVE_ELEARNING.md) ngay; gỡ active source/config/caller, giữ Git history/volume và bảo toàn các bài test đề. Sau G11: review prototype → G05 → G10 → G06 → G07 → G08 → G09 → G02/G03/G04 → QA cuối → duyệt local → AWS. [Phạm vi Portal/Blog riêng](PHAM_VI_CHOT_PORTAL_VA_BLOG.md) không thay đổi; G01 đã đạt, task mới chưa tính DAT.

> **Điều phối mới 02/11/2026:** Codex làm leader/tester, Gemini thực hiện từng task theo [BAN_GIAO_GEMINI.md](BAN_GIAO_GEMINI.md). Baseline `fefd263` có minh chứng 29/10: 14/18 nhóm tổng thể DAT, 10/10 mở rộng, 17 container/9 vai trò. Tại lần rà soát ban đầu ngày 02/11, Docker engine chưa kết nối; phiên review sau đó của Codex ghi nhận Docker 29.0.1 và 17 container đều đang Up, tuy nhiên chưa chạy lại full suite mới nên tiếp tục giữ nguyên giá trị minh chứng lịch sử ngày 29/10. Ưu tiên còn lại: G01 đồng bộ trạng thái → G02 báo cáo → G03 video → G04 tổng hợp → Codex QA cuối → người dùng kiểm tra → AWS. Kế hoạch này được đồng bộ ở task G01: tách rõ các việc đã hoàn thành (E01–E10, E-learning, logging, release) khỏi các việc còn lại (G01–G04, QA, duyệt local và AWS).

Cập nhật lần đầu: **27/10/2026**, đồng bộ trạng thái: **02/11/2026**. Nguồn tiêu chí: `Báo Cáo Cuối Kỳ.docx.pdf`, đối chiếu trang và chi tiết tại `KE_HOACH_MINICLOUD_2_NGAY.md`. Trạng thái kiểm thử cập nhật trong [TIEN_DO_OUTPUT.md](TIEN_DO_OUTPUT.md).

## 1. Đích bàn giao và thứ tự

1. Giữ phần bắt buộc local đã kiểm thử, sửa mọi lỗi hồi quy trước.
2. Hoàn tất **10/10 mở rộng**, có kiểm thử và minh chứng từng mục.
3. Hoàn thiện Web demo, image Docker Hub, bộ dựng lại, báo cáo và video local.
4. Người dùng kiểm tra bản cuối, xem bảng đã đạt/cần fix/chưa làm và xác nhận local đạt.
5. Sau xác nhận đó mới triển khai AWS EC2 Ubuntu; kiểm thử public IP và bổ sung hồ sơ cloud.

Hiện tại theo baseline ngày 29/10 (`fefd263`): đã có **14/18 nhóm bắt buộc đạt** và **10/10 mở rộng đạt** theo minh chứng lưu tại `evidence/local/`. Kiến trúc hoàn chỉnh gồm **17 container / 9 vai trò server / 8 named volume** (với 3 container Web riêng biệt: container Web chính `web-frontend-server` và hai replica `web-frontend-server1`, `web-frontend-server2`; các service/container có restart policy `unless-stopped`; 8 named volume lưu trữ dữ liệu bền vững), 6 custom image trên Docker Hub và release ghim digest `local-20261029.1`. R14 chưa đạt (AWS chờ người dùng xác nhận local trước); R16–R18 giữ trạng thái `CHO_KIEM_THU` (báo cáo và video đang cập nhật ở task G02/G03, phần cloud còn thiếu). Lần rà soát ban đầu Docker engine chưa kết nối; phiên review Codex ghi nhận Docker 29.0.1 và 17 container Up nhưng chưa có kết quả full suite mới, do đó giữ nguyên kết quả lịch sử 29/10. Hoàn tất local không đồng nghĩa hoàn tất toàn bộ đề.

## 2. Chọn ứng dụng demo từ phần đã có

**Phương án hiện hành:** Portal chỉ quan sát/kiểm thử hạ tầng; Blog là website demo riêng, giữ Flask/MariaDB/Keycloak/MinIO và dữ liệu E02/E03. G11 gỡ active source/config/caller E-learning theo yêu cầu mới. Các đoạn khảo sát/tích hợp phía dưới là lịch sử giai đoạn trước; giữ Git history và volume dữ liệu, không giữ app trong luồng mặc định.

Các repo đã khảo sát ban đầu:

| Repo / branch | Quan sát thực tế | Kết luận sử dụng |
|---|---|---|
| Coffee Shop / `main` @ `328341f` | React; backend Express chỉ trả Hello; chưa có MongoDB trong bản này | Không dùng main làm bản ứng dụng đầy đủ |
| Coffee Shop / `feat/Customer-update` @ `1f84c7c` | Có Mongoose, API auth/product/order, seed và Dockerfile; ahead main 40 commit | Có thể tái sử dụng nếu chọn Coffee Shop; chưa build/run. Sửa URL localhost, routing, seed và log URI trước |
| E-learning / `main` @ `9e9ebd5` | Flutter + Firebase Auth/Firestore/Storage; README xác nhận bỏ backend Node cũ; `flutter pub get` và `flutter build web --release --no-pub` đều thành công trên Flutter 3.35.7 / Dart 3.9.2 | Có thể dùng artifact Web. Cảnh báo Wasm dry-run không làm thất bại bản JavaScript Web |
| E-learning / `management_system` @ `9eccf47` | Ahead main 12 commit, có commit sửa deployment; đã đọc source và đối chiếu lịch sử | Là branch mới hơn để đối chiếu khi nhập; chưa build branch này, không tự coi tốt hơn bản main đã build |

Minh chứng khảo sát ban đầu: [source-audit-elearning.json](evidence/local/source-audit-elearning.json).

**Tình trạng tích hợp hiện hành (ngày 29/10/2026):**
Nhánh `feat/elearning-web-demo` đã hoàn tất tích hợp vào stack: Flutter Web được đóng gói vào image `katie217/myminicloud-elearning:local-20261029.1` (container `elearning-web-server`), Nginx gateway phục vụ tại `/elearning/` với base path đúng. Dữ liệu chạy bằng Firebase Emulator riêng (`katie217/myminicloud-firebase:local-20261029.1`, container `firebase-emulator-server`) trong mạng `cloud-net` với volume `firebase-data` lưu trữ; không dùng Firebase cloud thật. Đã kiểm thử hai vai trò giảng viên/sinh viên, xem và tạo khóa học, hiển thị số ghi danh thật và kiểm tra persistence sau restart (minh chứng `evidence/local/elearning-demo.json`, `evidence/local/elearning-persistence.json`). Emulator không thay thế Keycloak/MariaDB/MinIO của bài làm. Các chức năng ngoài luồng demo của đồ án gốc chưa kiểm chứng.

## 3. Kiến trúc cần giữ đúng đề

- Giữ đủ 9 vai trò server theo đề:
  1. **Web Frontend Server**: Nginx tĩnh + 3 bài blog + demo portal; gồm 3 container Web riêng biệt: container Web chính (`web-frontend-server`, host port 8080) và hai replica (`web-frontend-server1`, `web-frontend-server2`) phục vụ cân bằng tải round robin qua API Gateway.
  2. **Application Backend Server**: Flask REST API (`application-backend-server`), host port 8085; cung cấp `/hello`, `/notes`, `/student`, `/secure`.
  3. **Relational Database Server**: MariaDB (`relational-database-server`), volume `db-data`; lưu `minicloud.notes` và `studentdb.students`.
  4. **Authentication & Identity Server**: Keycloak (`authentication-identity-server`), host port 8081, volume `keycloak-data`; realm `realm_521H0092`, user sv01/sv02, public client `flask-app`.
  5. **Object Storage Server**: MinIO (`object-storage-server`), host ports 9000/9001, volume `minio-data`; buckets `demo`, `profile-pics` (avatar.jpg công khai), `documents` (PDF báo cáo).
  6. **Internal DNS Server**: Bind9 (`internal-dns-server`), host port 1053, cổng 53 nội bộ; phân giải tên miền `.cloud.local` cho các server.
  7. **Monitoring & Alerting Server**: Prometheus (`monitoring-prometheus-server`), host port 9090, volume `prometheus-data`; scrape jobs `node` và `web`.
  8. **Metrics Visualization Server**: Grafana (`monitoring-grafana-dashboard-server`), host port 3000, volume `grafana-data`; provision dashboard `System Health of 521H0092` và `MyMiniCloud Service Logs`.
  9. **API Gateway & Reverse Proxy Server**: Nginx Gateway (`api-gateway-proxy-server`), host port 80; reverse proxy `/`, `/blog/`, `/api/`, `/student/`, `/auth/`, `/lb/`, `/elearning/`.
- Container hỗ trợ:
  - `monitoring-node-exporter-server`: Node Exporter, host port 9100.
  - `monitoring-web-exporter-server`: Nginx Prometheus Exporter, cổng 9113 nội bộ.
  - `elearning-web-server`: Flutter Web demo tại `/elearning/`.
  - `firebase-emulator-server`: Firebase Auth & Firestore Emulator, volume `firebase-data`.
  - `logging-loki-server`: Grafana Loki lưu trữ log dịch vụ tập trung, volume `loki-data`.
  - `logging-alloy-server`: Grafana Alloy thu thập Docker logs, volume `alloy-data`.
- Cấu hình restart và lưu trữ:
  - Các service/container được thiết lập restart policy `restart: unless-stopped`.
  - Hệ thống sử dụng 8 named volume để lưu trữ dữ liệu bền vững qua các lần recreate: `db-data`, `keycloak-data`, `minio-data`, `prometheus-data`, `grafana-data`, `firebase-data`, `loki-data`, `alloy-data`.
- Mạng: `cloud-net` (bridge).

## 4. Phân công và lộ trình thực hiện

### 4.1. Các chức năng mở rộng và tích hợp đã hoàn thành (Baseline 29/10 `fefd263`)

Mỗi chức năng đã được phát triển trên một branch riêng bắt đầu từ main, kiểm thử và tích hợp:

| Chức năng | Branch thực thi | Commit tích hợp | Kết quả nghiệm thu |
|---|---|---|---|
| E02 JSON student API | `feat/student-json-api` | `9b4d11d` | DAT — `evidence/local/E02-student-api.json` |
| E03 student SQL database | `feat/student-sql-database` | `64e5f99` | DAT — `evidence/local/E03-student-database.json` |
| E09 student gateway route | `feat/student-proxy-route` | `6b69d0c` | DAT — `evidence/local/E09-student-proxy.json` |
| E01 blog cá nhân | `feat/personal-blog` | `c377c25` | DAT — `evidence/local/E01-blog.json` |
| Giao diện cổng demo | `feat/demo-portal` | `0f1d42d` | DAT — UI demo portal kết nối các service |
| E04 Keycloak realm/token | `feat/student-identity` | `0816e1b` | DAT — `evidence/local/E04-keycloak.json` |
| E04 Secure demo portal | `feat/secure-api-demo` | `e276d1f` | DAT — Portal test OIDC login và gọi /secure |
| E05 avatar/documents | `feat/profile-object-storage` | `d119e03` | DAT — `evidence/local/E05-storage.json` |
| E06 DNS mở rộng | `feat/service-dns-records` | `8f1b6be` | DAT — `evidence/local/E06-dns.json` |
| E07 Web metrics | `feat/web-metrics` | `ac394ac` | DAT — `evidence/local/E07-web-metrics.json` |
| E08 dashboard cá nhân | `feat/personal-health-dashboard` | `45f3a25` | DAT — `evidence/local/E08-system-health.json` |
| E10 round robin | `feat/round-robin-balancing` | `1f27f82` | DAT — `evidence/local/E10-round-robin.json` (FIX-005) |
| Flutter E-learning demo | `feat/elearning-web-demo` | `ec74016` | DAT — `evidence/local/elearning-demo.json`, persistence |
| Centralized service logs | `feat/centralized-service-logs` | `a249748` | DAT — `evidence/local/service-logging.json` |
| Release image ghim digest | `chore/local-release-images` | `de99b36` | DAT — `evidence/local/release-images.json` |
| Baseline kiểm thử local | `test/final-local-verification` | `fefd263` | DAT — bộ 27 bước chạy bằng `python scripts/check_all.py --screenshots` (`evidence/local/local-suite.json`); các bài test persistence và E-learning là kiểm tra bổ sung riêng |
| Bàn giao điều phối Codex | `docs/gemini-work-handoff` | `fd0b4e6` | DAT — Kế hoạch bàn giao và audit |

### 4.2. Kế hoạch công việc hiện hành (bổ sung UI ngày 09/11)

Theo [phạm vi chốt](PHAM_VI_CHOT_PORTAL_VA_BLOG.md), G01 đã đạt; làm G11 trước, rồi review prototype → G05 → G10 → G06 → G07 → G08 → G09 → G02/G03/G04. Review từng task trước tích hợp; không làm hồ sơ cuối dựa trên giao diện còn sắp sửa.

| Thứ tự / Task | Branch thực thi | Phạm vi thực hiện | Tiêu chí nghiệm thu |
|---|---|---|---|
| G01 Đồng bộ trạng thái | `docs/reconcile-local-status` | `TIEN_DO_OUTPUT.md`, `KE_HOACH_HOAN_THIEN_LOCAL.md`, `handoff/G01.md` | Đếm DAT đúng 14 R / 10 E; R14 chờ, R16–R18 CHO_KIEM_THU; mô tả đúng cụm 3 container Web (Web chính + 2 replica) và 8 named volume; dẫn chứng FIX-005; UTF-8 và git diff --check đạt |
| G05 Blog học thuật dạng card | `feat/personal-blog` fast-forward từ main | Blog index, 3 bài chi tiết, ảnh/CSS scope riêng, test và ảnh E01 | Card ảnh trái/chữ phải; mobile stack dọc; HTTP 200/ảnh/link; không hồi quy Home; nội dung theo PDF tr.21 |
| G10 Tách hai frontend | `feat/separate-portal-blog-sites` | Portal source/assets và website Blog Home riêng; gateway/URL | Portal chỉ có card mở Blog, không nội dung bài; Web Home/Blog HTTP 200, route cũ vẫn đạt |
| G06 API số liệu Portal | `feat/portal-metrics-api` | Endpoint Flask `/dashboard`, test số liệu/lỗi | Prometheus thật, query cố định, timeout/units/null đúng; route cũ giữ đúng contract |
| G07 Dashboard Portal | `feat/portal-health-dashboard` | KPI, biểu đồ live, refresh, card 9 vai trò | Dữ liệu thật, thiếu/lỗi rõ; desktop/mobile; chỉ card mở Blog riêng, không E-learning |
| G08 Giao diện gọi API | `feat/api-console-interface` | Card/bảng/trạng thái response, secure, RR | Response khớp API; status/time thật; 200/401; không lộ token; RR count từ request thật |
| G11 Gỡ bỏ E-learning — ưu tiên đầu | `chore/retire-elearning-demo` | handoff/G11_REMOVE_ELEARNING.md; gỡ active source/config/caller, release candidate gọn | Giữ Git history/volume; đủ 9 vai trò và E01–E10; test/digest/số lượng thực tế; không đè release cũ |
| G09 Release UI | `chore/ui-release-images` — Codex | Regression, tag/digest mới, pull/start, hướng dẫn chạy | Preview source khớp image release mới; giữ release cũ; số bước test ghi theo runner thực tế |
| G02 Báo cáo release cuối | `docs/refresh-local-report` | `report/BaoCao_Local_521H0092.md`, PDF/DOCX/HTML, `report/architecture.*`, `scripts/build_report.py` | Đủ 5 chương + phụ lục theo PDF trang 3; kiến trúc đúng 17 container/9 vai trò/8 volume; nhúng ảnh thật đọc được từng server; verify hash PDF MinIO |
| G03 Video local release | `docs/refresh-local-video` | `scripts/record_demo.py`, `report/Demo_Local_521H0092.webm/.html`, `evidence/local/demo-chapters.json` | Video 17 container xem được, đủ cảnh E-learning, logging, OIDC secure (không lộ secret); sinh chapters JSON từ cảnh quay thực tế; R17 giữ CHO_KIEM_THU |
| G04 Tổng hợp đầu ra | `docs/local-output-handoff` | Tạo `TONG_HOP_OUTPUT_LOCAL.md`; cập nhật `README.md`, `HUONG_DAN_TEST_LOCAL.md`, tracker | Danh mục toàn bộ output, bảng URL/tài khoản (không mật khẩu), hướng dẫn chạy release, link và digest |
| Codex QA cuối | `test/final-local-handoff` | Codex chạy độc lập suite 27 bước (`python scripts/check_all.py --screenshots`), persistence test, luồng E-learning, hash PDF, Docker Hub digest | Toàn bộ 27 bước đạt, volume giữ dữ liệu qua recreate, E-learning hoạt động, không hồi quy |
| Người dùng kiểm tra | Phụ thuộc người dùng | Xem bảng output, kiểm tra UI bản cuối | Người dùng xác nhận local đạt trước khi chuyển sang AWS |
| L10 Triển khai AWS EC2 | `chore/cloud-deployment` | Thuê EC2 Ubuntu, chạy stack, test public IP, bổ sung hồ sơ cloud R14/R16–R18 | Full stack EC2, public IP, hoàn thiện R14, cập nhật báo cáo/video cloud |

## 5. Checklist chi tiết cho 10 mở rộng

| ID / trang PDF | Kết quả bắt buộc cần xác minh | Minh chứng thực tế đã lưu |
|---|---|---|
| E01 / 21 | Đúng 3 file blog, mỗi bài có ảnh, link quay lại và danh sách hyperlink | `evidence/local/E01-blog.json`; ảnh trang danh sách và 3 bài |
| E02 / 22 | File students.json đúng 5 bản ghi id/name/major/gpa; Flask /student; proxy /api/student | `evidence/local/E02-student-api.json` |
| E03 / 23 | studentdb.students: id INT auto primary; student_id VARCHAR(10); fullname VARCHAR(100); dob DATE; major VARCHAR(50); >=3 dòng | `evidence/local/E03-student-database.json` gồm schema và query |
| E04 / 23–24 | Realm MSSV, sv01/sv02, public client flask-app, token và secure resource đúng username | `evidence/local/E04-keycloak.json` đã che bí mật; ảnh realm/users/client; export cấu hình |
| E05 / 24 | profile-pics/avatar.jpg đọc công khai; documents chứa PDF báo cáo cuối | `evidence/local/E05-storage.json`; ảnh bucket/object; URL avatar; hash PDF |
| E06 / 25 | app-backend.cloud.local = 10.10.10.20; thêm minio/keycloak; giữ bản ghi Web | `evidence/local/E06-dns.json`; zone file Bind9 |
| E07 / 25 | Job web đúng target web-frontend-server:80, UP, metrics thật | `evidence/local/E07-web-metrics.json`; Targets screenshot; Nginx exporter |
| E08 / 25–26 | System Health of 521H0092, CPU%, Memory, Network có dữ liệu; export/lưu dashboard | `evidence/local/E08-system-health.json` và PNG; dashboard JSON |
| E09 / 26 | /student/ qua Nginx trả đúng JSON /student của Flask | `evidence/local/E09-student-proxy.json` |
| E10 / 26–27 | 2 Web replica (thuộc cụm 3 container Web), round robin, kết quả luân phiên có nhận diện backend | `evidence/local/E10-round-robin.json`; upstream config; xử lý FIX-005 |

IP DNS 10.10.10.x là bản ghi ví dụ của đề trong lab Bind9, không phải Docker IP thực. Kiểm tra DNS xác minh dig đạt; kết nối liên dịch vụ dùng mạng nội bộ `cloud-net` và service name Docker.

## 6. Kiểm thử bản local cuối và chuẩn bị EC2 khi chưa thuê server

- Bộ kiểm thử tích hợp 27 bước chạy bằng lệnh `python scripts/check_all.py --screenshots` kiểm tra toàn bộ luồng chức năng, UI, OIDC, DNS, MinIO, metrics, logging và cân bằng tải. Các bài kiểm tra persistence dữ liệu (Core5, Firebase, Loki) và luồng E-learning demo là các bài kiểm tra bổ sung độc lập, không nằm hết trong bộ 27 bước này.
- Test persistence: xác minh dữ liệu MariaDB, Keycloak, MinIO, Prometheus, Grafana, Firebase, Loki sau khi recreate container; không dùng `down -v` hoặc xóa volume dữ liệu.
- Tách bạch minh chứng: `evidence/local/` lưu kết quả local; `evidence/ec2/` sẽ lưu kết quả chạy trên AWS EC2 sau này; không ghi đè lẫn nhau.
- Node Exporter trên Docker Desktop đo Linux VM và network theo exporter namespace; các giới hạn đo lường được ghi chú rõ ràng trong hồ sơ.
- File cấu hình mẫu `.env.example` cung cấp cấu trúc cấu hình; `.env` thật chứa thông tin môi trường local không commit lên Git.
- Tuyệt đối không tạo hoặc truy cập tài nguyên AWS trong giai đoạn hoàn thiện local.

## 7. Tiến độ dự kiến cho phần việc còn lại

Ước lượng dưới đây là phần hồ sơ đã lập trước đợt UI ngày 09/11; chưa bao gồm G05–G09. Chưa chốt thời gian UI cho đến khi nghiệm thu lát cắt đầu G05. Đây không phải cam kết giờ hoàn tất hoặc triển khai AWS trước duyệt local.

| Task / Khối | Thời gian dự kiến | Đầu ra chính |
|---|---|---|
| G01 | 1 giờ | Đồng bộ `TIEN_DO_OUTPUT.md` và `KE_HOACH_HOAN_THIEN_LOCAL.md` (hoàn thành trong task này) |
| G02 | 2–3 giờ | Báo cáo cuối 5 chương, sơ đồ 17 container/9 vai trò/8 volume, nhúng ảnh thật từng server |
| G03 | 2–3 giờ | Kịch bản `record_demo.py`, quay video WebM 17 container, chapters JSON |
| G04 | 1–2 giờ | `TONG_HOP_OUTPUT_LOCAL.md`, cập nhật README và hướng dẫn test |
| Codex QA cuối | 1–2 giờ | Chạy bộ test độc lập 27 bước (`check_all.py --screenshots`), persistence, PDF hash khi Docker engine sẵn sàng |
| Duyệt local | Phụ thuộc người dùng | Người dùng kiểm tra giao diện và xác nhận local đạt |
| L10 (AWS EC2) | 3–4 giờ | Triển khai EC2 Ubuntu sau khi duyệt local, hoàn thiện R14 và hồ sơ cloud |

## 8. Gói người dùng kiểm tra trước AWS

- README chỉ rõ lệnh setup/run/test và các URL demo; bảng service/port khớp cấu hình release cuối.
- Từng output local có trạng thái, branch/commit, lệnh kiểm thử và minh chứng trong [TIEN_DO_OUTPUT.md](TIEN_DO_OUTPUT.md).
- Không còn lỗi khiến output local bắt buộc hoặc mục mở rộng đã công bố đạt bị trượt; các giới hạn được ghi rõ.
- Báo cáo đủ 5 chương + phụ lục, thống kê đúng số mở rộng; video xem được và link truy cập phù hợp cách nộp bài.
- Docker Hub có 6 image custom ghim digest; source/config đủ dựng lại; secrets và volume không ở Git.
- Liệt kê riêng: phần AWS chưa làm, hồ sơ cloud cần bổ sung, MSSV Diệp Yến Nhi còn thiếu (avatar chữ K đã duyệt).
- Người dùng kiểm tra và xác nhận local đạt, sau đó mới thuê EC2 và bắt đầu L10.

## 9. Quy ước theo dõi và commit

- Trạng thái: `CHUA_LAM` → `DANG_LAM` → `CHO_KIEM_THU` → `DAT`; lỗi quan sát được ghi `CAN_FIX`; phụ thuộc bên ngoài ghi `CHO_THONG_TIN`.
- Commit tiếng Anh, format `<type>: <summary>`, phần summary 4–5 từ sau tiền tố, ví dụ `docs: correct status review findings`.
- Review diff → kiểm thử liên quan → cập nhật tracker → commit file liên quan; không đưa secrets, file tạm ngoài project hoặc dữ liệu thật vào commit.
