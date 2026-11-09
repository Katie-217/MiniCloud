# MyMiniCloud — Hướng dẫn partner thiết lập, chạy và kiểm tra local

Cập nhật: **09/11/2026**. Dành cho **Windows x64, Docker Desktop Linux containers**, thao tác bằng CMD hoặc PowerShell. Bản release hiện tại: `local-20261029.1`, **17 container / 9 vai trò server / 8 named volume**.

Mục tiêu: người mới nhận repo có thể tự chạy trên máy mình, biết vì sao phải làm từng bước và nhận biết khi nào môi trường đã sẵn sàng.

**Chọn đúng trường hợp:**

| Trường hợp | Cách đọc |
|---|---|
| Partner chưa có môi trường/source | Làm lần lượt bước 1–8, sau đó kiểm tra giao diện ở phần 9 |
| Đã setup và có dữ liệu demo | Dùng phần 10 để mở lại; không cần cài lại hoặc chạy full suite mỗi lần |
| Terminal hiện `(.venv)` | Python environment đã được kích hoạt; xem bước 5, tiếp tục bằng interpreter trong `.venv` |
| Chỉ cần chụp báo cáo | Mở lại hệ thống, kiểm tra phần 9 và lưu ảnh theo phần 11 |

Hướng dẫn này cho **mỗi người chạy một bản local trên máy riêng**. `localhost` luôn chỉ máy đang mở trình duyệt. Gửi link `http://localhost/` cho partner không làm partner truy cập được máy của Kim. E-learning hiện dùng emulator với cổng loopback và địa chỉ local; việc truy cập chung từ máy khác cần cấu hình riêng, chưa nằm trong hướng dẫn này.

## 1. Hiểu các thành phần trước khi chạy

| Thành phần | Là gì / vì sao cần |
|---|---|
| CMD / PowerShell | Nơi gõ lệnh trên Windows. Hai loại terminal có một số cú pháp khác nhau |
| Python `.venv` | Môi trường thư viện riêng để chạy script khởi động, kiểm thử, chụp ảnh và tạo báo cáo |
| Docker Desktop / Linux engine | Chạy các container Linux của hệ thống |
| Docker Compose | Đọc cấu hình service, network, port, volume và điều phối cả stack |
| Image | Gói phần mềm dùng để tạo container. Release ghim SHA256 để lấy đúng nội dung đã chọn |
| Container | Tiến trình dịch vụ đang chạy, ví dụ MariaDB hoặc Keycloak |
| Named volume | Lưu dữ liệu ngoài vòng đời container; giữ dữ liệu khi tạo lại container |
| `.env` | Cấu hình của riêng máy chạy, gồm thông tin đăng nhập; không nằm trong Git |

`(.venv)` chỉ thể hiện Python environment đang được kích hoạt trong terminal. Windows vẫn hoạt động bình thường; Web, database và các server của dự án chạy trong Docker.

Luồng ví dụ khi xem sinh viên SQL:

```text
Trình duyệt → localhost:80 → Nginx Gateway → Flask API → MariaDB
                                                     ↓
Trình duyệt ← dữ liệu JSON ←──────────────────────────┘
```

## 2. Chuẩn bị phần mềm — chỉ cần làm lần đầu

**Thao tác:** kiểm tra đã có những công cụ dưới đây. Nếu chưa có, dùng trang cài đặt chính thức được dẫn trong bảng.

| Công cụ | Mục đích | Nguồn cài đặt |
|---|---|---|
| Git for Windows | Lấy source và cập nhật đúng commit | [Git for Windows](https://git-scm.com/install/windows) |
| Python | Chạy script quản lý và kiểm thử | [Python cho Windows](https://www.python.org/downloads/windows/) |
| Docker Desktop | Chạy Linux containers, kèm Docker Compose | [Cài Docker Desktop trên Windows](https://docs.docker.com/desktop/setup/install/windows-install/) |
| VS Code, nếu dùng | Xem source, mở terminal, đọc `.env` | Có thể dùng editor khác; không bắt buộc để chạy Docker |

Source yêu cầu Python 3.11 trở lên; môi trường hiện đã chạy bằng **Python 3.12.7**. Có thể dùng nhánh Python 3.12 để gần môi trường đã kiểm tra; chưa xác nhận riêng mọi phiên bản Python mới hơn. Khi cài, cần để terminal nhận lệnh `python` hoặc Python launcher `py`.

Với Docker Desktop, dùng Linux containers. Nếu trình cài yêu cầu WSL 2, bật virtualization hoặc khởi động lại Windows, làm theo hướng dẫn chính thức ở bảng trên rồi mở Docker Desktop lại.

**Vì sao:** cần đủ công cụ trước khi chạy script; cài Docker CLI mà engine chưa hoạt động sẽ chưa chạy được container. Không cần cài riêng MariaDB, Keycloak, MinIO, Flutter, Node.js hoặc Java trên Windows để chạy bản release này; các dịch vụ đã đóng gói trong image.

**Kiểm tra:** mở một terminal mới sau khi cài đặt:

```text
git --version
python --version
docker --version
docker compose version
```

**Kết quả mong đợi:** mỗi lệnh trả phiên bản, không báo `not recognized`. `docker --version` mới xác nhận CLI đã có; trạng thái engine sẽ được kiểm tra ở bước 4.

## 3. Lấy source và mở đúng thư mục

### 3.1. Nếu partner chưa có repo

Ví dụ dùng đường dẫn ngắn `D:\MiniCloud`. Nếu không có ổ D, thay bằng một thư mục phù hợp, ví dụ `C:\MiniCloud`, ở tất cả lệnh liên quan.

```text
git clone https://github.com/Katie-217/MiniCloud.git "D:\MiniCloud"
```

Sau đó chuyển vào thư mục vừa clone:

**CMD:**

```cmd
cd /d "D:\MiniCloud"
```

**PowerShell:**

```powershell
Set-Location -LiteralPath 'D:\MiniCloud'
```

Nếu GitHub từ chối quyền truy cập, đăng nhập tài khoản có quyền vào repo hoặc nhờ chủ repo cấp quyền. Không gửi token hoặc private key trong chat.

### 3.2. Nếu đang dùng máy/thư mục hiện có của Kim

Không clone thêm vào thư mục đã chứa repo. Chuyển vào đúng thư mục hiện tại:

**CMD:**

```cmd
cd /d "D:\Điện toán đám mây"
```

**PowerShell:**

```powershell
Set-Location -LiteralPath 'D:\Điện toán đám mây'
```

Trong VS Code có thể chọn **File → Open Folder**, mở thư mục repo, rồi **Terminal → New Terminal**. Dấu nhắc `D:\...>` thường là CMD; `PS D:\...>` là PowerShell. Không gõ lại phần dấu nhắc này vào lệnh.

**Vì sao:** Compose và các script cần tìm đúng file cấu hình/source. Đường dẫn clone ngắn giúp tránh giới hạn độ dài đường dẫn Windows do một số tên asset dài trong source E-learning.

**Kiểm tra:**

```text
git branch --show-current
git log -1 --oneline
git status --short
```

Để chạy bản bàn giao, dùng `main` đã được Codex tích hợp. Ghi lại commit để hai người biết có đang chạy cùng bản source hay không. Trong thư mục phải có `docker-compose.yml`, `docker-compose.release.yml`, `release-images.json`, `.env.example` và `scripts`.

Nếu repo đã có và cần cập nhật, chỉ khi không có thay đổi dở mới thực hiện:

```text
git switch main
git pull --ff-only
```

Nếu có thay đổi chưa rõ nguồn gốc, giữ chúng lại và gửi `git status --short` cho Codex đối chiếu; không reset/clean để ép cập nhật. Các lần chạy kiểm thử cũng có thể làm thay đổi ảnh/log/tracker.

## 4. Mở Docker Desktop và đợi Linux engine

**Thao tác:** mở Docker Desktop từ Start menu. Đợi trạng thái engine hoạt động rồi chạy:

```text
docker info --format "{{.OSType}} / {{.ServerVersion}}"
docker compose version
```

**Vì sao:** engine là thành phần thực sự chạy container. Image của dự án dùng Linux; `docker info` kiểm tra cả kết nối đến engine, không chỉ việc CLI đã được cài.

**Kết quả mong đợi:** dòng đầu bắt đầu bằng `linux /`. Phiên bản đã kiểm tra trên máy Kim là `linux / 29.0.1`; partner có thể thấy số phiên bản khác.

Nếu báo pipe `dockerDesktopLinuxEngine` không tồn tại, đợi Docker Desktop khởi động xong và thử lại. Nếu đang dùng Windows containers, chuyển Docker Desktop sang Linux containers. Nếu Docker báo WSL/virtualization lỗi, xử lý theo màn hình Docker và tài liệu cài đặt ở bước 2.

## 5. Tạo Python environment và cài thư viện

### 5.1. Tạo `.venv` trên chính máy partner

Chạy ở thư mục gốc repo, chỉ khi chưa có `.venv`:

```text
python -m venv .venv
```

Nếu máy dùng Python launcher và không có lệnh `python`, có thể tạo bằng phiên bản 3.12 đã cài:

```text
py -3.12 -m venv .venv
```

Không cần chạy cả hai lệnh. Không copy `.venv` từ máy Kim; tạo môi trường riêng trên máy partner.

**Vì sao:** `.venv` tách thư viện script của repo khỏi các dự án Python khác và gắn với Python cài trên máy hiện tại.

### 5.2. Cài thư viện và browser kiểm thử

Các lệnh dưới đây dùng được trong **cả CMD và PowerShell**:

```text
.\.venv\Scripts\python.exe -m pip install -r scripts\requirements-dev.txt
.\.venv\Scripts\python.exe -m playwright install chromium
```

**Vì sao:**

- `requests` gọi API và kiểm tra service; `boto3` giao tiếp với MinIO qua S3 API.
- Playwright và Chromium tự động mở giao diện, chụp ảnh, kiểm tra đăng nhập.
- `python-docx` và Markdown phục vụ tạo báo cáo.
- Gọi trực tiếp Python trong `.venv` bảo đảm dùng đúng thư viện, kể cả khi terminal chưa activate.

**Kết quả mong đợi:** cài đặt hoàn tất không có traceback; nếu thư viện đã có, có thể thấy `Requirement already satisfied`. Kiểm tra interpreter bằng:

```text
.\.venv\Scripts\python.exe --version
.\.venv\Scripts\python.exe -m pip --version
```

Lệnh pip phải chỉ đến đường dẫn trong `.venv` của repo đang dùng.

### 5.3. Nếu terminal đang có `(.venv)`

Đây là trạng thái bình thường, không cần tạo lại môi trường. Có thể chạy `python scripts\run_release.py`, nhưng hướng dẫn này vẫn dùng đường dẫn đầy đủ `.\.venv\Scripts\python.exe` để tránh nhầm interpreter.

Activate là tùy chọn:

| Terminal | Lệnh activate |
|---|---|
| CMD | `.\.venv\Scripts\activate.bat` |
| PowerShell | `.\.venv\Scripts\Activate.ps1` |

Nếu PowerShell chặn `Activate.ps1`, tiếp tục bằng đường dẫn Python đầy đủ như trên; không cần đổi execution policy toàn máy. Đóng terminal hoặc dùng `deactivate` để thoát phiên activate; thao tác đó không dừng container Docker.

## 6. Sinh cấu hình `.env` của riêng máy

**Thao tác:**

```text
.\.venv\Scripts\python.exe scripts\setup.py
```

**Vì sao:** `.env.example` chỉ là mẫu với giá trị `CHANGE_ME`. Script tạo `.env` có mật khẩu ngẫu nhiên để các service và bộ kiểm thử dùng thống nhất.

**Kết quả mong đợi:**

```text
Created .env with random local passwords; values were not printed.
```

Hoặc, nếu đã thiết lập trước đó:

```text
Existing .env preserved.
```

Mỗi máy sinh `.env` riêng nên **mật khẩu của partner có thể khác máy Kim**, dù username demo giống nhau. Không cần gửi `.env` của Kim cho partner. Script khởi động cũng tự gọi setup; chạy riêng ở bước này giúp xác nhận cấu hình đã sẵn sàng.

Đọc thông tin đăng nhập bằng editor, ví dụ mở `.env` trong VS Code hoặc:

```text
notepad .env
```

Giữ nguyên `.env` khi đã có dữ liệu. Keycloak, database và Grafana có dữ liệu lưu trong volume; tự đổi mật khẩu trong file không bảo đảm tài khoản đã lưu cũng thay đổi theo. Không xóa `.env` để xử lý lỗi đăng nhập. File này được Git bỏ qua; không đưa mật khẩu, token hoặc ảnh chụp `.env` vào báo cáo.

## 7. Chạy lần đầu và tạo đủ dữ liệu demo

**Thao tác:** Docker engine phải đang chạy; máy có Internet để tải image và thư viện/browser nếu cần. Chạy:

```text
.\.venv\Scripts\python.exe scripts\run_release.py --verify
```

**Vì sao phải có `--verify` ở lần đầu:** Compose khởi động server; các script kiểm tra còn thiết lập các đối tượng demo cần thiết như realm/user/client Keycloak, bucket/object MinIO và tài khoản/khóa học E-learning. Trên máy có volume mới, chỉ mở container chưa bảo đảm có đủ dữ liệu để đi hết các màn demo.

Lệnh này thực hiện:

| Thứ tự | Việc được thực hiện | Lý do |
|---|---|---|
| 1 | Giữ/tạo `.env`, kiểm tra Compose | Phát hiện thiếu cấu hình trước khi chạy |
| 2 | Kết hợp `docker-compose.yml` và `docker-compose.release.yml` | Dùng cùng service/network/volume và image đúng release |
| 3 | Pull image đã ghim digest | Lấy đúng nội dung image, không phụ thuộc tag vừa bị thay đổi |
| 4 | Khởi động stack ở chế độ nền, chờ các healthcheck khai báo | Đợi các service phụ thuộc sẵn sàng |
| 5 | Pull/tag image tools cho bài kiểm tra DNS/network | Có sẵn `dig`, `ping`, `curl` trong container công cụ |
| 6 | Đợi metric CPU có mẫu | Công thức rate cần nhiều hơn một lượt scrape |
| 7 | Chạy 27 bước chức năng/UI, có ảnh | Kiểm tra phần cơ bản, 10 mở rộng, form secure, logging và giao diện |
| 8 | Chạy thêm core persistence, E-learning, Firebase persistence, Loki persistence | Kiểm tra luồng demo và dữ liệu qua recreate |

Release được chuẩn bị cho `linux/amd64`; máy Windows ARM chưa nằm trong môi trường đã kiểm tra. Cấu hình runtime dùng image đã đóng gói, không yêu cầu build Flutter/source trên máy partner.

**Kết quả mong đợi:** không có traceback/assertion thất bại; kết thúc bằng:

```text
Pinned local release ready: http://localhost/ and http://localhost/elearning/
```

Trong quá trình chạy có thể thấy `Pulling`, `Pulled`, `Waiting`, `Healthy` và các dòng `PASS`. Lần tải image đầu sẽ lâu hơn lần mở lại. Bộ 27 bước phải báo thành công, và các bài kiểm tra bổ sung phía sau cũng phải kết thúc thành công; không chỉ nhìn một dòng PASS ở giữa.

**Ảnh hưởng cần biết:** verify có ghi dữ liệu demo/marker, cập nhật các tài khoản lab do script quản lý, tạo lại một số container và cập nhật ảnh/log trong `evidence/local/` cùng `TIEN_DO_OUTPUT.md`. Các bài persistence giữ named volume. Chạy verify trước buổi kiểm tra/chụp ảnh, không đồng thời với người khác đang thao tác cùng stack hoặc Gemini/Codex đang chạy test recreate.

Nếu một bài thất bại: giữ log và tên script lỗi, xem phần 12. Không tự bỏ assertion hoặc đánh dấu output đạt. Việc kết thúc lỗi không đồng nghĩa mọi container đã dừng.

## 8. Xác nhận môi trường chạy xong

### 8.1. Kiểm tra container

```text
docker compose ps
```

**Vì sao:** kiểm tra trạng thái thực tế sau lệnh khởi động. Dự kiến có **17 container thường trực** trong project `myminicloud`; container tools chạy tạm không tính vào 17 này. Các service có healthcheck phải healthy; một số agent/exporter chỉ có trạng thái Running vì không khai báo healthcheck.

Container Web chính và hai replica là **ba container độc lập**. Hai job Prometheus `node`/`web` không phải số lượng container. `restart: unless-stopped` là policy của service/container; 8 named volume lưu dữ liệu.

### 8.2. Kiểm tra API qua gateway

```text
curl.exe http://localhost/api/hello
curl.exe http://localhost/api/student
curl.exe http://localhost/student/
curl.exe http://localhost/api/students-db
curl.exe http://localhost/api/notes
```

**Vì sao:** kiểm tra đường đi từ cổng gateway đến Flask và database, bổ sung cho việc xem trạng thái container. Dùng `curl.exe` để có cùng cách gọi trong CMD/PowerShell.

**Kết quả mong đợi:**

| URL | Kết quả |
|---|---|
| `/api/hello` | JSON có `Hello from App Server!` |
| `/api/student` và `/student/` | Cùng 5 bản ghi id/name/major/gpa từ file JSON |
| `/api/students-db` | Ít nhất 3 bản ghi từ `studentdb.students`; fixture hiện có 3 |
| `/api/notes` | Danh sách ghi chú đọc từ MariaDB |

5 sinh viên JSON và 3 sinh viên SQL là hai bộ dữ liệu riêng theo đề; không cần sửa thành cùng số lượng.

## 9. Đăng nhập và kiểm tra từng giao diện

### 9.1. Bảng địa chỉ và tài khoản

Mở các URL trên **chính máy đang chạy Docker**. Trong bảng, tên viết hoa là **khóa cần đọc giá trị từ `.env`**, không nhập nguyên chữ đó làm mật khẩu.

| Giao diện | URL | Username | Mật khẩu đọc từ khóa |
|---|---|---|---|
| Portal/Blog/sinh viên | http://localhost/ | Không cần | — |
| Form API bảo vệ | http://localhost/#secure-demo | sv01 hoặc sv02 | `KEYCLOAK_TEST_PASSWORD` |
| Keycloak quản trị | http://localhost/auth/admin/master/console/ | Giá trị `KEYCLOAK_ADMIN` | `KEYCLOAK_ADMIN_PASSWORD` |
| MinIO Console | http://localhost:9001/ | Giá trị `MINIO_ROOT_USER` | `MINIO_ROOT_PASSWORD` |
| Prometheus | http://localhost:9090/targets | Không cần | — |
| Grafana | http://localhost:3000/ | Giá trị `GRAFANA_ADMIN_USER` | `GRAFANA_ADMIN_PASSWORD` |
| E-learning giảng viên | http://localhost/elearning/ | instructor@example.test | `ELEARNING_INSTRUCTOR_PASSWORD` |
| E-learning sinh viên | http://localhost/elearning/ | student@example.test | `ELEARNING_STUDENT_PASSWORD` |

Username/password của Keycloak quản trị, form secure và E-learning thuộc những luồng khác nhau; dùng đúng hàng trong bảng. Hai user sv01/sv02 của realm bài làm dùng mật khẩu lab từ `KEYCLOAK_TEST_PASSWORD`.

Muốn xem hai vai trò E-learning cùng lúc trên một máy: dùng một cửa sổ thường và một cửa sổ ẩn danh, hoặc hai browser profile khác nhau. Hai cửa sổ ẩn danh có thể chia sẻ cùng phiên đăng nhập.

### 9.2. Checklist thao tác, lý do và kết quả

| Bước / yêu cầu | Thao tác cụ thể | Vì sao kiểm tra | Kết quả / ảnh tham khảo trong `evidence/local/` |
|---|---|---|---|
| A — R02, E01 | Portal → Blog → mở lần lượt cả 3 bài, thử link quay lại | Xác nhận Web, ảnh và điều hướng | Có danh sách 3 bài, mỗi bài có ảnh; `R02-home.png`, `E01-blog1.png`, `E01-blog2.png`, `E01-blog3.png` |
| B — E02, E09 | Portal → Tải danh sách sinh viên; mở `/api/student` và `/student/` | Xác nhận giao diện lấy dữ liệu API và proxy đúng | 5 bản ghi khớp nhau; `E02-student-api.json`, `E09-student-proxy.json` |
| C — R03/R04, E03 | Mở các API bước 8.2; xem schema trong `E03-result.png` | Xác nhận Flask kết nối MariaDB và đúng schema | Hello/notes thành công; SQL đủ id/student_id/fullname/dob/major; `E03-student-database.json` |
| D — R05, E04 | Đăng nhập Keycloak → chọn realm_521H0092 → Users; Clients → flask-app → Settings | Xác nhận realm, người dùng và public client theo đề | Có sv01/sv02, Client authentication Off; `E04-realm-users.png`, `E04-public-client.png`. Master realm còn có user sv01 cho bài cơ bản |
| E — E04 | Portal phần secure → chọn sv01, nhập mật khẩu → Gọi API có bảo vệ; thử sv02; bấm Gọi không có token | Xác nhận token hợp lệ được chấp nhận và thiếu token bị từ chối | 200 đúng username; không token trả **401 là đúng**; `portal-secure-success.png`, `portal-secure-missing-token.png` |
| F — R06, E05 | Đăng nhập MinIO → Buckets; mở http://localhost:9000/profile-pics/avatar.jpg | Xác nhận object storage và quyền truy cập | Có demo/profile-pics/documents; avatar chữ K công khai; documents có PDF. Tải PDF qua Console khi đã đăng nhập; ẩn danh **403 là đúng**. `E05-storage.json`, `E05-minio-buckets.png`, `E05-minio-avatar.png` |
| G — R07, E06 | Xem `E06-dns.json` hoặc chạy lệnh DNS ở phần 9.3 | Xác nhận Bind9 trả đúng 4 bản ghi lab | Web 10.10.10.10, App 10.10.10.20, MinIO 10.10.10.30, Keycloak 10.10.10.40; không dùng các IP này như Docker IP thật |
| H — R08, E07 | Prometheus → Targets; trang Query thử `nginx_up`, `nginx_http_requests_total` | Xác nhận metric và Web scrape thực tế | Job node/web UP, web target đúng web-frontend-server:80; nginx_up = 1, counter tăng khi truy cập; `E07-web-targets.png`, `E07-web-metrics.png` |
| I — R09, E08 | Đăng nhập Grafana → http://localhost:3000/d/system-health-521h0092 → Last 15 minutes, Refresh 10s | Xác nhận dashboard cá nhân có số liệu | System Health of 521H0092, CPU%, Memory%, Network Traffic. Đợi ≥2 scrape nếu mới chạy; `E08-system-health.png` |
| J — Logging | Grafana → http://localhost:3000/d/minicloud-service-logs → gọi `/api/hello` rồi Refresh | Xác nhận luồng Docker logs → Alloy → Loki → Grafana | Có log HTTP mới, nhãn service MyMiniCloud; stat là **số dòng log**, không phải số lỗi; `logging-grafana.png` |
| K — E10 | Portal thử cân bằng tải nhiều lần hoặc mở `/lb/whoami`; xem header qua curl | Xác nhận hai backend phục vụ request | Body/header X-Backend-Server nhận diện server1/server2. Test 8 request tuần tự xen kẽ, mỗi server 4 lần; truy cập đồng thời khác có thể làm thứ tự quan sát khác. `E10-result.png` |
| L — E-learning instructor | Đăng nhập instructor → Teaching; có thể Create Course với code riêng và semester HK1_2026 | Xác nhận app tái sử dụng đọc/ghi dữ liệu emulator | Cloud Computing Lab/CLOUD101, Students: 1; full verify còn tạo MiniCloud UI Demo Course/DEMOUI29. `elearning-instructor-courses.png`, `elearning-created-course.png` |
| M — E-learning student | Profile/cửa sổ tách biệt → đăng nhập student → Courses → F5 | Xác nhận vai trò sinh viên và phiên đăng nhập | Hello Demo Student, CLOUD101, số sinh viên thật; F5 giữ phiên. `elearning-student-courses.png`, `elearning-demo.json` |
| N — R12/R13/R15 | Xem JSON persistence, `release-images.json`, manifest Hub | Xác nhận lưu dữ liệu và bản image đang bàn giao | Core5/Firebase/Loki có minh chứng recreate; 6 custom image, 17 runtime image ghim digest. Xem ngày/commit của từng file trước khi dùng làm minh chứng mới |

Portal đầy đủ dùng **gateway cổng 80**. Cổng Web 8080 phục vụ kiểm tra nội dung tĩnh; dùng cổng 80 cho form API và các route tích hợp.

### 9.3. Kiểm tra bổ sung khi cần

Sau bước 7, image tools đã được chuẩn bị. Có thể chạy:

```text
.\.venv\Scripts\python.exe scripts\check_service_dns.py
.\.venv\Scripts\python.exe scripts\check_network.py
curl.exe -i http://localhost/lb/whoami
```

Các script DNS/network ghi lại JSON và cập nhật tracker; không phải chỉ xem màn hình. Không cần chạy lại full suite nếu chỉ muốn chụp giao diện. Những bài có `--recreate` sẽ tạo lại container thuộc project; chỉ dùng khi cần kiểm tra vòng đời dữ liệu/backend.

## 10. Cách dùng hằng ngày: mở lại, dừng, cập nhật

### 10.1. Mở lại sau khi setup lần đầu đã đạt

1. Mở Docker Desktop, đợi Linux engine.
2. Mở terminal và vào thư mục repo như bước 3.
3. Chạy:

```text
.\.venv\Scripts\python.exe scripts\run_release.py
```

4. Đợi dòng `Pinned local release ready`, mở http://localhost/.

**Vì sao:** dùng lại `.venv`, `.env`, image và dữ liệu volume hiện có. Không cần cài lại thư viện hoặc khởi tạo demo mỗi lần. Runner vẫn kiểm tra/pull image đã ghim nên cần kết nối registry.

### 10.2. Dừng khi dùng xong

```text
docker compose stop
```

**Vì sao:** dừng container của project để giải phóng tài nguyên chạy, giữ container và volume dữ liệu. Đóng terminal không tự dừng container vì stack chạy nền.

Không dùng `docker compose down -v` để sửa lỗi thông thường: `-v` xóa named volume và có thể làm mất dữ liệu demo/người dùng đã nhập. Không prune hoặc dừng container ngoài project.

### 10.3. Khi nhóm có source mới

Kiểm tra `git status --short`, giữ thay đổi dở nếu có. Khi working tree sạch mới dùng:

```text
git switch main
git pull --ff-only
.\.venv\Scripts\python.exe scripts\run_release.py
```

**Vì sao:** source và các file cấu hình mount cần khớp bản nhóm đang bàn giao. Nếu requirements thay đổi thì cài lại bằng lệnh pip ở bước 5. Nếu có thay đổi runtime, dùng bản release/digest mới do nhóm phát hành; không tự sửa code trong container để thay cho quy trình branch/build/test.

## 11. Chụp ảnh và gửi kết quả cho nhóm

**Thao tác:** tạo thư mục dành riêng ảnh thủ công. Lệnh dùng được trong CMD/PowerShell:

```text
mkdir evidence\manual
```

Nếu thư mục đã có thì dùng tiếp, không cần tạo lại. Có thể đặt tên ảnh `E04-realm-users-<ten-nguoi-chup>.png`, `E08-health-<ten-nguoi-chup>.png`… và ghi ngày chụp trong phần bàn giao.

**Vì sao:** ảnh test tự động ở `evidence/local/` có thể bị sinh lại khi chạy verify; thư mục thủ công giúp giữ ảnh partner chụp để làm báo cáo.

Trước khi chụp:

- Chờ giao diện và biểu đồ tải xong, chọn khoảng thời gian còn dữ liệu, giữ tiêu đề/đơn vị đo trong ảnh.
- Chụp sau đăng nhập; không đưa `.env`, mật khẩu, token, cookie hoặc URL ký có token vào ảnh.
- Ghi commit source bằng `git log -1 --oneline`, máy thực hiện, ngày kiểm tra, thao tác và kết quả.
- File JSON/ảnh có sẵn trong repo là minh chứng lịch sử; không tự đổi ngày để gọi là kết quả máy partner.

Khi báo lỗi, gửi **lệnh đã chạy, tên script/service, HTTP status/thông báo lỗi, commit và ảnh đã che bí mật**. Không gửi cả `.env` hoặc dump toàn bộ biến môi trường.

## 12. Xử lý các lỗi thường gặp

| Hiện tượng | Lý do thường gặp | Thao tác tiếp theo |
|---|---|---|
| `Set-Location is not recognized` | Đang dùng CMD | Dùng `cd /d "D:\MiniCloud"`, hoặc đổi sang PowerShell |
| `cd /d` lỗi trong PowerShell | Dùng cú pháp CMD trong PowerShell | Dùng `Set-Location -LiteralPath 'D:\MiniCloud'` |
| `python`/`git`/`docker` not recognized | Chưa cài hoặc terminal chưa nhận PATH mới | Cài công cụ tương ứng ở bước 2, mở terminal mới rồi kiểm tra lại |
| `Filename too long` khi lấy source | Đường dẫn checkout quá sâu và một số tên asset E-learning dài | Chọn đường dẫn clone ngắn như bước 3. Giữ log và báo Codex nếu checkout dở; không xóa repo đang có thay đổi để thử lại |
| Không thấy `.venv\Scripts\python.exe` | Chưa tạo `.venv` hoặc đang đứng sai thư mục | Kiểm tra thư mục repo, làm bước 5.1 |
| `No module named requests/boto3/playwright` | Chưa cài thư viện vào đúng interpreter | Chạy lệnh pip ở bước 5.2 bằng `.\.venv\Scripts\python.exe` |
| Chromium missing / executable doesn't exist | Chưa tải browser Playwright | Chạy lại `.\.venv\Scripts\python.exe -m playwright install chromium` |
| PowerShell chặn `Activate.ps1` | Chính sách chạy script của terminal | Dùng trực tiếp Python trong `.venv`, không bắt buộc activate |
| Không kết nối `dockerDesktopLinuxEngine` | Docker Desktop chưa chạy hoặc engine khởi động lỗi | Mở Docker Desktop; kiểm tra `docker info`; xử lý thông báo WSL nếu có |
| Pull bị rate limit/denied/network error | Quyền registry, giới hạn tải hoặc mạng | Kiểm tra mạng/thông báo cụ thể. Nếu registry yêu cầu đăng nhập, dùng Docker Desktop hoặc `docker login` trên máy mình; không gửi token/mật khẩu cho nhóm |
| `port is already allocated` / `address already in use` | Cổng 80/3000/8081/9000… đã có ứng dụng khác dùng | Xem danh sách container/cổng bằng lệnh dưới bảng; báo cổng xung đột. Không dừng project khác hoặc tự đổi port đơn lẻ làm lệch URL/Auth |
| Container unhealthy / timeout | Service chưa sẵn sàng, thiếu tài nguyên hoặc lỗi cấu hình | `docker compose ps`, xem log đúng service; giữ dữ liệu và gửi lỗi. Không xóa volume |
| Keycloak không có realm/user, MinIO không có bucket hoặc E-learning chưa có tài khoản | Mới chạy server, chưa thiết lập demo đầy đủ | Kiểm tra kết quả bước 7; chạy `run_release.py --verify` khi phù hợp và xử lý bài test lỗi đầu tiên |
| Đăng nhập sai dù đọc `.env` | Dùng nhầm loại tài khoản, `.env` khác máy hoặc mật khẩu cũ trong volume | Đối chiếu bảng 9.1; giữ `.env`/volume và nhờ Codex kiểm tra, không tạo ngẫu nhiên mật khẩu mới |
| Secure 401 / PDF 403 | Có thể là trường hợp bảo vệ mong đợi | Không token thì secure 401 đúng; PDF ẩn danh 403 đúng. Đối chiếu bước E/F trước khi kết luận lỗi |
| Grafana No data / Loki tạm thời 503 ngay sau startup | Chưa đủ scrape/readiness hoặc khoảng thời gian không phù hợp | Đợi thêm, chọn Last 15 minutes/Refresh. Nếu kéo dài, kiểm tra Prometheus Targets và log service |
| Mở link localhost từ máy khác không thấy ứng dụng | localhost là máy đang mở trình duyệt | Chạy stack trên máy partner theo hướng dẫn; không chỉ thay IP vì Auth/emulator còn cấu hình local |
| Git báo file thay đổi sau verify | Test ghi evidence/tracker | Giữ kết quả để đối chiếu; không reset/xóa hoặc commit gộp vào chức năng khác |

Lệnh chẩn đoán đọc trạng thái:

```text
docker compose ps
docker compose logs --tail 80 application-backend-server
docker compose logs --tail 80 authentication-identity-server
docker ps --format "table {{.Names}}\t{{.Ports}}"
```

Chọn đúng service liên quan. Đọc log tại máy; kiểm tra và che thông tin nhạy cảm trước khi chuyển log cho người khác. Không dùng `docker compose config` dạng in toàn cấu hình để gửi vì có thể hiện giá trị `.env`; nếu chỉ cần kiểm tra hợp lệ dùng:

```text
docker compose config --quiet
```

## 13. Phạm vi kiểm chứng và hồ sơ còn lại

- Hướng dẫn khớp script hiện tại, được đối chiếu ngày 09/11/2026. Đã mở lại release và kiểm tra nhanh giao diện/API/Auth/dữ liệu/monitoring trên máy Kim; **chưa xác nhận bằng một lượt cài mới hoàn toàn trên máy partner**. Partner cần giữ kết quả bước 7 làm căn cứ nghiệm thu máy mình.
- 17 runtime image ghim digest, 6 custom image gồm công cụ. Nguồn khóa image: [release-images.json](release-images.json), [Compose release](docker-compose.release.yml). Việc chạy release không cần build source.
- CPU/RAM của Node Exporter phản ánh Linux VM Docker Desktop; network theo namespace exporter. Không ghi thành CPU/RAM Windows host hoặc riêng từng container. Một số panel Root FS của Node Exporter Full có thể N/A; dùng dashboard cá nhân 3 panel để kiểm tra yêu cầu bắt buộc.
- Loki chỉ thu project myminicloud; retention 24h, xóa theo chu kỳ compactor. Loki persistence đã có test; Alloy có volume nhưng resume positions chưa có bài kiểm tra riêng.
- E-learning dùng source main `9e9ebd539c7f08092ea6855c9aceafe645bd28e0`, Firebase Auth/Firestore/Storage Emulator `demo-minicloud`, dữ liệu giả. Hai vai trò, đọc/tạo khóa học, số ghi danh/F5 đã có test; Google Sign-In, Cloud Functions, link preview và các luồng gốc khác chưa được xác nhận. Flask/MariaDB/Keycloak/MinIO vẫn đảm nhận yêu cầu riêng của đề.
- G01 đã nghiệm thu; G02 báo cáo cuối, G03 video cuối, G04 tổng hợp và QA cuối còn theo kế hoạch. PDF/video có trong repo chưa tự động được coi là bản báo cáo cuối phản ánh đầy đủ 17 container.
- MSSV Diệp Yến Nhi chờ bổ sung, không chặn chạy local. Avatar chữ K là lựa chọn đã được người dùng duyệt.
- AWS chưa triển khai. R14 và phần cloud của R16–R18 còn chờ người dùng kiểm tra và xác nhận local; không tạo tài nguyên AWS trong quy trình này.

Hồ sơ tham khảo:

- [Trạng thái output](TIEN_DO_OUTPUT.md), [kế hoạch local](KE_HOACH_HOAN_THIEN_LOCAL.md), [bàn giao Gemini](BAN_GIAO_GEMINI.md).
- [Báo cáo PDF hiện có](report/BaoCao_Local_521H0092.pdf), [DOCX](report/BaoCao_Local_521H0092.docx).
- [Video hiện có](report/Demo_Local_521H0092.webm), [trang xem video](report/Demo_Local_521H0092.html).
- [Minh chứng đọc được](evidence/local/evidence.html); xem thời điểm trong từng JSON để biết kết quả thuộc lần chạy nào.

## 14. Checklist partner trước khi bàn giao kết quả

- [ ] Đã lấy đúng repo/commit, ghi lại `git log -1 --oneline`.
- [ ] `docker info` trả Linux engine; Python/pip dùng đúng `.venv` của máy mình.
- [ ] `.env` do máy mình sinh, không commit/chụp mật khẩu.
- [ ] Lần đầu `run_release.py --verify` hoàn tất cả suite và kiểm tra bổ sung.
- [ ] Có 17 container Running, các healthcheck khai báo healthy.
- [ ] Portal và E-learning mở được; API có 5 JSON và ít nhất 3 SQL.
- [ ] Đăng nhập đúng tài khoản; secure có token 200, thiếu token 401.
- [ ] Prometheus node/web UP; Grafana 3 panel có dữ liệu, dashboard log có log mới.
- [ ] Avatar public, PDF riêng tư; RR nhận diện được cả hai backend.
- [ ] Ảnh thủ công/ghi chú lỗi có ngày, commit và kết quả thật; bí mật đã được che.
- [ ] Không thay `.env`, xóa volume hoặc tác động project khác để ép test đạt.
- [ ] Đã gửi lỗi/chỗ chưa kiểm chứng cho Codex; chưa tự đánh dấu hoàn thành cloud.
