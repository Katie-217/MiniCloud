# Bảng theo dõi output MyMiniCloud

Cập nhật lần đầu: **26/10/2026** theo ngày phiên làm việc. Nguồn yêu cầu: `Báo Cáo Cuối Kỳ.docx.pdf`. Cách làm chi tiết: `KE_HOACH_MINICLOUD_2_NGAY.md`; thứ tự branch và triển khai: `KE_HOACH_TRIEN_KHAI_BAT_BUOC.md`.

## 1. Tổng quan hiện tại

- **Output bắt buộc đạt: 1/18** nhóm trong bảng dưới. Đây là cách chia nhóm để quản lý, không phải cách chia điểm của PDF.
- **Mở rộng đạt: 0/10** mục.
- Đã đọc đề và chuẩn bị kế hoạch, quy ước Git, bảng theo dõi. Chưa có mã nguồn hệ thống hoặc kết quả chạy service.
- Đã khởi tạo Git local, branch `chore/project-foundation`; chưa có remote. Commit tài liệu: `567b95e` — `docs: ghi nhận kế hoạch`; `main` trỏ vào mốc khởi tạo này.
- Đã thêm `.gitignore` loại trừ bí mật, dữ liệu runtime và file trích PDF; `.gitattributes` thống nhất line ending cho file container Linux.
- Đã kết nối `https://github.com/Katie-217/MiniCloud`, giữ README và lịch sử remote; đã push branch nền tảng. Nhóm: Võ Thị Thiên Kim — 521H0092; Diệp Yến Nhi — chờ MSSV. Docker Hub namespace: `katie217`.
- Quy ước mới: commit message tiếng Anh, tiền tố phù hợp và thông điệp chính khoảng 4–5 từ. AWS để sau theo yêu cầu người dùng; tiếp tục toàn bộ công việc local không phụ thuộc AWS.
- Docker CLI/Compose đã cài; lần kiểm tra cuối `docker info` đã kết nối được Linux engine, server **29.0.1**. Chưa build/chạy service MyMiniCloud.

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
| R01 | Compose khởi động toàn hệ thống; `cloud-net`, container name, cổng, restart đúng — tr. 1–3 | `chore/project-foundation` + các nhóm tích hợp | CHO_KIEM_THU | Compose nền hợp lệ; chưa đủ service |
| R02 | Home và `/blog/` HTTP 200, nội dung đúng — tr. 12–13 | `feat/web-api-database` | DAT | evidence/local/R02-web.json; Home + Blog |
| R03 | `/hello` trực tiếp và qua proxy trả JSON đúng — tr. 13 | `feat/web-api-database` + `feat/gateway-network-tests` | CHO_KIEM_THU | evidence/local/R03-api.json; direct đạt, chờ proxy |
| R04 | `minicloud.notes` có bảng và dữ liệu khởi tạo — tr. 6, 14 | `feat/web-api-database` | CHUA_LAM | — |
| R05 | Keycloak admin đăng nhập được, tạo user sv01 — tr. 14–15 | `feat/identity-storage-dns` | CHUA_LAM | — |
| R06 | MinIO bucket demo, upload và tải file được — tr. 2, 15–16 | `feat/identity-storage-dns` | CHUA_LAM | — |
| R07 | DNS Web trả `10.10.10.10` bằng dig — tr. 16–17 | `feat/identity-storage-dns` | CHUA_LAM | — |
| R08 | Prometheus node target UP, query metric có dữ liệu — tr. 17–18 | `feat/monitoring-dashboard` | CHUA_LAM | — |
| R09 | Grafana datasource hoạt động, CPU/RAM/Network có dữ liệu — tr. 18–19 | `feat/monitoring-dashboard` | CHUA_LAM | — |
| R10 | Proxy `/`, `/api/`, `/auth/` hoạt động, đúng status/redirect — tr. 19–20 | `feat/gateway-network-tests` | CHUA_LAM | — |
| R11 | Các server thông mạng, có log ping và network membership — tr. 20 | `feat/gateway-network-tests` | CHUA_LAM | — |
| R12 | Volume cần thiết lưu được dữ liệu, restart policy đầy đủ — tr. 3 | Các nhóm service + `feat/gateway-network-tests` | CHUA_LAM | — |
| R13 | Ít nhất 1 image tùy chỉnh trên Docker Hub, có link/tag — tr. 3 | `chore/cloud-deployment` | CHUA_LAM | — |
| R14 | Toàn hệ thống chạy trên EC2 Ubuntu, public IP và test server đạt — tr. 1, 3 | `chore/cloud-deployment` | CHUA_LAM | — |
| R15 | Dockerfile/Compose/config và source đủ để tái tạo — tr. 3 | Toàn bộ branch triển khai | DANG_LAM | Đã có setup, env mẫu và quy ước cấu hình |
| R16 | Báo cáo đủ 5 chương + phụ lục, thống kê mở rộng — tr. 3, 27 | `docs/submission-evidence` | CHUA_LAM | — |
| R17 | Video demo và link truy cập được trong phụ lục — tr. 3 | `docs/submission-evidence` | CHUA_LAM | — |
| R18 | Ảnh từng server, log test; phân biệt local và EC2 — tr. 3 | Từng branch + `docs/submission-evidence` | CHUA_LAM | — |

## 4. Những output đã đạt

**Chưa có output chức năng nào được kiểm thử đạt.**

Công việc chuẩn bị đã hoàn thành: đọc PDF, trích yêu cầu/tiêu chí, lập kế hoạch hai ngày và quy trình branch/commit, tạo bảng này. Các công việc đó không được tính thay cho output hệ thống theo đề.

Khi có kết quả, mỗi mục ghi: ID output, môi trường local/EC2, branch/commit, lệnh hoặc thao tác kiểm thử, kết quả thực tế và file minh chứng.

## 5. Vấn đề cần fix và tình trạng xử lý

| ID | Vấn đề | Ảnh hưởng | Hướng xử lý | Trạng thái |
|---|---|---|---|---|
| FIX-001 | Ban đầu Docker CLI không kết nối được `dockerDesktopLinuxEngine` | Đã hết chặn build/chạy container | Kiểm tra lại bằng `docker info --format '{{.ServerVersion}}'`, nhận `29.0.1` | DAT |
| FIX-002 | Chưa có remote GitHub ở lần kiểm tra đầu | Đã hết chặn push branch | Đã fetch, giữ lịch sử và push `chore/project-foundation` lên MiniCloud | DAT |

Chưa có lỗi chức năng nào của MyMiniCloud được xác nhận vì chưa triển khai service.

## 6. Thông tin và setup còn thiếu

| Việc cần làm rõ | Trạng thái | Hành động tiếp theo |
|---|---|---|
| URL repo và quyền làm việc | DAT | Katie-217/MiniCloud; quyền ADMIN; đã push branch |
| MSSV, tên sinh viên/nhóm | DANG_LAM | Có Võ Thị Thiên Kim / 521H0092 và Diệp Yến Nhi; chờ MSSV thành viên thứ hai |
| Username Docker Hub và login local | DANG_LAM | Namespace katie217; sẽ xác minh bằng push image thực tế |
| Có EC2 Ubuntu hay chưa | CHO_THONG_TIN | Chốt phương án; nếu có, xác minh SSH và môi trường |
| Public IP, user SSH, đường dẫn key nếu đã có EC2 | CHO_THONG_TIN | Kết nối bằng key local, không đưa nội dung key vào Git/chat |

## 7. Mở rộng chưa làm

| ID | Output mở rộng | Trạng thái | Minh chứng / commit |
|---|---|---|---|
| E01 | Blog 3 bài, mỗi bài có ảnh và link quay lại | CHUA_LAM | — |
| E02 | `/student`, JSON 5 sinh viên đủ trường | CHUA_LAM | — |
| E03 | `studentdb.students`, schema đúng, ít nhất 3 dòng | CHUA_LAM | — |
| E04 | Realm MSSV, 2 user, public client, token gọi `/secure` | CHUA_LAM | — |
| E05 | Avatar public URL, documents chứa PDF báo cáo | CHUA_LAM | — |
| E06 | Bản ghi DNS App/MinIO/Keycloak, dig đúng | CHUA_LAM | — |
| E07 | Prometheus giám sát Web, target UP và metrics thật | CHUA_LAM | — |
| E08 | System Health of MSSV, 3 biểu đồ có dữ liệu | CHUA_LAM | — |
| E09 | Proxy `/student/` trả JSON backend | CHUA_LAM | — |
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
