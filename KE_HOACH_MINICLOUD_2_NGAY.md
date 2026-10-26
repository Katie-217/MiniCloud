# MyMiniCloud: yêu cầu, task, output và kế hoạch 2 ngày

Nguồn: **Báo Cáo Cuối Kỳ.docx.pdf**, 27 trang, trong workspace. Số trang bên dưới là số trang PDF, tính từ 1. Đã đọc phần chữ và xem các hình kiến trúc, cấu trúc thư mục, kết quả khởi động ở trang 2, 3, 11.

**Cập nhật theo yêu cầu làm việc:** hoàn tất và kiểm thử toàn bộ phần bắt buộc, bao gồm EC2/Docker Hub/hồ sơ nộp, trước khi làm mở rộng. Dùng [kế hoạch triển khai theo branch](KE_HOACH_TRIEN_KHAI_BAT_BUOC.md) làm thứ tự thực hiện và [bảng output](TIEN_DO_OUTPUT.md) để theo dõi đã đạt, cần fix, chưa làm. Quy ước commit nằm trong `AGENTS.md`.

Đây là tài liệu phân tích và kế hoạch thực hiện; chưa phải kết quả triển khai hay minh chứng đã chạy thành công. Các thời lượng, tên file minh chứng và cách tổ chức thư mục là đề xuất, không phải quy định của giảng viên.

## 1. Phạm vi và cách chấm điểm

- Xây dựng mô phỏng cloud tên MyMiniCloud, gồm **9 loại server**, container hóa và giao tiếp qua Docker Network; chạy trên **local và AWS EC2 Ubuntu** (trang 1–3).
- **Phần cơ bản: 5 điểm** theo ghi chú sau phần demo và kiểm tra mạng (trang 21). PDF không chia điểm riêng từng task cơ bản.
- **Phần mở rộng: 5 điểm**, thực tế có **10 mục × 0,5 điểm**, dù đoạn giới thiệu ghi 9 yêu cầu (trang 21, 26–27).
- Muốn phủ toàn bộ thang điểm: hoàn thành phần cơ bản, 10 mục mở rộng, triển khai EC2, Docker Hub và hồ sơ báo cáo. Đây là phạm vi công việc theo tài liệu, không phải cam kết điểm số.
- Báo cáo phải **ghi rõ đã hoàn thành bao nhiêu mục mở rộng** (trang 27).
- PDF không nêu số trang báo cáo, thời lượng video, hạn nộp cụ thể hay cấu hình EC2 tối thiểu. Mốc 2 ngày là yêu cầu của bạn.

## 2. Đầu ra cuối cùng cần chuẩn bị

| Đầu ra | Nội dung phải có | Căn cứ |
|---|---|---|
| Hệ thống local | Đủ 9 loại server, khởi động bằng Compose, kiểm thử từng server và thông mạng | Trang 1–3, 11–20 |
| Hệ thống AWS | Toàn bộ hệ thống chạy trên EC2 Ubuntu, truy cập được qua public IP | Trang 1, 3 |
| Mã nguồn và cấu hình | Dockerfile tùy chỉnh, HTML, Flask, SQL, DNS, Nginx, Prometheus, `docker-compose.yml`; giữ cấu hình có thể dựng lại | Trang 3–11 |
| Image trên Docker Hub | Ít nhất 1 image tùy chỉnh, có đường dẫn repository/tag để đối chiếu | Trang 3 |
| Báo cáo cuối kỳ | 5 chương và phụ lục; ảnh từng server; thống kê các phần mở rộng đã làm | Trang 3, 27 |
| Video demo | Có link video trong phụ lục; nên thể hiện cả local và EC2 | Trang 3; cách quay là đề xuất |
| Log kiểm thử | Kết quả lệnh kiểm thử, trạng thái container, query và kết quả tương ứng | Trang 3, 11–20 |
| Sản phẩm mở rộng | 10 đầu ra ở mục 6, nếu hướng tới đủ 5 điểm mở rộng | Trang 21–27 |

PDF yêu cầu trình bày code/config trong báo cáo nhưng không chỉ rõ phải nộp ZIP hay Git repository. Nên đóng gói source hoặc chuẩn bị repository để người chấm dựng lại được.

## 3. Yêu cầu kỹ thuật chung và quyết định triển khai

### Những điều PDF yêu cầu

- Các container cùng mạng tên **`cloud-net`**.
- Khởi động toàn bộ bằng **`docker-compose.yml`**.
- Mỗi service có tên container riêng, ánh xạ cổng phù hợp, volume khi cần và **`restart: unless-stopped`**.
- Có thể dùng image có sẵn; **không bắt buộc viết 9 Dockerfile**. Web và Flask là hai chỗ phù hợp để build image tùy chỉnh.
- Có kiểm thử từng server, truy vấn DNS, kiểm tra thông mạng, monitoring và proxy.
- Push ít nhất một image tùy chỉnh lên Docker Hub và chạy toàn hệ thống trên EC2 Ubuntu.

### Cổng thống nhất để thực hiện

Dùng bảng cổng trong phần hướng dẫn chi tiết trang 4, 9–10; bảng tổng quan trang 2 có cổng App khác.

| Service | Cổng trên host local | Cổng trong container | Cách truy cập |
|---|---|---|---|
| Reverse proxy | 80 | 80 | `http://localhost/` |
| Web | 8080 | 80 | `http://localhost:8080/` |
| Flask App | 8085 | 8081 | `http://localhost:8085/hello` |
| MariaDB | 3306 trong mẫu | 3306 | Qua `docker compose exec` hoặc client cùng mạng |
| Keycloak | 8081 | 8080 | `http://localhost:8081/`; đường dẫn phụ thuộc cấu hình `/auth` đã chọn |
| MinIO API | 9000 | 9000 | URL object dùng cổng này |
| MinIO Console | 9001 | 9001 | `http://localhost:9001/` |
| Bind9 | 1053/UDP | 53/UDP | `dig @127.0.0.1 -p 1053 ...` |
| Node Exporter | 9100 trong mẫu | 9100 | `/metrics`; Prometheus gọi trong mạng |
| Prometheus | 9090 | 9090 | `http://localhost:9090/` |
| Grafana | 3000 | 3000 | `http://localhost:3000/` |

Ở EC2, URL trình duyệt dùng public IP thay cho `localhost`. Container gọi nhau bằng **tên service và cổng nội bộ**. DB và exporter không cần mở công khai để thực hiện demo qua SSH và các giao diện tương ứng. Phân biệt cổng host/cổng container theo [Docker Compose Networking](https://docs.docker.com/compose/how-tos/networking/).

## 4. Các task nền tảng dùng chung

| ID | Task và cách làm | Output cụ thể | Điều kiện hoàn thành / minh chứng |
|---|---|---|---|
| T00 | Kiểm tra Docker/Compose; chuẩn bị Docker Hub, quyền dùng EC2, SSH, MSSV, tên nhóm, ảnh đại diện và nội dung blog | Danh sách thông tin sẵn sàng; Docker hoạt động; có phương án truy cập EC2 | Biết chắc có thể dùng EC2 và Docker Hub ngay đầu ngày 1 |
| T01 | Tạo 9 thư mục service như trang 4; viết Compose; khai báo `cloud-net`, container name, port, restart, volume; thêm healthcheck khi cần | `docker-compose.yml`, thư mục service, `.env.example`, README đề xuất | `docker compose config` hợp lệ; `docker compose up -d --build` dựng được hệ thống |
| T02 | Thực hiện B01–B09 bên dưới; lưu ảnh/log ngay khi kiểm thử đạt | Hệ thống cơ bản đủ vai trò | Tất cả test cơ bản có kết quả thực tế |
| T03 | Kiểm tra mạng từ container công cụ tạm trên `cloud-net`; ping đúng tên tất cả service, gồm proxy và exporter | `network-test.txt`, `docker network inspect cloud-net` | Có kết quả phân giải tên và ping; xác minh dịch vụ thêm bằng HTTP/SQL/DNS |
| T04 | Đặt tag theo tài khoản Docker Hub, build và push ít nhất image Web; lưu link/tag | Image tùy chỉnh trên Docker Hub, `dockerhub.txt` | `docker push` thành công, repository/tag hiển thị; tốt nhất EC2 pull và dùng chính image này |
| T05 | Trên EC2 Ubuntu: cài Docker/Compose; chuyển source/config; tạo `.env`; điều chỉnh URL public; dựng toàn hệ thống; chạy lại các test | Hệ thống EC2; URL public; log `docker compose ps` trên EC2 | Web/API qua public IP chạy; 9 nhóm server được kiểm thử trên EC2; không chỉ upload source |
| T06 | Làm 10 mục mở rộng; giữ kết quả từng mục riêng | Các sản phẩm E01–E10 | Đánh dấu mục nào đã có minh chứng, mục nào chưa |
| T07 | Viết báo cáo, dựng sơ đồ thực tế, gom log/ảnh, quay video, kiểm tra link | Báo cáo, video, thư mục evidence, source có hướng dẫn chạy | Đủ 5 chương/phụ lục; link mở được; ghi đúng số mục mở rộng hoàn thành |

Chuỗi phụ thuộc: `T00 → T01 → B01–B09 → T03 → T04/T05 → kiểm thử cuối → T07`. Có thể viết báo cáo và làm mở rộng sau khi từng service ổn định; không cần đợi tất cả xong mới chụp ảnh.

## 5. Task cơ bản theo từng server — phần demo 5 điểm

### B01. Web Frontend — Nginx

- **Nguồn:** trang 4–5, 11–13.
- **Yêu cầu:** phục vụ trang chủ và `/blog/`.
- **Cách làm:** tạo `web-frontend-server/html/index.html` và `html/blog/index.html`; viết Nginx config với `root`, `index`, `/blog/`; tạo Dockerfile copy HTML/config vào image; publish `8080:80`.
- **Output:** Dockerfile + Nginx config + hai trang HTML; Web chạy trực tiếp và qua proxy.
- **Kiểm thử:** `curl.exe -I http://localhost:8080/` và `curl.exe -I http://localhost:8080/blog/` trên PowerShell.
- **Kết quả đạt:** HTTP 200; trang chủ có nội dung MyMiniCloud Home và trang blog có nội dung MyMiniCloud Blog.
- **Minh chứng đề xuất:** `B01-home.png`, `B01-blog.png`, `B01-http.txt`.

### B02. Application Backend — Flask

- **Nguồn:** trang 5–6, 13.
- **Yêu cầu:** `/hello` trả JSON; gọi trực tiếp và qua proxy đều thành công. Mẫu còn cung cấp `/secure` để dùng với phần Auth mở rộng.
- **Cách làm:** viết `application-backend-server/app.py`; Flask listen `0.0.0.0:8081`; cài thư viện cần thiết trong image; publish `8085:8081`; proxy strip tiền tố `/api/`.
- **Output:** Flask app, Dockerfile, endpoint `/hello` và phần xử lý `/secure`.
- **Kiểm thử:** `curl.exe http://localhost:8085/hello` và `curl.exe http://localhost/api/hello`.
- **Kết quả đạt:** cả hai trả `{"message":"Hello from App Server!"}`.
- **Minh chứng:** `B02-api-direct.txt`, `B02-api-proxy.txt`.
- **Lưu ý phạm vi:** trang 1 mô tả App có kết nối DB nhưng mẫu Flask chưa làm. Trang 23 coi kết nối Flask–DB là tùy chọn. Đề xuất thêm API `/students-db` đọc thật từ MariaDB để thể hiện rõ kiến trúc, sau khi các yêu cầu chấm điểm chính đã ổn định.

### B03. Relational Database — MariaDB

- **Nguồn:** trang 6, 14.
- **Yêu cầu:** tự tạo database `minicloud`, bảng `notes`, ít nhất một dòng `Hello from MariaDB!`.
- **Cách làm:** viết `relational-database-server/init/001_init.sql`; mount vào `/docker-entrypoint-initdb.d`; thêm volume dữ liệu DB; dùng đúng service `relational-database-server` để truy cập.
- **Output:** SQL khởi tạo, database và dữ liệu truy vấn được.
- **Kiểm thử mẫu cho môi trường lab dùng mật khẩu trong PDF:**

```powershell
docker compose exec relational-database-server mariadb -uroot -proot -e "USE minicloud; SHOW TABLES; SELECT * FROM notes;"
```

- **Kết quả đạt:** bảng `notes` tồn tại; có dữ liệu ban đầu.
- **Minh chứng:** `B03-db-query.txt`, ảnh truy vấn nếu cần.
- **Lưu ý:** mount script init không thay thế volume lưu dữ liệu. Nếu DB đã khởi tạo, chỉnh script init không có nghĩa dữ liệu cũ tự được cập nhật; có thể chạy SQL bổ sung trực tiếp, tránh xóa volume chỉ để thêm bảng.

### B04. Authentication & Identity — Keycloak

- **Nguồn:** trang 7, 9, 14–15.
- **Yêu cầu:** đăng nhập quản trị được và tạo user test `sv01`.
- **Cách làm:** chạy image Keycloak với cấu hình bootstrap admin; mở cổng host 8081; đăng nhập và tạo user; đặt mật khẩu để dùng tiếp ở E04; lưu cấu hình/realm để dựng lại.
- **Output:** Keycloak hoạt động, admin console truy cập được, user `sv01` tồn tại.
- **Kiểm thử:** mở `http://localhost:8081/` theo cấu hình gốc hoặc URL có `/auth/` nếu đã đổi context path.
- **Kết quả đạt:** vào được giao diện quản trị, xem được user vừa tạo.
- **Minh chứng:** `B04-keycloak-admin.png`, `B04-user-sv01.png`.
- **Lưu ý:** `admin/admin` là tài khoản mẫu trong PDF; cấu hình EC2 phải dùng thông tin thực tế của bạn.

### B05. Object Storage — MinIO

- **Nguồn:** trang 7, 10, 15–16; bảng trang 2 còn yêu cầu upload/tải file.
- **Yêu cầu:** truy cập Console; tạo bucket `demo`; upload `index.html` từ Web; xác minh tải về được.
- **Cách làm:** chạy MinIO với API 9000 và Console 9001; mount `/data`; đăng nhập; tạo bucket và upload. Chọn phiên bản có giao diện/chức năng phù hợp hoặc dùng client MinIO khi cần.
- **Output:** bucket `demo` chứa `index.html`, dữ liệu tồn tại trên volume.
- **Kết quả đạt:** object hiển thị, tải về và mở được.
- **Minh chứng:** `B05-bucket-demo.png`, file tải về hoặc log tải xuống.

### B06. Internal DNS — Bind9

- **Nguồn:** trang 7, 16–17.
- **Yêu cầu:** phân giải `web-frontend-server.cloud.local` thành `10.10.10.10` như cấu hình đề.
- **Cách làm:** tạo `named.conf.options`, `named.conf.local`, `db.cloud.local`; mount vào Bind9; publish UDP `1053:53`.
- **Kiểm thử:** chạy bằng WSL/Ubuntu hoặc container có `dig`:

```bash
dig @127.0.0.1 -p 1053 web-frontend-server.cloud.local +short
```

- **Output:** zone `cloud.local`, bản ghi Web và kết quả `dig`.
- **Kết quả đạt:** trả `10.10.10.10`.
- **Minh chứng:** `B06-dig-web.txt`, bản sao zone file.
- **Lưu ý:** đây là IP mẫu. Query DNS đúng chưa chứng minh HTTP truy cập được tại IP đó. Nếu muốn dùng zone để gọi dịch vụ thật, phải thiết kế subnet/IP tương ứng; không cần làm thêm việc này chỉ để đạt test DNS trong PDF.

### B07. Monitoring — Prometheus + Node Exporter

- **Nguồn:** trang 7, 10, 17–18.
- **Yêu cầu:** Prometheus scrape Node Exporter; target `monitoring-node-exporter-server:9100` ở trạng thái UP; query `node_cpu_seconds_total` có dữ liệu.
- **Cách làm:** chạy thêm container exporter; cấu hình scrape interval và target trong `monitoring-prometheus-server/prometheus.yml`; mount config; mở Prometheus cổng 9090.
- **Output:** config Prometheus, target UP, metrics có thể truy vấn.
- **Kiểm thử:** trang Targets và truy vấn `node_cpu_seconds_total`; có thể kiểm tra `up{job="node"}` bằng 1.
- **Minh chứng:** `B07-target-node-up.png`, `B07-node-metrics.png`.
- **Phạm vi đo:** Node Exporter trong container cần cấu hình truy cập host phù hợp. Với Docker Desktop, phải ghi rõ số liệu thuộc môi trường Linux chạy Docker; không mặc nhiên coi là toàn bộ Windows hay số liệu từng container. Xem [Node Exporter Docker](https://github.com/prometheus/node_exporter#docker).

### B08. Visualization — Grafana

- **Nguồn:** trang 2, 7, 18–19.
- **Yêu cầu:** thêm datasource Prometheus, import dashboard Node Exporter, hiển thị CPU/RAM/Network.
- **Cách làm:** chạy Grafana cổng 3000, thêm volume; cấu hình datasource **`http://monitoring-prometheus-server:9090`**; import dashboard Node Exporter phù hợp. Có thể provision datasource/dashboard bằng file để EC2 dựng lại nhanh.
- **Output:** datasource hoạt động và dashboard có dữ liệu.
- **Kết quả đạt:** panel hiển thị dữ liệu thật, không chỉ tạo được dashboard rỗng.
- **Minh chứng:** `B08-datasource.png`, `B08-node-dashboard.png`.
- **Giới hạn theo đề:** trang 1 gọi nhóm này là Logging/Visualization; bài hướng dẫn và test dùng Grafana + Prometheus. Cấu hình đó cung cấp biểu đồ metrics, chưa phải hệ thống thu thập log tập trung. Lưu `docker compose logs` cho phụ lục; PDF không đưa một task Loki bắt buộc riêng.

### B09. Reverse Proxy / API Gateway — Nginx

- **Nguồn:** trang 8, 10–11, 19–20.
- **Yêu cầu:** một cổng vào chung để gọi Web, App và Auth.
- **Cách làm:** viết `api-gateway-proxy-server/nginx.conf`; `/` tới Web; `/api/` tới Flask và bỏ tiền tố; `/auth/` tới Keycloak với context path nhất quán.
- **Output:** proxy chạy cổng 80, config route và các endpoint hợp nhất.
- **Kiểm thử:**

```powershell
curl.exe -I http://localhost/
curl.exe http://localhost/api/hello
curl.exe -I http://localhost/auth/
```

- **Kết quả đề ghi:** `/` trả 200; `/api/hello` trả JSON; `/auth/` trả redirect 302 đến đăng nhập. Khi kiểm thử thực tế, lưu cả status và `Location`, đồng thời xác minh trình duyệt theo redirect đến trang đúng.
- **Minh chứng:** `B09-proxy-routes.txt`, `B09-auth-through-proxy.png`.

### B10. Kiểm tra thông mạng toàn hệ thống

- **Nguồn:** trang 20.
- **Yêu cầu:** ping các server trong cùng mạng; ghi kết quả thông mạng.
- **Cách làm:** chạy một container công cụ tạm có `ping` trên `cloud-net`; ping tên service thực tế trong Compose. Ví dụ trên PowerShell:

```powershell
docker run --rm --network cloud-net alpine ping -c 3 web-frontend-server
```

- Lặp lại với App, DB, Auth, Storage, DNS, Prometheus, Grafana, Proxy và Node Exporter. Container công cụ dùng xong sẽ tự xóa.
- **Output:** log ping, danh sách container thuộc network.
- **Kết quả đạt:** phân giải được tên và nhận phản hồi từ các service; kiểm thử chức năng ở B01–B09 vẫn phải đạt.
- **Minh chứng:** `B10-network-test.txt`, `B10-network-inspect.txt`.

## 6. Mười task mở rộng — mỗi task 0,5 điểm

### E01. Blog cá nhân 3 bài — trang 21

- **Yêu cầu/output:** `blog1.html`, `blog2.html`, `blog3.html` trong `/blog/`; mỗi bài có ảnh minh họa và liên kết quay lại trang chính; `index.html` có danh sách hyperlink.
- **Cách làm:** chọn một chủ đề, viết 3 bài ngắn có nội dung riêng; lưu ảnh vào thư mục Web; cập nhật danh sách bài trên trang chủ và trang blog để tránh mơ hồ; build lại image.
- **Điều kiện đạt:** mở đủ 3 bài qua Web và proxy, ảnh và liên kết hoạt động.
- **Minh chứng:** ảnh danh sách + ảnh 3 bài; giữ các HTML/ảnh trong source.
- **Ước lượng:** 45 phút nếu nội dung đã chuẩn bị.

### E02. API `/student` đọc JSON — trang 22

- **Yêu cầu/output:** `students.json` có **5 sinh viên**, mỗi bản ghi có `id`, `name`, `major`, `gpa`; Flask thêm `GET /student`.
- **Cách làm:** tạo JSON UTF-8; import `json`; đọc file bằng đường dẫn rõ ràng; bổ sung `COPY students.json` vào Dockerfile; trả `jsonify(data)`; build lại App.
- **Kiểm thử:** `http://localhost:8085/student` và **`http://localhost/api/student`**.
- **Điều kiện đạt:** HTTP 200, mảng JSON đúng 5 bản ghi và đủ trường; không lỗi thiếu file trong container.
- **Minh chứng:** file JSON, đoạn route, log response trực tiếp/qua proxy.
- **Ước lượng:** 30 phút.

### E03. Database sinh viên — trang 23

- **Yêu cầu/output:** database **`studentdb`**, bảng **`students`**, tối thiểu **3 bản ghi**; cấu trúc:

```sql
id INT PRIMARY KEY AUTO_INCREMENT,
student_id VARCHAR(10),
fullname VARCHAR(100),
dob DATE,
major VARCHAR(50)
```

- **Cách làm:** viết SQL tạo DB/bảng/seed; áp dụng vào MariaDB; chạy `DESCRIBE studentdb.students` và `SELECT * FROM studentdb.students`; giữ SQL trong source.
- **Điều kiện đạt:** đúng tên DB/bảng, đúng các cột và tối thiểu 3 dòng.
- **Tùy chọn theo PDF:** thực hành SELECT/UPDATE/DELETE và kết nối Flask đọc DB qua `/students-db`; đây không phải một mục 0,5 điểm bổ sung riêng.
- **Minh chứng:** SQL + output schema/query; API response nếu có làm kết nối.
- **Ước lượng:** 30 phút phần bắt buộc; thêm khoảng 30 phút cho API đọc DB.

### E04. Keycloak realm/client/token và `/secure` — trang 23–24

- **Yêu cầu/output:** realm theo MSSV, ví dụ `realm_sv001`; 2 user **`sv01`, `sv02`**; client public **`flask-app`**; lấy token endpoint và gọi `/secure`.
- **Cách làm:** tạo realm/client/user; đặt mật khẩu; dùng token endpoint từ OIDC discovery của realm; lấy access token; cấu hình backend kiểm tra token; gọi `/api/secure` kèm `Authorization: Bearer ...`.
- **Điều kiện đạt:** token hợp lệ trả `Secure resource OK` và đúng username. Nên lưu thêm test không có token trả 401 để chứng minh endpoint có bảo vệ.
- **Điểm cần cấu hình:** public client tương ứng `Client authentication: Off`; nếu test bằng password grant thì bật Direct Access Grants. `iss` phải khớp issuer backend, JWKS phải truy cập được; `aud` cần chứa audience backend, có thể thêm Audience mapper. Không bỏ kiểm tra chữ ký/issuer/audience để vượt test. Tham khảo [Keycloak Admin Guide](https://www.keycloak.org/docs/latest/server_admin/index.html#_oidc_clients) và [hostname](https://www.keycloak.org/server/hostname).
- **Minh chứng:** ảnh realm, 2 user, client; URL endpoint; response `/secure`; export realm để dựng lại. Không cần đưa token đầy đủ vào báo cáo.
- **Ước lượng:** 90 phút sau khi Auth cơ bản hoạt động; có thể lâu hơn nếu URL local/EC2 không thống nhất.

### E05. MinIO avatar public và tài liệu — trang 24

- **Yêu cầu/output:** bucket **`profile-pics`** có **`avatar.jpg`**; URL object truy cập được công khai; bucket **`documents`** có PDF báo cáo.
- **Cách làm:** tạo bucket; upload avatar; thiết lập quyền đọc công khai cho avatar; lấy URL từ **API endpoint cổng 9000**; thử mở không có phiên đăng nhập; tạo bucket documents và upload PDF báo cáo.
- **Điều kiện đạt:** avatar mở/tải được từ URL; PDF có trong documents. Đề chỉ yêu cầu URL public cho avatar, không yêu cầu documents phải public.
- **Minh chứng:** ảnh 2 bucket/object; URL avatar và ảnh mở từ phiên ẩn danh; ảnh PDF báo cáo đã upload.
- **Ước lượng:** 30 phút; upload lại bản PDF cuối khi hoàn thiện báo cáo.

### E06. DNS mở rộng — trang 25

- **Yêu cầu/output:** thêm `app-backend.cloud.local` → **`10.10.10.20`**, thêm `minio.cloud.local` và `keycloak.cloud.local`.
- **Cách làm:** sửa zone file; chọn và ghi rõ IP cho MinIO/Keycloak vì đề không chỉ định; tăng SOA serial, kiểm tra cấu hình rồi restart/reload Bind9; chạy `dig` cho từng tên.
- **Điều kiện đạt:** cả 3 bản ghi mới trả đúng IP đã khai báo; bản ghi Web cũ vẫn đúng.
- **Minh chứng:** zone file và 4 kết quả `dig` gồm cả Web.
- **Ước lượng:** 30 phút.

### E07. Prometheus giám sát Web — trang 25

- **Yêu cầu/output theo đề:** thêm job **`web`** cho `web-frontend-server:80`, target mới **UP**.
- **Vấn đề với mẫu:** chỉ thêm target không đủ; Web tĩnh ở phần trước chưa cung cấp `/metrics` đúng định dạng Prometheus.
- **Cách làm đề xuất:** bật `stub_status` trên Web; thêm **NGINX Prometheus Exporter** đọc endpoint này; cho Web proxy `/metrics` tới exporter; Prometheus vẫn scrape `web-frontend-server:80` với `metrics_path: /metrics` đúng địa chỉ trong đề. Luồng: `Prometheus → Web /metrics → Exporter → Web /stub_status`. Cơ chế exporter tham khảo [tài liệu chính thức NGINX](https://github.com/nginx/nginx-prometheus-exporter#readme).
- **Output bổ sung:** config `stub_status`, exporter service, route `/metrics`, scrape job web.
- **Điều kiện đạt:** `up{job="web"} = 1`, metric `nginx_up{job="web"} = 1`; có metrics thật, không chỉ trang HTML trả 200. Endpoint stub_status cần để exporter truy cập được trong mạng.
- **Minh chứng:** Targets có node và web UP; query metric Nginx; config liên quan.
- **Ước lượng:** 45 phút nếu hiểu cấu hình Nginx; có thể cần dự phòng thêm.
- Đây là phương án sửa kỹ thuật, không phải đoạn cấu hình có sẵn trong PDF. Exporter làm tăng số container, cần ghi rõ trong kiến trúc.

### E08. Dashboard cá nhân 3 biểu đồ — trang 25–26

- **Yêu cầu/output:** dashboard tên **`System Health of <MSSV>`**, dùng datasource Prometheus; có CPU Usage (%), Memory Usage, Network Traffic; lưu dashboard và chụp ảnh.
- **Cách làm đề xuất:** tạo 3 panel, chọn đơn vị tương ứng và time range đủ dài; dùng PromQL dưới đây sau khi đã có metrics. Nếu job exporter đổi tên thì sửa filter `job`.

```promql
# CPU Usage, đơn vị phần trăm
100 * (1 - avg by (instance) (rate(node_cpu_seconds_total{job="node",mode="idle"}[5m])))

# Memory Usage, đơn vị phần trăm
100 * (1 - node_memory_MemAvailable_bytes{job="node"} / node_memory_MemTotal_bytes{job="node"})

# Network nhận vào, đơn vị bytes/giây
sum by (instance) (rate(node_network_receive_bytes_total{job="node",device!="lo"}[5m]))
```

- **Điều kiện đạt:** đúng tên, ít nhất 3 panel, có dữ liệu thật. Counter CPU/Network cần `rate` để thể hiện mức sử dụng/tốc độ thay vì chỉ số tích lũy.
- **Minh chứng:** ảnh toàn dashboard và file JSON export; khuyến nghị provision file để triển khai lại trên EC2.
- **Ước lượng:** 45 phút.

### E09. Route `/student/` qua proxy — trang 26

- **Yêu cầu/output:** Nginx `/student/` trỏ vào Flask `/student`, trả danh sách sinh viên JSON.
- **Cách làm:** thêm route vào Nginx; có thể dùng `location = /student/ { proxy_pass http://application-backend-server:8081/student; }` cho chính xác URL cần test; kiểm tra `nginx -t`, reload/restart proxy.
- **Kiểm thử:** `curl.exe http://localhost/student/`.
- **Điều kiện đạt:** cùng dữ liệu 5 sinh viên như `/api/student`; không lỗi dấu `/` hay route 404.
- **Minh chứng:** Nginx config và `E09-student-proxy.txt`.
- **Ước lượng:** 15 phút.

### E10. Load Balancing Round Robin — trang 26–27

- **Yêu cầu/output:** 2 Web server **`web-frontend-server1`**, **`web-frontend-server2`**; Nginx upstream round robin; kết quả trả về luân phiên giữa 2 trang.
- **Cách làm:** tạo 2 container Web có nội dung/header nhận diện rõ `WEB-1`/`WEB-2`; khai báo upstream gồm 2 backend; thêm route demo cân bằng tải, ví dụ `/lb/`; để Nginx dùng round robin mặc định.
- **Kiểm thử:** gửi ít nhất 6 request tuần tự bằng `curl.exe`; lưu body/header nhận diện từng Web. Dùng terminal giúp tránh cache trình duyệt.
- **Điều kiện đạt:** cả 2 backend được phục vụ; ghi lại chuỗi luân phiên trong điều kiện cả 2 backend khỏe. Cân bằng tải vẫn hoạt động trên EC2.
- **Minh chứng:** cấu hình upstream, danh sách 2 Web container, `E10-round-robin.txt`.
- **Ước lượng:** 45 phút.
- Đề không chỉ định URL `/lb/`; đây là route demo đề xuất để giữ các route Web/API hiện có đơn giản. Có thể dùng 2 Web làm upstream chính nếu muốn.

## 7. Những điểm cần xử lý trước khi chép mẫu trong PDF

| Điểm trong PDF | Hệ quả | Cách xử lý đề xuất |
|---|---|---|
| Trang 1 ghi tổng 9 container; trang 8–10 có 9 server + Node Exporter | Compose mẫu thực tế có 10 service | Hiểu là 9 loại server; báo cáo số container thực tế, exporter là thành phần hỗ trợ |
| Trang 21 ghi 9 mở rộng; bảng chấm điểm có 10 | Dễ bỏ mục cân bằng tải 0,5 điểm | Theo đủ E01–E10 |
| App cổng 8081 ở bảng đầu; hướng dẫn chi tiết dùng 8085 | Xung đột với Keycloak nếu chép lẫn | App host 8085, nội bộ 8081; Auth host 8081, nội bộ 8080 |
| Lệnh dùng `db`, `prometheus`, `web`, `keycloak`, nhưng service có tên dài | Không phân giải hostname hoặc không tìm thấy container | Dùng đúng tên service dài hoặc thêm network aliases có chủ đích |
| DNS trả IP ví dụ 10.10.10.x; Docker network không khai báo subnet tương ứng | Phân giải đúng nhưng truy cập IP có thể thất bại | Tách test bản ghi DNS với test kết nối service qua Docker DNS |
| Thêm scrape target Web nhưng Web chưa có metrics | Target DOWN hoặc lỗi parse | Triển khai exporter/metrics thật như E07 |
| Keycloak proxy `/auth/` nhưng backend mặc định ở `/` | Có thể lỗi redirect, tài nguyên giao diện hoặc endpoint | Thống nhất path/hostname và proxy; xem [Keycloak reverse proxy](https://www.keycloak.org/server/reverseproxy) |
| Backend mặc định realm `master`, audience `myapp`; mở rộng dùng realm MSSV, client `flask-app` | Có token nhưng `/secure` vẫn 401 | Cập nhật cấu hình OIDC và Audience mapper tương ứng; kiểm tra issuer/JWKS |
| Mẫu Compose thiếu restart ở nhiều service và thiếu volume dữ liệu ở DB/Grafana | Không phủ yêu cầu chung; cấu hình/dữ liệu có thể mất khi recreate | Bổ sung restart cho tất cả và volume đúng chỗ; export/provision cấu hình |
| `depends_on` trong mẫu chỉ nêu thứ tự | Container đã chạy nhưng dịch vụ chưa sẵn sàng | Chờ readiness thực tế, thêm healthcheck/retry phù hợp |
| Hướng dẫn nói bash/cmd/PowerShell nhưng dùng `mkdir -p`, heredoc, `ping -c` | Lệnh không chạy nguyên bản trên PowerShell | Chọn WSL Bash cho lệnh Linux hoặc viết PowerShell tương ứng; dùng `curl.exe` khi test HTTP |
| Trang 11 dừng/xóa tất cả container trên máy | Có thể ảnh hưởng project khác | Chỉ quản lý project bằng `docker compose down`; giữ volume dữ liệu |
| `latest` được dùng trong mẫu | Máy local và EC2 có thể nhận image khác phiên bản | Ghim phiên bản đã kiểm thử trong bản nộp |

Với thiết kế giữ Web gốc + thêm 2 Web cho load balancing + 1 Nginx exporter: có thể là **13 container chạy thường trực**. Nếu tái sử dụng Web gốc thành một trong hai backend thì có thể là **12**. Số này là hệ quả của thiết kế đề xuất, không phải yêu cầu bắt buộc mới.

## 8. Kế hoạch 2 ngày — ưu tiên phần bắt buộc

Giả định **1 người, khoảng 10 giờ làm tập trung mỗi ngày**, tổng 20 giờ chưa tính nghỉ; đã có kiến thức Docker cơ bản và có quyền dùng AWS. Đây là ước lượng để phủ đủ việc, cần dùng quỹ dự phòng khi gặp lỗi. Ngày 1/ngày 2 là hai buổi làm việc của bạn, không tự suy ra hạn nộp từ ngày hiện tại.

### Ngày 1 — dựng nền, xác minh AWS sớm, giữ phần cơ bản

| Khung thời gian tương đối | Task | Output phải có khi kết thúc |
|---|---|---|
| Giờ 0–0,5 | T00: Docker/Compose, Docker Hub, kiểm tra khả năng dùng AWS/SSH; chốt MSSV, tên image và cổng | Không còn phụ thuộc tài khoản chưa rõ |
| Giờ 0,5–2 | T01 + B01/B02/B03: Compose, Web, App, SQL, volume | Web/API/DB chạy; ảnh/log test đầu tiên |
| Giờ 2–4 | B04/B05/B06: Keycloak, MinIO, DNS | Login, upload/download và dig đạt |
| Giờ 4–5,5 | B07/B08: Node Exporter, Prometheus, Grafana | Target UP, dashboard cơ bản có dữ liệu |
| Giờ 5,5–7,5 | B09/B10: proxy, `/auth/`, ping toàn mạng, volume/restart, ghi lại full test | Bộ test cơ bản local có minh chứng |
| Giờ 7,5–10 | T04 + T05 vòng 1: push Web image, dựng stack trên EC2, kiểm tra public Web/API; ghi evidence | Docker Hub có image; EC2 có stack chạy và URL public sơ bộ |

**Mốc cuối ngày 1:** phần cơ bản local đã kiểm thử; EC2 ít nhất đã dựng và chạy Web/API công khai; đã push image; biết rõ những test EC2 còn cần chạy lại. Nếu chưa đạt mốc này, dùng thời gian mở rộng ngày 2 để khép phần cơ bản trước.

### Ngày 2 — khép phần bắt buộc rồi mới mở rộng

| Khung thời gian tương đối | Task | Output phải có khi kết thúc |
|---|---|---|
| Giờ 0–2 | Hoàn tất EC2, chạy test đủ các server, bổ sung minh chứng cloud | Phần bắt buộc local/EC2 và Docker Hub đạt |
| Giờ 2–4 | Báo cáo, ảnh/log, video và link phần cơ bản; cập nhật bảng output | Hồ sơ phần bắt buộc đầy đủ |
| Giờ 4–8 | Chỉ sau khi phần bắt buộc hoàn tất: làm các mục mở rộng theo thời gian thực tế, kiểm thử và cập nhật báo cáo/video | Mỗi mục làm được có output, commit và minh chứng riêng |
| Giờ 8–10 | Dự phòng lỗi, kiểm tra lại link/file, đóng gói và chuẩn bị nộp | Bộ nộp hoàn chỉnh, không còn thiếu minh chứng chính |

### Quy tắc ưu tiên khi chậm tiến độ

1. Khép **phần cơ bản + AWS + Docker Hub + báo cáo/minh chứng** trước; không bỏ AWS chỉ vì local đã chạy.
2. Mở rộng ít phụ thuộc, dễ chốt: E02 → E09 → E03 → E06 → E05 → E01. E08 thuận lợi sau khi monitoring cơ bản hoạt động.
3. E04, E07, E10 cần khung thời gian riêng vì dễ phát sinh lỗi cấu hình. Chỉ bắt đầu khi phần bắt buộc đã hoàn tất; không hy sinh hồ sơ nộp để chạy theo số lượng mở rộng.
4. Nếu phải giảm phạm vi, bỏ tính năng ngoài đề, giao diện cầu kỳ, CRUD tùy chọn hoặc API DB tùy chọn trước. Mục mở rộng chưa làm phải ghi đúng là chưa hoàn thành.
5. Mốc dừng thêm tính năng: cuối giờ 8 ngày 2, hoặc sớm hơn nếu thiếu minh chứng. Dành 2 giờ cuối cho bộ nộp và bản chạy EC2 ổn định. Với thứ tự mới, số mục mở rộng hoàn thành tùy vào tiến độ thực tế, không mặc định đủ cả 10.

## 9. Báo cáo và minh chứng

### Cấu trúc báo cáo bắt buộc ở trang 3

| Phần | Nội dung cần viết | Tài liệu nên đưa vào |
|---|---|---|
| Chương 1. Giới thiệu & mục tiêu | Mô hình cloud thu nhỏ; vai trò 9 nhóm server; mục tiêu bài | Bảng vai trò, phạm vi local/EC2 |
| Chương 2. Kiến trúc & sơ đồ | Network, cổng, luồng request và quan hệ giữa service | Sơ đồ thực tế; thêm exporter và 2 Web nếu có |
| Chương 3. Cấu hình & Dockerfile | Dockerfile, Compose và config từng service | Đoạn config quan trọng, giải thích port/volume/restart |
| Chương 4. Demo & kiểm thử | Ảnh từng server, lệnh test, expected/actual; local và EC2; các mục mở rộng | Bảng kiểm thử và ảnh/log có tên rõ ràng |
| Chương 5. Đánh giá & phân tích | Ưu điểm, khó khăn, hạn chế, hướng mở rộng | Nêu các lỗi đã giải quyết và giới hạn metrics/logging |
| Phụ lục | Link Docker Hub, video demo, log kết quả | Image tag, URL demo, source/README nếu có |

Mỗi task nên ghi: **mục tiêu → file đã cấu hình → cách kiểm thử → kết quả thực tế → ảnh/log**. Tách rõ bản local và bản EC2; không dùng ảnh ví dụ trong PDF làm ảnh kết quả của mình.

### Cấu trúc lưu sản phẩm đề xuất

```text
MyMiniCloud/
  docker-compose.yml
  .env.example
  README.md
  web-frontend-server/
  application-backend-server/
  relational-database-server/init/
  authentication-identity-server/
  object-storage-server/
  internal-dns-server/
  monitoring-prometheus-server/
  monitoring-grafana-dashboard-server/
  api-gateway-proxy-server/
  evidence/
    local/
    ec2/
    extensions/
    logs/
  report/
    BaoCao.docx
    BaoCao.pdf
    links.md
```

Đây là cấu trúc đề xuất; không cần copy dữ liệu volume, mật khẩu thật hay token vào gói source. Nội dung ảnh, SQL seed, JSON, realm export và dashboard export cần giữ để tái tạo demo.

### Kịch bản video đề xuất

1. Giới thiệu sơ đồ và `docker compose ps`.
2. Web/Home/Blog và API trực tiếp/qua proxy.
3. Query DB, đăng nhập Auth, bucket MinIO và DNS.
4. Prometheus Targets và Grafana có dữ liệu.
5. API student, studentdb, token `/secure`, avatar URL, các DNS record mở rộng.
6. Web metrics, dashboard cá nhân, route `/student/` và Round Robin.
7. Chuyển sang public IP EC2, chứng minh stack đang chạy trên EC2; mở link Docker Hub.

PDF không quy định thời lượng video; quay ngắn, rõ từng output là đủ để người xem đối chiếu.

## 10. Checklist hoàn tất

### Nền tảng và cơ bản

- [ ] Tài khoản/quyền EC2 và Docker Hub sử dụng được.
- [ ] Compose hợp lệ; các container dùng `cloud-net`, có tên riêng và restart policy.
- [ ] Có volume dữ liệu cần thiết; cấu hình có thể dựng lại.
- [ ] B01: Home và Blog HTTP 200.
- [ ] B02: `/hello` trực tiếp/qua proxy trả JSON đúng.
- [ ] B03: `minicloud.notes` có dữ liệu.
- [ ] B04: Keycloak admin login và user `sv01`.
- [ ] B05: MinIO bucket demo, upload và tải file.
- [ ] B06: DNS Web trả `10.10.10.10`.
- [ ] B07: Node Exporter target UP, query metric có dữ liệu.
- [ ] B08: Grafana datasource hoạt động, dashboard CPU/RAM/Network có dữ liệu.
- [ ] B09: proxy Web/App/Auth hoạt động, lưu status/redirect.
- [ ] B10: log kiểm tra thông mạng các service.
- [ ] Ít nhất một image tùy chỉnh được push Docker Hub, có link/tag.
- [ ] Toàn stack chạy trên EC2 Ubuntu, public Web/API truy cập được.
- [ ] Có bộ kiểm thử/minh chứng riêng của EC2.

### Mở rộng

- [ ] E01: 3 bài blog, mỗi bài có ảnh và link quay lại.
- [ ] E02: `/student`, file JSON đúng 5 sinh viên/4 trường.
- [ ] E03: `studentdb.students`, đúng schema, ít nhất 3 dòng.
- [ ] E04: realm MSSV, sv01/sv02, flask-app public, token và `/secure` thành công.
- [ ] E05: avatar public URL, documents chứa PDF báo cáo cuối.
- [ ] E06: bản ghi App/MinIO/Keycloak và kết quả `dig`.
- [ ] E07: target web UP, có metrics Web thật.
- [ ] E08: dashboard System Health of MSSV, ít nhất 3 panel có dữ liệu.
- [ ] E09: `/student/` qua proxy trả JSON.
- [ ] E10: hai Web backend, log Round Robin luân phiên.

### Hồ sơ nộp

- [ ] Báo cáo đủ 5 chương và phụ lục.
- [ ] Báo cáo ghi đúng số mục mở rộng hoàn thành.
- [ ] Ảnh/log đủ từng task, đọc được và khớp cấu hình cuối.
- [ ] Link video và Docker Hub mở được.
- [ ] Source/config và README có hướng dẫn dựng local/EC2.
- [ ] PDF báo cáo cuối được upload vào bucket documents.
- [ ] Kiểm tra bộ nộp theo kênh/định dạng giảng viên yêu cầu ngoài PDF, nếu có.

## 11. Nguồn đối chiếu kỹ thuật ngoài PDF

Các nguồn dưới đây chỉ hỗ trợ cách sửa cấu hình dễ lỗi; không bổ sung yêu cầu chấm điểm mới.

- [Docker Compose Networking](https://docs.docker.com/compose/how-tos/networking/): service name, cổng nội bộ và cổng host.
- [NGINX Prometheus Exporter](https://github.com/nginx/nginx-prometheus-exporter): xuất metrics Nginx và scrape endpoint.
- [Prometheus Node Exporter](https://github.com/prometheus/node_exporter#docker): phạm vi host metrics khi chạy trong container.
- [Keycloak Reverse Proxy](https://www.keycloak.org/server/reverseproxy): context path, hostname và proxy.
- [Keycloak Hostname](https://www.keycloak.org/server/hostname): URL public và backchannel.
- [Keycloak Admin Guide](https://www.keycloak.org/docs/latest/server_admin/index.html): public client, grant và audience mapper.
