# Bảng theo dõi output MyMiniCloud

> **Rà soát & đồng bộ 02/11/2026 (Task G01):** bảng R/E hiện có 14 nhóm bắt buộc DAT và 10/10 mở rộng DAT theo minh chứng lịch sử ngày 29/10, baseline `fefd263`. Tại lần rà soát ban đầu ngày 02/11/2026, Docker engine chưa kết nối được; trong phiên review sau đó của Codex ghi nhận Docker 29.0.1 đã kết nối và 17 container đang Up, tuy nhiên chưa chạy lại full suite mới nên trạng thái kiểm thử chức năng ngày 02/11 vẫn ghi NOT_RUN và giữ nguyên giá trị minh chứng lịch sử ngày 29/10. Kế hoạch hoàn thiện bản local gồm G01 (đồng bộ trạng thái), G02 (cập nhật báo cáo 17 container), G03 (quay lại video walkthrough) và G04 (tổng hợp bàn giao) theo [BAN_GIAO_GEMINI.md](BAN_GIAO_GEMINI.md). Codex review và kiểm thử độc lập trước khi tích hợp từng branch. AWS EC2 (R14) và hồ sơ cloud vẫn chờ người dùng kiểm tra và xác nhận bản local đạt trước khi triển khai.

Cập nhật lần đầu: **26/10/2026**, cập nhật kế hoạch **27/10/2026**, đồng bộ trạng thái **02/11/2026**. Nguồn yêu cầu: `Báo Cáo Cuối Kỳ.docx.pdf`. Tiêu chí theo trang: `KE_HOACH_MINICLOUD_2_NGAY.md`; thứ tự triển khai hiện hành: [KE_HOACH_HOAN_THIEN_LOCAL.md](KE_HOACH_HOAN_THIEN_LOCAL.md). Kế hoạch bắt buộc cũ lưu giai đoạn nền tảng đã thực hiện.

## 1. Tổng quan hiện tại

- **Output bắt buộc đạt: 14/18** nhóm trong bảng mục 3. Đây là cách chia nhóm để quản lý, không phải cách chia điểm của PDF.
- **Mở rộng đạt: 10/10** mục trong bảng mục 7 theo minh chứng lịch sử ngày 29/10 (baseline `fefd263`).
- Các service local được triển khai và kiểm thử theo từng branch chức năng độc lập; chỉ các dòng `DAT` có minh chứng JSON/ảnh mới được tính hoàn thành.
- Git local có `main` và các branch chức năng riêng theo quy định, kết nối repo `https://github.com/Katie-217/MiniCloud`; lịch sử tài liệu ban đầu và các commit nền tảng được giữ nguyên.
- Đã thêm `.gitignore` loại trừ bí mật, dữ liệu runtime và file trích PDF; `.gitattributes` thống nhất line ending cho file container Linux.
- Đã kết nối `https://github.com/Katie-217/MiniCloud`, giữ README và lịch sử remote; đã push branch nền tảng. Nhóm: Võ Thị Thiên Kim — 521H0092; Diệp Yến Nhi — chờ MSSV. Docker Hub namespace: `katie217`.
- Quy ước commit: commit message tiếng Anh, tiền tố phù hợp (`feat`, `fix`, `chore`, `test`, `docs`) và thông điệp chính 4–5 từ sau tiền tố. AWS để sau theo yêu cầu người dùng; tiếp tục toàn bộ công việc local không phụ thuộc AWS.
- Docker CLI/Compose: phiên bản server ghi nhận Docker **29.0.1**. Tại lần rà soát ban đầu ngày 02/11/2026, Docker Desktop Linux engine chưa kết nối được; phiên review của Codex ghi nhận Docker 29.0.1 và 17 container đều đang Up, nhưng chưa có kết quả full suite mới. Các container MyMiniCloud được quản lý độc lập, không dừng container project khác.
- **Kết quả local hiện hành:** Toàn bộ chức năng cơ bản và 10 mở rộng đã kiểm thử đạt; hệ thống chạy trên kiến trúc **17 container / 9 vai trò server / 8 named volume**, mạng nội bộ `cloud-net`. Kiến trúc Web gồm 3 container Web riêng biệt: container Web chính `web-frontend-server` và hai replica `web-frontend-server1`, `web-frontend-server2` phục vụ cân bằng tải round robin qua Nginx gateway. Toàn bộ service/container được cấu hình restart policy `unless-stopped`; 8 named volume lưu trữ dữ liệu bền vững. 6 custom image trên Docker Hub (`myminicloud-web`, `myminicloud-app`, `myminicloud-minio`, `myminicloud-elearning`, `myminicloud-firebase`, `myminicloud-tools`) được ghim digest đầy đủ trong release `local-20261029.1` (`evidence/local/release-images.json`). Bộ kiểm thử tích hợp 27 bước thực hiện bởi `python scripts/check_all.py --screenshots` đã đạt (`evidence/local/local-suite.json`); các bài kiểm tra persistence dữ liệu và E-learning demo là các bài kiểm tra bổ sung riêng, không nằm hết trong bộ 27 bước này.
- **Ứng dụng E-learning và logging tập trung đã tích hợp:** Ghép Flutter Web demo phục vụ tại `/elearning/` với Firebase Emulator nội bộ có dữ liệu mẫu và persistence; logging tập trung gồm Loki lưu volume `loki-data` và Alloy thu log Docker, có dashboard Grafana `MyMiniCloud Service Logs`.
- **Hồ sơ local đang hoàn thiện bản cuối:** Đã có báo cáo (PDF 18 trang, DOCX, Markdown) và video (75,68s, 14 cảnh) của giai đoạn nền tảng ban đầu; hiện đang thực hiện task G02 (cập nhật báo cáo 17 container, nhúng ảnh thật đọc được từng server) và G03 (quay lại video walkthrough đầy đủ 17 container và các luồng demo mới); tổng hợp ở G04. Do đó, các mục R16, R17, R18 giữ trạng thái `CHO_KIEM_THU`.
- **Chưa hoàn tất toàn đề:** EC2/public IP và bằng chứng cloud (R14 `CHO_THONG_TIN` — người dùng yêu cầu chỉ triển khai sau khi nghiệm thu local); bổ sung MSSV Diệp Yến Nhi; hoàn thiện hồ sơ local cuối (G02/G03/G04); bổ sung hồ sơ cloud sau khi chạy EC2.
- **Thứ tự thực hiện:** Hoàn tất local và 10 mở rộng, Docker Hub/hồ sơ (G01–G04) → Codex QA cuối độc lập → người dùng kiểm tra bản cuối → mới thuê và triển khai EC2. Tuyệt đối chưa thao tác AWS.
- **Minh chứng khảo sát và tích hợp E-learning:** Khảo sát Flutter Web main `9e9ebd5` tại [source-audit-elearning.json](evidence/local/source-audit-elearning.json). Tích hợp hoàn tất ngày 29/10 trên branch `feat/elearning-web-demo`: image Flutter Web và Firebase Emulator riêng, login 2 vai trò, xem/tạo khóa học, đếm sinh viên ghi danh và persistence sau recreate; minh chứng `evidence/local/elearning-demo.json`, `evidence/local/elearning-persistence.json`. Không sử dụng Firebase cloud thật.

## 2. Quy ước trạng thái

- `CHUA_LAM`: chưa thực hiện.
- `DANG_LAM`: đang triển khai.
- `CHO_KIEM_THU`: đã có code/config nhưng chưa có kết quả test đủ điều kiện.
- `CAN_FIX`: test không đạt hoặc có lỗi đã xác nhận.
- `DAT`: đã kiểm thử đúng tiêu chí và có minh chứng.
- `CHO_THONG_TIN`: phụ thuộc thông tin/tài khoản/môi trường chưa sẵn sàng.

Không lấy trạng thái container Running thay cho kết quả kiểm thử chức năng. Local đạt không tự động có nghĩa EC2 đạt.

## 3. Output bắt buộc

| ID | Output cần đạt / căn cứ PDF | Branch phụ trách | Trạng thái | Minh chứng / commit |
|---|---|---|---|---|
| R01 | Compose khởi động toàn hệ thống; `cloud-net`, container name, cổng, restart đúng — tr. 1–3 | `chore/project-foundation` + các nhóm tích hợp | DAT | evidence/local/R01-stack.json; 17 running/healthy containers / 9 server roles; commit `1f9f77b` / `fefd263` |
| R02 | Home và `/blog/` HTTP 200, nội dung đúng — tr. 12–13 | `feat/web-api-database` | DAT | evidence/local/R02-web.json; Home + Blog; commit `a28234e` |
| R03 | `/hello` trực tiếp và qua proxy trả JSON đúng — tr. 13 | `feat/web-api-database` + `feat/gateway-network-tests` | DAT | evidence/local/R03-api.json; direct + proxy; commit `35f3502` |
| R04 | `minicloud.notes` có bảng và dữ liệu khởi tạo — tr. 6, 14 | `feat/web-api-database` | DAT | evidence/local/R04-database.json; commit `ea51eb3` |
| R05 | Keycloak admin đăng nhập được, tạo user sv01 — tr. 14–15 | `feat/identity-storage-dns` | DAT | evidence/local/R05-auth.json; R05-keycloak-admin.png; R05-keycloak-user.png; commit `22e8a99` |
| R06 | MinIO bucket demo, upload và tải file được — tr. 2, 15–16 | `feat/identity-storage-dns` | DAT | evidence/local/R06-storage.json; R06-minio-bucket.png; R06-minio-object.png; commit `2114441` |
| R07 | DNS Web trả `10.10.10.10` bằng dig — tr. 16–17 | `feat/identity-storage-dns` | DAT | evidence/local/R07-dns.json; dig internal 53 + published host 1053; commit `41e7815` |
| R08 | Prometheus node target UP, query metric có dữ liệu — tr. 17–18 | `feat/monitoring-dashboard` | DAT | evidence/local/R08-monitoring.json; commit `435dc43` |
| R09 | Grafana datasource hoạt động, CPU/RAM/Network có dữ liệu — tr. 18–19 | `feat/monitoring-dashboard` | DAT | evidence/local/R09-grafana.json; R09-grafana-dashboard.png; R09-grafana-network.png; commit `25d4a51` |
| R10 | Proxy `/`, `/api/`, `/auth/` hoạt động, đúng status/redirect — tr. 19–20 | `feat/gateway-network-tests` | DAT | evidence/local/R10-gateway.json; Web/App/Auth + correct public OIDC issuer; commit `35f3502` |
| R11 | Các server thông mạng, có log ping và network membership — tr. 20 | `feat/gateway-network-tests` | DAT | evidence/local/R11-network.json; ping 3 packets for each of 17 services, 0% loss; commit `1f9f77b` |
| R12 | Volume cần thiết lưu được dữ liệu, restart policy đầy đủ — tr. 3 | Các nhóm service + `feat/gateway-network-tests` | DAT | evidence/local/R12-persistence.json; custom data preserved across all 5 stateful service recreations; commit `5967fba` |
| R13 | Ít nhất 1 image tùy chỉnh trên Docker Hub, có link/tag — tr. 3 | `chore/image-publication` | DAT | evidence/local/release-images.json; chore/local-release-images; 6 custom images pushed and manifests verified; commit `431197d` |
| R14 | Toàn hệ thống chạy trên EC2 Ubuntu, public IP và test server đạt — tr. 1, 3 | `chore/cloud-deployment` | CHO_THONG_TIN | AWS deferred by user; no EC2 resources created/accessed |
| R15 | Dockerfile/Compose/config và source đủ để tái tạo — tr. 3 | Toàn bộ branch triển khai | DAT | evidence/local/R15-source.json; pinned pull release + source/config/build instructions present |
| R16 | Báo cáo đủ 5 chương + phụ lục, thống kê mở rộng — tr. 3, 27 | `docs/submission-evidence` | CHO_KIEM_THU | report/BaoCao_Local_521H0092.md/.pdf/.docx: bản local 17 container đang refresh ở task G02; chờ EC2 và MSSV thành viên hai; commit `503a61a` |
| R17 | Video demo và link truy cập được trong phụ lục — tr. 3 | `docs/submission-evidence` | CHO_KIEM_THU | report/Demo_Local_521H0092.webm: bản local walkthrough đang refresh ở task G03; cloud demo pending; commit `f3e3c15` |
| R18 | Ảnh từng server, log test; phân biệt local và EC2 — tr. 3 | Từng branch + `docs/submission-evidence` | CHO_KIEM_THU | evidence/local: đủ ảnh/log từng server, network, persistence, Docker Hub; EC2 chưa thực hiện; commit `0d2c665` |

## 4. Những output đã đạt

Portal kiểm thử OIDC qua giao diện: `feat/secure-api-demo`; `scripts/check_secure_portal.py` xác minh sv01/sv02 trả HTTP 200, thiếu token trả 401; ảnh `portal-secure-success.png` và `portal-secure-missing-token.png`. Không hiển thị access token hoặc mật khẩu trong kết quả.

Bộ kiểm thử tích hợp 27 bước: chạy bằng lệnh `python scripts/check_all.py --screenshots` trên branch `test/final-local-verification` (commit `fefd263`); file kết quả `evidence/local/local-suite.json` ghi nhận toàn bộ 27 bước đạt (chức năng cốt lõi R01–R12, 10 mục mở rộng E01–E10, secure portal UI và logging). Các bài kiểm tra persistence dữ liệu (Core5, Firebase, Loki) và luồng tương tác E-learning chuyên sâu là các bài kiểm tra bổ sung độc lập, không nằm hết trong bộ 27 bước này.

Các dòng `DAT` ở bảng mục 3 và 7 là output đã kiểm thử đạt, kèm đường dẫn log/ảnh. Các dòng `CHO_KIEM_THU` (R16–R18) là hồ sơ đang cập nhật bản release cuối tại local và còn thiếu phần cloud. R14 giữ `CHO_THONG_TIN` chờ kiểm tra bản local trước khi tiến hành AWS.

Công việc chuẩn bị đã hoàn thành: đọc PDF, trích yêu cầu/tiêu chí, lập kế hoạch hai ngày và quy trình branch/commit, tạo bảng này. Các công việc đó không được tính thay cho output hệ thống theo đề.

Khi có kết quả, mỗi mục ghi: ID output, môi trường local/EC2, branch/commit, lệnh hoặc thao tác kiểm thử, kết quả thực tế và file minh chứng.

## 5. Vấn đề cần fix và tình trạng xử lý

| ID | Vấn đề | Ảnh hưởng | Hướng xử lý | Trạng thái |
|---|---|---|---|---|
| FIX-001 | Ban đầu Docker CLI không kết nối được `dockerDesktopLinuxEngine` | Đã hết chặn build/chạy container | Kiểm tra lại bằng `docker info --format '{{.ServerVersion}}'`, nhận `29.0.1` | DAT |
| FIX-002 | Chưa có remote GitHub ở lần kiểm tra đầu | Đã hết chặn push branch | Đã fetch, giữ lịch sử và push `chore/project-foundation` lên MiniCloud | DAT |
| FIX-003 | Image/download MinIO được hướng dẫn không còn truy cập được tại lần kiểm tra | Không dựng được storage bằng cách copy image mẫu | Build source chính thức có tag/checksum, giữ license; UI và upload/download đã kiểm thử | DAT |
| FIX-004 | Docker Desktop từ chối root bind mount rslave | Node Exporter không start với cấu hình host mount ban đầu | Dùng root bind read-only mặc định, giữ proc/sys mounts; metric và dashboard có dữ liệu | DAT |
| FIX-005 | Round robin giữ IP cũ của hai Web sau recreate, có thể trỏ nhầm container | E10 không còn bảo đảm đúng backend sau khởi động lại | Dùng `zone web_lb 64k` và resolver nội bộ Docker trong cấu hình Nginx gateway (`feat/round-robin-balancing`). Đã kiểm thử recreate replica trong commit `1f27f82` (`evidence/local/E10-round-robin.json` có `details.verified_after_replica_recreation: true`). Lượt test thường tiếp theo ở `fefd263` ghi nhận trường này `false` do không chạy lại recreate, nhưng xác nhận cân bằng tải 8/8 request giữa 2 web backend. | DAT |

Hiện tại toàn bộ 5 vấn đề kỹ thuật phát hiện trong quá trình triển khai local đã được xử lý đạt (FIX-001 đến FIX-005). Các hạn chế còn lại được ghi rõ ở mục 10; phần AWS và môi trường cloud đang ở hàng chờ theo yêu cầu người dùng.

## 6. Thông tin và setup còn thiếu

| Việc cần làm rõ | Trạng thái | Hành động tiếp theo |
|---|---|---|
| URL repo và quyền làm việc | DAT | Katie-217/MiniCloud; quyền ADMIN; đã push branch |
| MSSV, tên sinh viên/nhóm | DANG_LAM | Có Võ Thị Thiên Kim / 521H0092 và Diệp Yến Nhi; chờ MSSV thành viên thứ hai |
| Username Docker Hub và login local | DAT | Namespace `katie217`; 6 custom image đã push và đọc lại manifest thành công |
| Có EC2 Ubuntu hay chưa | CHO_THONG_TIN | Người dùng yêu cầu để sau; chưa thao tác AWS |
| Public IP, user SSH, đường dẫn key nếu đã có EC2 | CHO_THONG_TIN | Kết nối bằng key local, không đưa nội dung key vào Git/chat |
| Repo ứng dụng demo | DAT | `feat/elearning-web-demo`; source main `9e9ebd5`; hai vai trò, khóa học, số ghi danh và persistence bằng emulator; chức năng ngoài luồng demo chưa kiểm chứng |
| Avatar cá nhân cho E05 | DAT | Người dùng chọn chữ cái đầu tên ngày 29/10/2026; avatar chữ K cho Thiên Kim, nguồn SVG và bản JPEG trong object-storage-server |

## 7. Kết quả 10 mục mở rộng (E01–E10)

| ID | Output mở rộng | Trạng thái | Minh chứng / commit |
|---|---|---|---|
| E01 | Blog 3 bài, mỗi bài có ảnh và link quay lại | DAT | evidence/local/E01-blog.json; feat/personal-blog; python scripts/check_blog.py; E01-blog1/2/3.png |
| E02 | `/student`, JSON 5 sinh viên đủ trường | DAT | evidence/local/E02-student-api.json; feat/student-json-api; python scripts/check_students.py |
| E03 | `studentdb.students`, schema đúng, ít nhất 3 dòng | DAT | evidence/local/E03-student-database.json; feat/student-sql-database; python scripts/check_student_database.py |
| E04 | Realm MSSV, 2 user, public client, token gọi `/secure` | DAT | evidence/local/E04-keycloak.json; feat/student-identity; python scripts/check_identity.py |
| E05 | Avatar public URL, documents chứa PDF báo cáo | DAT | evidence/local/E05-storage.json; feat/profile-object-storage; python scripts/check_profile_storage.py; E05-minio-avatar.png |
| E06 | Bản ghi DNS App/MinIO/Keycloak, dig đúng | DAT | evidence/local/E06-dns.json; feat/service-dns-records; python scripts/check_service_dns.py |
| E07 | Prometheus giám sát Web, target UP và metrics thật | DAT | evidence/local/E07-web-metrics.json; feat/web-metrics; python scripts/check_web_metrics.py; E07-web-targets.png; E07-web-metrics.png |
| E08 | System Health of MSSV, 3 biểu đồ có dữ liệu | DAT | evidence/local/E08-system-health.json; feat/personal-health-dashboard; python scripts/check_health_dashboard.py; E08-system-health.png |
| E09 | Proxy `/student/` trả JSON backend | DAT | evidence/local/E09-student-proxy.json; feat/student-proxy-route; python scripts/check_student_proxy.py |
| E10 | 2 Web replica (thuộc cụm 3 Web container), log Round Robin luân phiên | DAT | evidence/local/E10-round-robin.json; feat/round-robin-balancing; python scripts/check_round_robin.py |

## 8. Các điểm cần đối chiếu khi triển khai

Đây là lưu ý từ mẫu PDF, **chưa phải lỗi đã quan sát trên hệ thống của bạn**:

- Số container: 9 loại server nhưng mẫu có thêm Node Exporter; hệ thống thực tế hoàn chỉnh có 17 container (gồm 3 container Web riêng biệt: Web chính `web-frontend-server` và hai replica `web-frontend-server1`, `web-frontend-server2`; Nginx exporter; E-learning Flutter Web; Firebase emulator; Loki; Alloy).
- Tên service và cổng ở các phần của mẫu không thống nhất; chọn tên dài nhất quán, App host 8085, Auth host 8081.
- Keycloak `/auth/`, hostname và issuer cần cấu hình thống nhất local/EC2.
- Grafana dùng datasource đúng tên service Prometheus; logging tập trung đã được tích hợp qua Loki + Alloy với datasource Loki riêng.
- DNS dùng Bind9 nội bộ (`internal-dns-server`); IP ví dụ 10.10.10.x là bản ghi lab, không tự trở thành IP thật của container.
- Mẫu thiếu restart/volume ở một số service; bổ sung để khớp yêu cầu chung: các service/container được cấu hình restart policy `unless-stopped`; 8 named volume lưu trữ dữ liệu bền vững qua các lần recreate.
- Mở rộng Prometheus Web cần endpoint metrics thật; Nginx prometheus exporter đã được tích hợp trên cổng 9113 và scrape qua job `web`.

## 9. Nhật ký cập nhật

| Ngày | Nội dung | Branch / commit |
|---|---|---|
| 02/11/2026 | Rà soát bàn giao Codex – Gemini ([BAN_GIAO_GEMINI.md](BAN_GIAO_GEMINI.md)); Docker engine chưa kết nối ở lần rà soát ban đầu, Codex review ghi nhận Docker 29.0.1 và 17 container Up (chưa chạy lại full suite mới); hoàn thành G01 đồng bộ trạng thái và kế hoạch | `docs/reconcile-local-status` / `docs: reconcile current local status` |
| 29/10/2026 | Chạy kiểm thử release và lưu bằng chứng 27 bước đạt bằng `check_all.py --screenshots`; ghim digest 17 runtime images và 6 custom images | `test/final-local-verification` / `fefd263`; evidence/local/local-suite.json, release-images.json |
| 29/10/2026 | Tích hợp centralized logging với Loki và Alloy; tạo Grafana dashboard Service Logs; kiểm thử persistence sau recreate Loki | `feat/centralized-service-logs` / `a249748`; evidence/local/service-logging.json |
| 29/10/2026 | Tích hợp Flutter Web E-learning demo tại `/elearning/`, kết nối Firebase Emulator riêng; kiểm thử hai vai trò và persistence | `feat/elearning-web-demo` / `ec74016`; evidence/local/elearning-demo.json, elearning-persistence.json |
| 29/10/2026 | Xử lý FIX-005: dùng upstream resolver và zone trong gateway, kiểm thử E10 với recreate replica đạt | `feat/round-robin-balancing` / `1f27f82`; evidence/local/E10-round-robin.json |
| 28/10/2026 | Chạy lại 22 bước core + E01–E10: tất cả đạt trên 13 container local; chưa kiểm chứng AWS | `test/local-output-audit` / `test: refresh local output verification`; evidence/local/local-audit-20261028.json |
| 27/10/2026 | Kế hoạch hoàn tất local/10 mở rộng trước AWS; đối chiếu branch Coffee Shop/E-learning; build Flutter Web main đạt, chưa chạy Firebase/data | `docs/local-completion-plan` / `docs: plan complete local delivery`; evidence/local/source-audit-elearning.json |
| 26/10/2026 | Generated local PDF/DOCX report, screenshots and 75.68-second video; AWS deferred | `docs/submission-evidence` / `503a61a`, `f3e3c15` |
| 26/10/2026 | Published katie217/myminicloud-web:1.0.0 and verified registry manifest | `chore/image-publication` / `431197d` |
| 26/10/2026 | Local mandatory features and integration checks passed; 10 healthy containers; named-volume recreation passed | Group branches integrated into main |
| 26/10/2026 | Xác minh Docker Linux engine đã chạy; đóng FIX-001; các output hệ thống vẫn chưa thực hiện | `chore/project-foundation` / `docs: cập nhật trạng thái` |
| 26/10/2026 | Bổ sung quy tắc loại trừ file local/bí mật và line ending; không tính là output hệ thống đã chạy | `chore/project-foundation` / `chore: cấu hình nền git` |
| 26/10/2026 | Tạo bảng theo dõi, kế hoạch và quy ước; khởi tạo Git local để lưu commit ngay | `chore/project-foundation` / `docs: ghi nhận kế hoạch` |

## 10. Hạn chế còn lại và thứ tự tiếp tục

1. **AWS EC2 chưa thực hiện** theo yêu cầu người dùng: chưa có public IP, SSH và bằng chứng cloud. Chỉ sau khi người dùng kiểm tra và xác nhận bản local cuối đạt mới triển khai trên branch `chore/cloud-deployment`, kiểm thử đủ server rồi cập nhật R14.
2. **R16/R17/R18 giữ trạng thái CHO_KIEM_THU**: Báo cáo cuối (G02) và video local cuối (G03) đang được cập nhật để phản ánh đầy đủ 17 container và các chức năng mới; hồ sơ cloud sẽ bổ sung sau khi triển khai EC2.
3. **MSSV Diệp Yến Nhi còn thiếu**: Cập nhật `project-info.json`, trang Home, báo cáo và video khi được cung cấp; avatar chữ K đã được người dùng phê duyệt ngày 29/10/2026 và không chặn các task kỹ thuật.
4. **Metrics có giới hạn**: CPU/RAM Linux VM của Docker Desktop, network theo namespace exporter; chưa có cAdvisor cho từng container hoặc toàn bộ Windows. CPU/RAM/Network bắt buộc đã có dữ liệu.
5. **Logging tập trung đã làm:** Alloy chỉ thu Docker logs thuộc project myminicloud, Loki giữ log trong volume theo retention 24 giờ, Grafana dashboard MyMiniCloud Service Logs hiển thị log thật. Marker request đã được tìm thấy qua Loki/Grafana và còn sau recreate Loki; `evidence/local/service-logging.json`, `logging-grafana.png`.
6. **Mở rộng 10/10 đã hoàn thành trên local**: Cả 10 mục E01–E10 đều đã triển khai trên các branch riêng, kiểm thử và có minh chứng JSON/PNG tại `evidence/local/` (baseline `fefd263`).
7. **E-learning demo đã tích hợp:** `/elearning/`, Flutter Web demo, Firebase Emulator trong Docker với dữ liệu giả; login hai vai trò, xem/tạo khóa học, số sinh viên ghi danh, refresh và recreate đạt. Google Sign-In, Cloud Functions/link preview và các luồng khác của đồ án gốc chưa kiểm chứng. SQL/Keycloak/MinIO theo đề vẫn giữ riêng.

Các artifact dùng ngay: [README](README.md), [báo cáo PDF local](report/BaoCao_Local_521H0092.pdf), [DOCX](report/BaoCao_Local_521H0092.docx), [video local](report/Demo_Local_521H0092.webm), [trang xem video](report/Demo_Local_521H0092.html), [ảnh/log](evidence/local/).

## 11. Branch đã thực hiện

| Nhóm chức năng | Branch | Kết quả |
|---|---|---|
| Nền tảng | `chore/project-foundation` | Repo/config/setup và quy ước; đã tích hợp main |
| Web/App/DB | `feat/web-api-database` | HTTP/JSON/SQL và App–DB đạt; đã tích hợp main |
| Identity/Storage/DNS | `feat/identity-storage-dns` | Auth UI, S3 và dig đạt; đã tích hợp main |
| Monitoring/Grafana | `feat/monitoring-dashboard` | Metrics/query/charts đạt; đã tích hợp main |
| Gateway/Network/Volume | `feat/gateway-network-tests` | Routing/ping/recreate và bộ test tổng hợp đạt; đã tích hợp main |
| Docker Hub | `chore/image-publication` | Web image 1.0.0 push/manifest đạt; đã tích hợp main |
| Hồ sơ local ban đầu | `docs/submission-evidence` | Báo cáo/ảnh/video local ban đầu; phần cloud chờ EC2 |
| E01 blog cá nhân | `feat/personal-blog` | 3 bài blog có ảnh và link điều hướng; commit `c377c25` |
| E02 JSON student API | `feat/student-json-api` | Endpoint `/student` trả 5 sinh viên; commit `9b4d11d` |
| E03 student SQL database | `feat/student-sql-database` | Schema `studentdb.students` và 3 dòng seed; commit `64e5f99` |
| E09 student gateway route | `feat/student-proxy-route` | Proxy gateway route `/student/`; commit `6b69d0c` |
| E04 Keycloak realm/token | `feat/student-identity` | Realm `realm_521H0092`, client, users, token; commit `0816e1b` |
| E04 Secure demo portal | `feat/secure-api-demo` | Portal đăng nhập OIDC, gọi `/secure`; commit `e276d1f` |
| E05 avatar cá nhân / PDF | `feat/profile-object-storage` | Avatar chữ K công khai, bucket documents; commit `d119e03` |
| E06 DNS mở rộng | `feat/service-dns-records` | Bản ghi DNS app, minio, keycloak; commit `8f1b6be` |
| E07 Web metrics | `feat/web-metrics` | Nginx prometheus exporter, job web scrape; commit `ac394ac` |
| E08 dashboard cá nhân | `feat/personal-health-dashboard` | Dashboard System Health of 521H0092; commit `45f3a25` |
| E10 round robin | `feat/round-robin-balancing` | 2 Web replica (cụm 3 Web container), cân bằng tải round robin, xử lý FIX-005; commit `1f27f82` |
| Portal demo tích hợp | `feat/demo-portal` | Trang cổng demo tích hợp các dịch vụ; commit `0f1d42d` |
| E-learning demo | `feat/elearning-web-demo` | Flutter Web demo + Firebase emulator; commit `ec74016` |
| Centralized logging | `feat/centralized-service-logs` | Loki + Alloy + Grafana logs dashboard; commit `a249748` |
| Release images ghim digest | `chore/local-release-images` | 17 runtime images, 6 custom images; commit `de99b36` |
| Baseline kiểm thử local | `test/final-local-verification` | Chạy bộ 27 bước bằng `check_all.py --screenshots` đạt; các bài test persistence/E-learning bổ sung riêng; commit `fefd263` |
| Bàn giao điều phối Codex | `docs/gemini-work-handoff` | Lập kế hoạch điều phối bàn giao; commit `fd0b4e6` |

## 12. Kế hoạch công việc còn lại (G01–G04 và QA) theo phân công 02/11/2026

Theo [BAN_GIAO_GEMINI.md](BAN_GIAO_GEMINI.md), Gemini thực hiện tuần tự từng task trên branch riêng, Codex review và kiểm thử độc lập trước khi tích hợp vào main. Thứ tự thực hiện:

| Task / Nhóm | Branch thực thi | Trạng thái | Điều kiện nghiệm thu / Nội dung bàn giao |
|---|---|---|---|
| G01 Đồng bộ trạng thái | `docs/reconcile-local-status` | DANG_LAM | Đồng bộ TIEN_DO_OUTPUT.md và KE_HOACH_HOAN_THIEN_LOCAL.md; đếm DAT 14 R / 10 E; R14 chờ, R16–R18 CHO_KIEM_THU; mô tả đúng cụm 3 container Web (Web chính + 2 replica) và 8 named volume; dẫn chứng FIX-005 |
| G02 Báo cáo cuối release | `docs/refresh-local-report` | CHUA_LAM | Cập nhật BaoCao_Local_521H0092.md/.pdf/.docx/HTML đủ 5 chương, 17 container/9 vai trò/8 volume, nhúng ảnh thật đọc được từng server; verify hash PDF MinIO |
| G03 Video local release | `docs/refresh-local-video` | CHUA_LAM | Sửa scripts/record_demo.py quay video WebM 17 container, cảnh E-learning, logging, form secure (không lộ secret); demo-chapters.json đúng cảnh thực tế |
| G04 Tổng hợp đầu ra | `docs/local-output-handoff` | CHUA_LAM | Tạo TONG_HOP_OUTPUT_LOCAL.md; cập nhật README.md, HUONG_DAN_TEST_LOCAL.md, đồng bộ tracker bản cuối |
| QA cuối độc lập | `test/final-local-handoff` | CHUA_LAM | Codex chạy độc lập suite 27 bước (`python scripts/check_all.py --screenshots`), persistence test, luồng E-learning, hash PDF, Docker Hub digest |
| Duyệt local trước AWS | Phụ thuộc người dùng | CHO_THONG_TIN | Người dùng kiểm tra giao diện và xác nhận bản local đạt trước khi tạo tài nguyên cloud |
| L10 Triển khai AWS EC2 | `chore/cloud-deployment` | CHUA_LAM | Chỉ bắt đầu sau khi người dùng duyệt local; thuê EC2 Ubuntu, chạy stack, test public IP, bổ sung hồ sơ cloud R14/R16–R18 |
