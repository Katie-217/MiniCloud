# Kế hoạch triển khai: hoàn thành yêu cầu bắt buộc trước

Tài liệu này lưu kế hoạch giai đoạn nền tảng đã thực hiện. **Thứ tự hiện hành ngày 27/10/2026 nằm trong [KE_HOACH_HOAN_THIEN_LOCAL.md](KE_HOACH_HOAN_THIEN_LOCAL.md): hoàn tất local và 10 mở rộng → người dùng kiểm tra → AWS.** Nội dung yêu cầu gốc, số trang PDF và các lỗi trong mẫu nằm ở `KE_HOACH_MINICLOUD_2_NGAY.md`.

**Điều chỉnh theo chỉ dẫn mới nhất:** AWS chờ người dùng duyệt bản local cuối. Được thực hiện cả 10 mở rộng trước EC2; giữ EC2 và phần hồ sơ cloud ở trạng thái chờ.

## 1. Trạng thái setup đã kiểm tra

Kiểm tra ngày 26/10/2026 theo ngày của phiên làm việc:

| Thành phần | Thực tế quan sát được | Việc cần làm |
|---|---|---|
| Git | Có Git 2.49.0; đã có cấu hình author | Dùng cấu hình hiện có |
| GitHub CLI | Tài khoản Katie-217 có quyền ADMIN repo MiniCloud | Đã fetch/push; giữ lịch sử remote |
| Workspace Git | Có main và các branch nhóm, remote Katie-217/MiniCloud | Tích hợp từng nhóm sau kiểm thử |
| Docker CLI | Có phiên bản 29.0.1 | Không cần cài lại |
| Docker Compose | Có v2.40.3 | Không cần cài lại |
| Docker Engine | Lần kiểm tra sau đã kết nối được; server 29.0.1 | Đã sẵn sàng cho bước build/chạy container |
| WSL | Có thành phần `docker-desktop`; chưa thấy Ubuntu riêng | Chưa cần cài Ubuntu WSL chỉ để làm bài này; có thể dùng PowerShell và container công cụ |
| SSH | Có OpenSSH client | Cần thông tin kết nối EC2 khi triển khai |
| AWS CLI | Chưa có | Chưa cần cài nếu dùng Console và SSH |
| MSSV / nhóm | Võ Thị Thiên Kim 521H0092; Diệp Yến Nhi | Chờ MSSV Diệp Yến Nhi |
| Docker Hub | katie217; Web image 1.0.0 đã push và đọc lại manifest | Output R13 đạt |
| AWS EC2 | Người dùng yêu cầu để sau | Tiếp tục toàn bộ phần local; chưa tạo/truy cập EC2 |

Thông tin còn chờ: MSSV Diệp Yến Nhi và trạng thái EC2. Khi người dùng sẵn sàng phần AWS: public IP, username SSH và đường dẫn `.pem` trên máy; không gửi nội dung key/mật khẩu/token trong chat.

Git đã được khởi tạo cục bộ để có thể commit ngay, không phụ thuộc việc tạo remote. Commit tài liệu ban đầu dùng subject `docs: ghi nhận kế hoạch`; tạo `main` tại commit gốc này làm mốc khởi tạo, tiếp tục G0 trên `chore/project-foundation`. Khi nhận URL repo, đọc nội dung remote trước; nếu có lịch sử sẵn thì tích hợp hoặc chuyển các commit phù hợp, không dùng force push hay ghi đè lịch sử.

## 2. Các mốc hoàn thành

### M0 — đủ điều kiện bắt đầu

- Docker client kết nối được Linux engine; Compose gọi được Docker.
- Repo xác định rõ, quyền làm việc được kiểm chứng, có branch làm việc.
- Có MSSV/tên nhóm và namespace Docker Hub.
- AWS được tách khỏi mốc bắt đầu local theo yêu cầu mới nhất; trạng thái EC2 được giữ rõ trong bảng tiến độ.

### M1 — phần cơ bản local đạt

- Đạt R01–R12 và R15 trong `TIEN_DO_OUTPUT.md`.
- Có đủ 9 loại server, Compose mẫu tương ứng 10 container khi tính Node Exporter.
- Mỗi server được kiểm thử chức năng, không chỉ xem container ở trạng thái Running.
- Có log và ảnh minh chứng local; các mục chưa đạt được ghi rõ.

### M2 — phần cloud và image đạt

- R13: có ít nhất 1 image tùy chỉnh đã push Docker Hub.
- R14: toàn stack chạy trên EC2 Ubuntu; public Web/API hoạt động; test các server trên EC2 có bằng chứng.
- Bản cấu hình local/EC2 có hướng dẫn dựng lại và thông tin hostname phù hợp.

### M3 — đủ hồ sơ phần bắt buộc

- R16–R18: báo cáo 5 chương + phụ lục; link video; log/ảnh cho từng server, network, Docker Hub và EC2.
- `TIEN_DO_OUTPUT.md` phản ánh đúng kết quả; các lỗi còn lại và việc chưa làm đều được liệt kê.
- Quy tắc cũ chờ M3 mới mở rộng đã được thay thế: sửa lỗi bắt buộc local trước, rồi làm đủ 10 mở rộng trong kế hoạch hiện hành; không chờ EC2.

## 3. Branch theo nhóm yêu cầu

| Thứ tự | Branch | Công việc và output | Phụ thuộc / điều kiện tích hợp |
|---|---|---|---|
| G0 | `chore/project-foundation` | Kết nối Git; `.gitignore`, `.gitattributes`, `.env.example`; cấu trúc project; tài liệu, Compose nền; R01/R15 được cập nhật dần | M0; tài liệu và cấu trúc hợp lệ |
| G1 | `feat/web-api-database` | B01–B03 / R02–R04: Home, Blog, Flask hello, SQL init/seed; volume DB | G0; HTTP/JSON/SQL test đạt |
| G2 | `feat/identity-storage-dns` | B04–B06 / R05–R07: Keycloak, MinIO, Bind9; cấu hình lưu dữ liệu liên quan | G1; login/user, upload/download, dig có kết quả |
| G3 | `feat/monitoring-dashboard` | B07–B08 / R08–R09: Node Exporter, Prometheus, Grafana; datasource/dashboard dựng lại được | G2; target UP, query và biểu đồ có dữ liệu |
| G4 | `feat/gateway-network-tests` | B09–B10 / R10–R12: proxy Web/App/Auth, kiểm tra toàn mạng, kiểm thử lưu dữ liệu và restart policy | G3; M1 đạt, đủ bằng chứng local |
| G5a | `chore/image-publication` | R13: image Docker Hub, tag/digest và kiểm chứng registry | G4; đã hoàn thành độc lập AWS |
| G5b | `chore/cloud-deployment` | R14: triển khai EC2 và kiểm thử cloud | Chờ thông tin AWS từ người dùng; chưa tạo branch |
| G6 | `docs/submission-evidence` | R16–R18: báo cáo, ảnh/log, video local, hướng dẫn chạy và bảng tổng hợp | Làm bản local sau G5a; bổ sung cloud sau G5b trước M3 |

Mỗi branch có nhiều commit nhỏ theo chức năng/output. Kết thúc nhóm, kiểm thử các luồng liên quan và tích hợp vào `main`; branch sau tạo từ `main` đã cập nhật. Có thể push branch để theo dõi sau khi repo đã được kết nối. PR chỉ dùng nếu quy trình repo cần.

Các branch mở rộng và thứ tự mới được xác định trong `KE_HOACH_HOAN_THIEN_LOCAL.md`. Bảng trạng thái vẫn ghi E01–E10 chưa làm cho đến khi có kiểm thử thực tế.

## 4. Task chi tiết và kiểm thử theo nhóm

| Nhóm | Các bước thực hiện | Test bắt buộc / bằng chứng cần lưu |
|---|---|---|
| G0 | Xác minh remote; bảo toàn PDF/tài liệu; khai báo mạng `cloud-net`, quy ước tên service/cổng; cấu hình line ending cho file Linux; chuẩn bị biến môi trường | Git status/remote đúng; Compose parse được khi có service; config mẫu không chứa bí mật thật |
| G1 | Web: Dockerfile, Nginx config, Home/Blog; App: Flask `/hello`, chuẩn bị `/secure` theo mẫu; DB: SQL `minicloud.notes`, seed và volume | Home/Blog 200; `/hello` JSON đúng; SQL có bảng/dữ liệu; lưu log riêng từng output |
| G2 | Keycloak: admin, user test, cấu hình path/hostname rõ ràng; MinIO: volume, demo bucket, upload/download; Bind9: zone và bản ghi | Ảnh login/user; file tải về đúng; dig Web trả 10.10.10.10; service names khớp Compose |
| G3 | Exporter → Prometheus → Grafana; datasource dùng tên service; lưu dashboard/provisioning để EC2 dựng lại | Node target UP, CPU metric có dữ liệu; biểu đồ CPU/RAM/Network không rỗng; ghi rõ phạm vi số liệu |
| G4 | Proxy `/`, `/api/`, `/auth/`; kiểm tra readiness; ping tất cả service từ container công cụ; hoàn thiện volume/restart; thử recreate các service lưu dữ liệu | HTTP/JSON/redirect đúng; ping/name resolution thành công; dữ liệu mẫu vẫn còn sau recreate, không xóa volume |
| G5 | Tag/push Web image; kiểm tra EC2/SSH, Docker/Compose; chuyển config, dùng URL public; dựng full stack; chạy lại bộ kiểm thử | Docker Hub repository/tag + push log; `compose ps` trên EC2; Web/API qua public IP; bằng chứng từng server trên EC2 |
| G6 | Tổng hợp kết quả expected/actual; vẽ sơ đồ đúng kiến trúc cuối; viết báo cáo; chụp ảnh và quay demo; kiểm tra link | Báo cáo đủ chương, minh chứng từng server, link video/Hub dùng được; liệt kê lỗi/chưa làm trung thực |

Ảnh UI cần thao tác trình duyệt: tự động hóa khi môi trường có công cụ phù hợp; nếu cần bạn thao tác/chụp ảnh, ghi rõ task và ảnh còn thiếu trong bảng output. Không đánh dấu minh chứng đã có trước khi file tồn tại và nội dung được kiểm tra.

## 5. Quy ước commit

Định dạng đã chốt theo yêu cầu mới nhất: **`type: English summary of 4–5 words`**. Thông điệp bằng tiếng Anh, ngắn gọn, đúng ý chính; không tính tiền tố vào số từ. Không thêm dấu `*` vào subject. Commit cũ đã có trên remote được giữ nguyên lịch sử.

| Tình huống | Ví dụ commit |
|---|---|
| Lưu kế hoạch/quy ước | `docs: record project implementation plan` |
| Tạo cấu trúc | `chore: initialize project directory structure` |
| Thêm Home | `feat: serve project home page` |
| Thêm Blog | `feat: serve static blog page` |
| API hello | `feat: add hello API endpoint` |
| Seed DB | `feat: initialize database seed records` |
| Sửa routing | `fix: correct authentication proxy routing` |
| Bổ sung test | `test: verify internal network connectivity` |
| Lưu evidence | `docs: capture local verification evidence` |
| Cập nhật trạng thái riêng | `docs: update output tracking status` |

Quy trình mỗi commit: sửa một chức năng/output → kiểm tra diff → chạy test liên quan → cập nhật `TIEN_DO_OUTPUT.md` → commit đúng file. Những thay đổi phục vụ cùng một output có thể nằm chung commit; không gom Web, DB và Auth thành một commit duy nhất.

Khi bắt đầu triển khai, file tiến độ ghi branch, subject hoặc hash commit đã có, test và bằng chứng. Một output mới có code nhưng chưa chạy được sẽ mang trạng thái `CHO_KIEM_THU`, không phải `DAT`.

## 6. Lịch dự kiến ban đầu — đã được thay thế ngày 27/10/2026

Giả định tổng khoảng 20 giờ làm tập trung; đây là dự kiến, không phải bảo đảm mọi bước sẽ vừa thời lượng khi còn thiếu repo/Docker/EC2.

| Thời gian | Công việc | Mục tiêu |
|---|---|---|
| Ngày 1, giờ 0–0,5 | Setup và G0 | M0; repo/branch và cấu trúc sẵn sàng |
| Ngày 1, giờ 0,5–2 | G1 | Web/App/DB có test |
| Ngày 1, giờ 2–4 | G2 | Auth/Storage/DNS có test |
| Ngày 1, giờ 4–5,5 | G3 | Monitoring và dashboard có dữ liệu |
| Ngày 1, giờ 5,5–7,5 | G4, kiểm tra tổng thể local | M1; lưu evidence local |
| Ngày 1, giờ 7,5–10 | G5 vòng đầu | Push image; dựng EC2, xác minh truy cập public |
| Ngày 2, giờ 0–2 | Hoàn tất G5, kiểm thử toàn stack EC2 | M2; xử lý lỗi cloud trước |
| Ngày 2, giờ 2–4 | G6: báo cáo, evidence và video phần cơ bản | M3; bảng output bắt buộc đầy đủ |
| Ngày 2, giờ 4–8 | Mở rộng sau M3, chọn theo thời gian thực tế | Làm từng mục có test/commit; cập nhật báo cáo và video tương ứng |
| Ngày 2, giờ 8–10 | Dự phòng và kiểm tra bộ nộp cuối | File tổng hợp phản ánh đúng tất cả đã làm/chưa làm |

Lịch trên chỉ lưu phương án ban đầu. Không dùng các bước AWS trong lịch này trước khi người dùng duyệt local. Thời lượng và thứ tự phần việc còn lại dùng kế hoạch hiện hành; mục tiêu là đủ 10 mở rộng, không tự giảm phạm vi theo lịch cũ.
