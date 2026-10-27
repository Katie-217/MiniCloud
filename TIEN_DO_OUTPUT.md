# Bảng theo dõi output MyMiniCloud

Cập nhật lần đầu: **26/10/2026**, cập nhật kế hoạch **27/10/2026**. Nguồn yêu cầu: `Báo Cáo Cuối Kỳ.docx.pdf`. Tiêu chí theo trang: `KE_HOACH_MINICLOUD_2_NGAY.md`; thứ tự triển khai hiện hành: [KE_HOACH_HOAN_THIEN_LOCAL.md](KE_HOACH_HOAN_THIEN_LOCAL.md). Kế hoạch bắt buộc cũ lưu giai đoạn nền tảng đã thực hiện.

## 1. Tổng quan hiện tại

- **Output bắt buộc đạt: 14/18** nhóm trong bảng dưới. Đây là cách chia nhóm để quản lý, không phải cách chia điểm của PDF.
- **Mở rộng đạt: 4/10** mục.
- Các service local được triển khai và kiểm thử dần theo bảng mục 3; chỉ các dòng `DAT` được tính hoàn thành.
- Git local có `main` và các branch theo nhóm, kết nối repo Katie-217/MiniCloud; lịch sử tài liệu ban đầu được giữ nguyên.
- Đã thêm `.gitignore` loại trừ bí mật, dữ liệu runtime và file trích PDF; `.gitattributes` thống nhất line ending cho file container Linux.
- Đã kết nối `https://github.com/Katie-217/MiniCloud`, giữ README và lịch sử remote; đã push branch nền tảng. Nhóm: Võ Thị Thiên Kim — 521H0092; Diệp Yến Nhi — chờ MSSV. Docker Hub namespace: `katie217`.
- Quy ước mới: commit message tiếng Anh, tiền tố phù hợp và thông điệp chính khoảng 4–5 từ. AWS để sau theo yêu cầu người dùng; tiếp tục toàn bộ công việc local không phụ thuộc AWS.
- Docker CLI/Compose đã cài; `docker info` kết nối được Linux engine, server **29.0.1**. Các container MyMiniCloud được quản lý riêng, không dừng container project khác.
- **Kết quả local:** toàn bộ chức năng cơ bản đã kiểm thử đạt; 10 container healthy; bộ kiểm thử tổng hợp thành công, bao gồm UI. Docker Hub Web image 1.0.0 đã push và xác minh manifest.
- **Hồ sơ local:** báo cáo PDF 18 trang và DOCX/Markdown đủ 5 chương; video WebM 75,68 giây gồm 14 phần, có chú thích; ảnh/log đầy đủ trong `evidence/local/`.
- **Chưa hoàn tất toàn đề:** EC2/public IP và bằng chứng cloud; bổ sung MSSV Diệp Yến Nhi; cập nhật báo cáo/video bản cuối. Mở rộng hiện chưa làm.
- **Thứ tự mới 27/10:** hoàn tất local và 10 mở rộng, Docker Hub/hồ sơ → người dùng kiểm tra bản cuối → mới thuê và triển khai EC2. Chưa thao tác AWS.
- **Repo E-learning đã khảo sát:** main `9e9ebd5` build Flutter Web thành công; Firebase Auth/Firestore/Storage chưa chạy kiểm thử dữ liệu. Chưa nhập source hoặc thay Web MiniCloud. Branch management_system ahead main 12 commit, chưa build branch đó.
  Minh chứng khảo sát: [source-audit-elearning.json](evidence/local/source-audit-elearning.json); đây là test build repo nguồn, không phải output E01–E10 đã đạt.

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
| R01 | Compose khởi động toàn hệ thống; `cloud-net`, container name, cổng, restart đúng — tr. 1–3 | `chore/project-foundation` + các nhóm tích hợp | DAT | evidence/local/R01-stack.json; 10 healthy containers / 9 server roles; commit `1f9f77b` |
| R02 | Home và `/blog/` HTTP 200, nội dung đúng — tr. 12–13 | `feat/web-api-database` | DAT | evidence/local/R02-web.json; Home + Blog; commit `a28234e` |
| R03 | `/hello` trực tiếp và qua proxy trả JSON đúng — tr. 13 | `feat/web-api-database` + `feat/gateway-network-tests` | DAT | evidence/local/R03-api.json; direct + proxy; commit `35f3502` |
| R04 | `minicloud.notes` có bảng và dữ liệu khởi tạo — tr. 6, 14 | `feat/web-api-database` | DAT | evidence/local/R04-database.json; commit `ea51eb3` |
| R05 | Keycloak admin đăng nhập được, tạo user sv01 — tr. 14–15 | `feat/identity-storage-dns` | DAT | evidence/local/R05-auth.json; R05-keycloak-admin.png; R05-keycloak-user.png; commit `22e8a99` |
| R06 | MinIO bucket demo, upload và tải file được — tr. 2, 15–16 | `feat/identity-storage-dns` | DAT | evidence/local/R06-storage.json; R06-minio-bucket.png; R06-minio-object.png; commit `2114441` |
| R07 | DNS Web trả `10.10.10.10` bằng dig — tr. 16–17 | `feat/identity-storage-dns` | DAT | evidence/local/R07-dns.json; dig internal 53 + published host 1053; commit `41e7815` |
| R08 | Prometheus node target UP, query metric có dữ liệu — tr. 17–18 | `feat/monitoring-dashboard` | DAT | evidence/local/R08-monitoring.json; commit `435dc43` |
| R09 | Grafana datasource hoạt động, CPU/RAM/Network có dữ liệu — tr. 18–19 | `feat/monitoring-dashboard` | DAT | evidence/local/R09-grafana.json; R09-grafana-dashboard.png; R09-grafana-network.png; commit `25d4a51` |
| R10 | Proxy `/`, `/api/`, `/auth/` hoạt động, đúng status/redirect — tr. 19–20 | `feat/gateway-network-tests` | DAT | evidence/local/R10-gateway.json; Web/App/Auth + correct public OIDC issuer; commit `35f3502` |
| R11 | Các server thông mạng, có log ping và network membership — tr. 20 | `feat/gateway-network-tests` | DAT | evidence/local/R11-network.json; ping 3 packets for each of 10 services, 0% loss; commit `1f9f77b` |
| R12 | Volume cần thiết lưu được dữ liệu, restart policy đầy đủ — tr. 3 | Các nhóm service + `feat/gateway-network-tests` | DAT | evidence/local/R12-persistence.json; custom data preserved across all 5 stateful service recreations; commit `5967fba` |
| R13 | Ít nhất 1 image tùy chỉnh trên Docker Hub, có link/tag — tr. 3 | `chore/image-publication` | DAT | evidence/local/R13-dockerhub.json; katie217/myminicloud-web:1.0.0; manifest verified from registry; commit `431197d` |
| R14 | Toàn hệ thống chạy trên EC2 Ubuntu, public IP và test server đạt — tr. 1, 3 | `chore/cloud-deployment` | CHO_THONG_TIN | AWS deferred by user; no EC2 resources created/accessed |
| R15 | Dockerfile/Compose/config và source đủ để tái tạo — tr. 3 | Toàn bộ branch triển khai | DAT | evidence/local/R15-source.json; full source/config, setup idempotent, README with tested commands |
| R16 | Báo cáo đủ 5 chương + phụ lục, thống kê mở rộng — tr. 3, 27 | `docs/submission-evidence` | CHO_KIEM_THU | report/BaoCao_Local_521H0092.md/.pdf/.docx: đủ 5 chương cho local; chờ EC2 và MSSV thành viên hai; commit `503a61a` |
| R17 | Video demo và link truy cập được trong phụ lục — tr. 3 | `docs/submission-evidence` | CHO_KIEM_THU | report/Demo_Local_521H0092.webm: silent captioned local walkthrough; EC2 segment pending; commit `f3e3c15` |
| R18 | Ảnh từng server, log test; phân biệt local và EC2 — tr. 3 | Từng branch + `docs/submission-evidence` | CHO_KIEM_THU | evidence/local: đủ ảnh/log từng server, network, persistence, Docker Hub; EC2 chưa thực hiện; commit `0d2c665` |

## 4. Những output đã đạt

Các dòng `DAT` ở bảng mục 3 và 7 là output đã kiểm thử đạt, kèm đường dẫn log/ảnh. Các dòng `CHO_KIEM_THU` mới đạt một phần hoặc còn thiếu test tích hợp.

Công việc chuẩn bị đã hoàn thành: đọc PDF, trích yêu cầu/tiêu chí, lập kế hoạch hai ngày và quy trình branch/commit, tạo bảng này. Các công việc đó không được tính thay cho output hệ thống theo đề.

Khi có kết quả, mỗi mục ghi: ID output, môi trường local/EC2, branch/commit, lệnh hoặc thao tác kiểm thử, kết quả thực tế và file minh chứng.

## 5. Vấn đề cần fix và tình trạng xử lý

| ID | Vấn đề | Ảnh hưởng | Hướng xử lý | Trạng thái |
|---|---|---|---|---|
| FIX-001 | Ban đầu Docker CLI không kết nối được `dockerDesktopLinuxEngine` | Đã hết chặn build/chạy container | Kiểm tra lại bằng `docker info --format '{{.ServerVersion}}'`, nhận `29.0.1` | DAT |
| FIX-002 | Chưa có remote GitHub ở lần kiểm tra đầu | Đã hết chặn push branch | Đã fetch, giữ lịch sử và push `chore/project-foundation` lên MiniCloud | DAT |
| FIX-003 | Image/download MinIO được hướng dẫn không còn truy cập được tại lần kiểm tra | Không dựng được storage bằng cách copy image mẫu | Build source chính thức có tag/checksum, giữ license; UI và upload/download đã kiểm thử | DAT |
| FIX-004 | Docker Desktop từ chối root bind mount rslave | Node Exporter không start với cấu hình host mount ban đầu | Dùng root bind read-only mặc định, giữ proc/sys mounts; metric và dashboard có dữ liệu | DAT |

Hiện không còn lỗi chức năng làm trượt các bài kiểm thử MiniCloud local đã chạy. Các hạn chế ngoài bộ kiểm thử được ghi ở mục 10; phần AWS và môi trường dữ liệu E-learning chưa được kiểm chứng. Không tính cảnh báo Wasm dry-run của repo E-learning là lỗi bản Web JavaScript đã build thành công.

## 6. Thông tin và setup còn thiếu

| Việc cần làm rõ | Trạng thái | Hành động tiếp theo |
|---|---|---|
| URL repo và quyền làm việc | DAT | Katie-217/MiniCloud; quyền ADMIN; đã push branch |
| MSSV, tên sinh viên/nhóm | DANG_LAM | Có Võ Thị Thiên Kim / 521H0092 và Diệp Yến Nhi; chờ MSSV thành viên thứ hai |
| Username Docker Hub và login local | DAT | Namespace katie217; push Web 1.0.0 và đọc lại manifest thành công |
| Có EC2 Ubuntu hay chưa | CHO_THONG_TIN | Người dùng yêu cầu để sau; chưa thao tác AWS |
| Public IP, user SSH, đường dẫn key nếu đã có EC2 | CHO_THONG_TIN | Kết nối bằng key local, không đưa nội dung key vào Git/chat |
| Repo ứng dụng demo | DANG_LAM | Đã nhận E-learning; main build Web đạt; cần môi trường Firebase demo riêng và kiểm thử UI, không dùng database thật |
| Avatar cá nhân cho E05 | CHO_THONG_TIN | Cần ảnh được người dùng chọn/cung cấp; chưa coi ảnh minh họa bất kỳ là avatar cá nhân đã hoàn tất |

## 7. Mở rộng chưa làm

| ID | Output mở rộng | Trạng thái | Minh chứng / commit |
|---|---|---|---|
| E01 | Blog 3 bài, mỗi bài có ảnh và link quay lại | DAT | evidence/local/E01-blog.json; feat/personal-blog; python scripts/check_blog.py; E01-blog1/2/3.png |
| E02 | `/student`, JSON 5 sinh viên đủ trường | DAT | evidence/local/E02-student-api.json; feat/student-json-api; python scripts/check_students.py |
| E03 | `studentdb.students`, schema đúng, ít nhất 3 dòng | DAT | evidence/local/E03-student-database.json; feat/student-sql-database; python scripts/check_student_database.py |
| E04 | Realm MSSV, 2 user, public client, token gọi `/secure` | CHUA_LAM | — |
| E05 | Avatar public URL, documents chứa PDF báo cáo | CHUA_LAM | — |
| E06 | Bản ghi DNS App/MinIO/Keycloak, dig đúng | CHUA_LAM | — |
| E07 | Prometheus giám sát Web, target UP và metrics thật | CHUA_LAM | — |
| E08 | System Health of MSSV, 3 biểu đồ có dữ liệu | CHUA_LAM | — |
| E09 | Proxy `/student/` trả JSON backend | DAT | evidence/local/E09-student-proxy.json; feat/student-proxy-route; python scripts/check_student_proxy.py |
| E10 | 2 Web server, log Round Robin luân phiên | CHUA_LAM | — |

## 8. Các điểm cần đối chiếu khi triển khai

Đây là lưu ý từ mẫu PDF, **chưa phải lỗi đã quan sát trên hệ thống của bạn**:

- Số container: 9 loại server nhưng mẫu có thêm Node Exporter; ghi đúng kiến trúc thực tế.
- Tên service và cổng ở các phần của mẫu không thống nhất; chọn tên dài nhất quán, App host 8085, Auth host 8081.
- Keycloak `/auth/`, hostname và issuer cần cấu hình thống nhất local/EC2.
- Grafana dùng datasource đúng tên service Prometheus; không mặc nhiên có logging tập trung khi mới có metrics.
- DNS IP ví dụ không tự trở thành IP thật của container.
- Mẫu thiếu restart/volume ở một số service; bổ sung để khớp yêu cầu chung.
- Mở rộng Prometheus Web cần endpoint metrics thật; chỉ thêm target Web tĩnh chưa đủ.

## 9. Nhật ký cập nhật

| Ngày | Nội dung | Branch / commit |
|---|---|---|
| 26/10/2026 | Tạo bảng theo dõi, kế hoạch và quy ước; khởi tạo Git local để lưu commit ngay | `chore/project-foundation` / `docs: ghi nhận kế hoạch` |
| 26/10/2026 | Bổ sung quy tắc loại trừ file local/bí mật và line ending; không tính là output hệ thống đã chạy | `chore/project-foundation` / `chore: cấu hình nền git` |
| 26/10/2026 | Xác minh Docker Linux engine đã chạy; đóng FIX-001; các output hệ thống vẫn chưa thực hiện | `chore/project-foundation` / `docs: cập nhật trạng thái` |
| 26/10/2026 | Local mandatory features and integration checks passed; 10 healthy containers; named-volume recreation passed | Group branches integrated into main |
| 26/10/2026 | Published katie217/myminicloud-web:1.0.0 and verified registry manifest | `chore/image-publication` / `431197d` |
| 26/10/2026 | Generated local PDF/DOCX report, screenshots and 75.68-second video; AWS deferred | `docs/submission-evidence` / `503a61a`, `f3e3c15` |
| 27/10/2026 | Kế hoạch hoàn tất local/10 mở rộng trước AWS; đối chiếu branch Coffee Shop/E-learning; build Flutter Web main đạt, chưa chạy Firebase/data | `docs/local-completion-plan` / `docs: plan complete local delivery`; evidence/local/source-audit-elearning.json |

## 10. Hạn chế còn lại và thứ tự tiếp tục

1. **AWS EC2 chưa thực hiện** theo yêu cầu người dùng: chưa có public IP, SSH và bằng chứng cloud. Chỉ sau khi người dùng kiểm tra và xác nhận bản local cuối đạt mới triển khai trên branch `chore/cloud-deployment`, kiểm thử đủ server rồi cập nhật R14.
2. **R16/R17/R18 mới hoàn tất bản local**: báo cáo, video và ảnh/log cloud phải bổ sung sau EC2. Video local có chú thích, không có giọng đọc; file `report/Demo_Local_521H0092.webm`, 75,68 giây, 1440×1000, đã kiểm tra playback.
3. **MSSV Diệp Yến Nhi còn thiếu**: cập nhật `project-info.json`, trang Home, báo cáo và video khi được cung cấp; rebuild Web nếu đổi nội dung.
4. **Metrics có giới hạn**: CPU/RAM Linux VM của Docker Desktop, network theo namespace exporter; chưa có cAdvisor/mọi container hoặc toàn bộ Windows. Một số panel Root FS/hệ thống tùy chọn của template có thể N/A; CPU/RAM/Network bắt buộc đã có dữ liệu.
5. **Logging tập trung chưa làm**: theo bài demo chi tiết dùng Grafana + Prometheus, log container được lưu riêng đã loại mật khẩu; chưa có Loki.
6. **Mở rộng 0/10**: được làm trước EC2 theo thứ tự mới; kế hoạch đã có task/output/test cho cả 10 mục. `/secure` đã có test từ chối token thiếu/sai, chưa có realm MSSV/client/token hợp lệ của E04.
7. **E-learning chưa tích hợp:** main đã build Web, nhưng đăng nhập/dữ liệu Firebase, môi trường emulator, base path và proxy chưa kiểm thử. Không dùng kết quả build để tuyên bố đủ các luồng ứng dụng; không thay SQL/Keycloak/MinIO theo đề bằng Firebase.

Các artifact dùng ngay: [README](README.md), [báo cáo PDF local](report/BaoCao_Local_521H0092.pdf), [DOCX](report/BaoCao_Local_521H0092.docx), [video local](report/Demo_Local_521H0092.webm), [trang xem video](report/Demo_Local_521H0092.html), [ảnh/log](evidence/local/).

## 11. Branch đã thực hiện

| Nhóm | Branch | Kết quả |
|---|---|---|
| Nền tảng | `chore/project-foundation` | Repo/config/setup và quy ước; đã tích hợp main |
| Web/App/DB | `feat/web-api-database` | HTTP/JSON/SQL và App–DB đạt; đã tích hợp main |
| Identity/Storage/DNS | `feat/identity-storage-dns` | Auth UI, S3 và dig đạt; đã tích hợp main |
| Monitoring/Grafana | `feat/monitoring-dashboard` | Metrics/query/charts đạt; đã tích hợp main |
| Gateway/Network/Volume | `feat/gateway-network-tests` | Routing/ping/recreate và bộ test tổng hợp đạt; đã tích hợp main |
| Docker Hub | `chore/image-publication` | Web image 1.0.0 push/manifest đạt; đã tích hợp main |
| Hồ sơ local | `docs/submission-evidence` | Báo cáo/ảnh/video local và hướng dẫn; phần cloud vẫn chờ |
| AWS | `chore/cloud-deployment` | Chưa tạo, chờ người dùng kiểm tra AWS |
| Kế hoạch local cuối | `docs/local-completion-plan` | Lập task/output/test cho E01–E10 và tích hợp demo; chưa tính thêm output triển khai đạt |

## 12. Công việc tiếp theo theo kế hoạch ngày 27/10/2026

Chỉ dẫn mới nhất: mỗi chức năng một branch riêng. Bảng dưới là nhóm tiến độ; tên branch thực thi chính xác nằm trong bảng chức năng ở `KE_HOACH_HOAN_THIEN_LOCAL.md`. E01–E10 không dùng chung branch.

| Nhóm | Branch dự kiến | Trạng thái | Điều kiện hoàn thành |
|---|---|---|---|
| Student JSON / SQL / route | feat/student-api-database | CHUA_LAM | E02/E03/E09 kiểm thử và có minh chứng |
| Blog / giao diện demo | feat/demo-web-content | CHUA_LAM | E01 và UI đọc API qua gateway |
| Realm / token hợp lệ | feat/identity-extensions | CHUA_LAM | E04 đủ test chấp nhận/từ chối token |
| Avatar / tài liệu / DNS | feat/storage-dns-extensions | CHUA_LAM | E05/E06; PDF cuối upload lại sau cập nhật báo cáo |
| Web metrics / dashboard | feat/observability-extensions | CHUA_LAM | E07/E08 với dữ liệu thật |
| Round robin | feat/round-robin-balancing | CHUA_LAM | E10, giữ các route/metrics cũ đạt |
| E-learning demo | feat/elearning-web-demo | CHUA_LAM | Build source đã khảo sát; bước tích hợp cần UI/data runtime và môi trường riêng |
| Kiểm thử / image release | test/local-release-readiness; chore/local-release-images | CHUA_LAM | Regression, persistence, dựng lại, Hub tag/digest cuối |
| Hồ sơ local cuối | docs/final-local-delivery | CHUA_LAM | Báo cáo/video/ảnh/log/tracker phản ánh bản release |
| Duyệt local trước AWS | Phụ thuộc người dùng | CHO_THONG_TIN | Chỉ yêu cầu duyệt sau khi có bộ bàn giao local cụ thể |

Chi tiết cách làm, test và ước lượng nằm trong [kế hoạch hoàn thiện local](KE_HOACH_HOAN_THIEN_LOCAL.md). Chưa thay đổi số lượng DAT khi mới hoàn tất khảo sát và kế hoạch.
