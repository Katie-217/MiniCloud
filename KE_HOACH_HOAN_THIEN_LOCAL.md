# Kế hoạch hoàn thiện local trước khi thuê EC2

Cập nhật: **27/10/2026**. Nguồn tiêu chí: `Báo Cáo Cuối Kỳ.docx.pdf`, đối chiếu trang và chi tiết tại `KE_HOACH_MINICLOUD_2_NGAY.md`. Trạng thái kiểm thử nằm trong `TIEN_DO_OUTPUT.md`.

## 1. Đích bàn giao và thứ tự

1. Giữ phần bắt buộc local đã kiểm thử, sửa mọi lỗi hồi quy trước.
2. Hoàn tất **10/10 mở rộng**, có kiểm thử và minh chứng từng mục.
3. Hoàn thiện Web demo, image Docker Hub, bộ dựng lại, báo cáo và video local.
4. Người dùng kiểm tra bản cuối, xem bảng đã đạt/cần fix/chưa làm và xác nhận local đạt.
5. Sau xác nhận đó mới triển khai AWS EC2 Ubuntu; kiểm thử public IP và bổ sung hồ sơ cloud.

Hiện có **14/18 nhóm bắt buộc đạt**, **0/10 mở rộng** theo bảng theo dõi. Các kết quả này thuộc bản local cũ, phải kiểm thử lại sau thay đổi. R14 chưa đạt; R16–R18 còn thiếu phần cloud. Hoàn tất local không đồng nghĩa hoàn tất toàn bộ đề.

## 2. Chọn ứng dụng demo từ phần đã có

**Phương án dùng lại:** giữ cổng Web/API/SQL của MiniCloud để chứng minh các yêu cầu đề; ghép Flutter Web E-learning làm ứng dụng demo tại `/elearning/`. Bản main E-learning đã build Web thành công; tiếp theo phải kiểm tra môi trường dữ liệu riêng trước khi chạy UI. Dùng dữ liệu E02/E03 cho trang sinh viên của MiniCloud, giữ Flask và bổ sung 3 bài blog. Người dùng không cần tự viết ứng dụng mới.

Các repo đã kiểm tra chỉ đọc, chưa nhập source vào MiniCloud và chưa chạy ứng dụng với database thật:

| Repo / branch | Quan sát thực tế | Kết luận sử dụng |
|---|---|---|
| Coffee Shop / `main` @ `328341f` | React; backend Express chỉ trả Hello; chưa có MongoDB trong bản này | Không dùng main làm bản ứng dụng đầy đủ |
| Coffee Shop / `feat/Customer-update` @ `1f84c7c` | Có Mongoose, API auth/product/order, seed và Dockerfile; ahead main 40 commit | Có thể tái sử dụng nếu chọn Coffee Shop; chưa build/run. Sửa URL localhost, routing, seed và log URI trước |
| E-learning / `main` @ `9e9ebd5` | Flutter + Firebase Auth/Firestore/Storage; README xác nhận bỏ backend Node cũ; `flutter pub get` và `flutter build web --release --no-pub` đều thành công trên Flutter 3.35.7 / Dart 3.9.2 | Có thể dùng artifact Web. Chưa chạy login/course/data; cảnh báo Wasm dry-run không làm thất bại bản JavaScript Web |
| E-learning / `management_system` @ `9eccf47` | Ahead main 12 commit, có commit sửa deployment; đã đọc source và đối chiếu lịch sử | Là branch mới hơn để đối chiếu khi nhập; chưa build branch này, không tự coi tốt hơn bản main đã build |

Coffee Shop `completed-admin-panel` và `feat/Customer-update` có lịch sử diverged; không kết luận mọi tính năng ở các branch đã tích hợp chỉ từ tên merge commit. Không cần merge repo nguồn vào main để lấy đúng một source commit cho MiniCloud. Mọi sửa đổi phục vụ bài làm sẽ nằm trong repo MiniCloud, giữ URL/branch/SHA và thông tin tác giả nguồn.

Nhánh `feat/elearning-web-demo`: xuất Flutter Web, Nginx phục vụ tại `/elearning/` với base path đúng. Chạy Firebase bằng bộ emulator riêng với dữ liệu giả là phương án cần kiểm chứng; không tự kết nối Firebase thật hoặc triển khai Functions. Khởi tạo app chỉ trỏ vào emulator, dùng demo project ID; kiểm tra request trình duyệt để bảo đảm không truy cập dữ liệu thật. Emulator không được coi là Keycloak/MariaDB/MinIO của bài. Việc chuyển toàn bộ Firebase sang SQL/Keycloak/MinIO là một phạm vi lớn, chưa nằm trong kế hoạch hai ngày này.

Kiểm tra import bằng cách ghép đường dẫn filesystem ban đầu cho ra 12 đường dẫn nghi vấn, nhưng build Dart thực tế thành công. Không coi kết quả kiểm tra tĩnh đơn giản đó là 12 lỗi compiler; không sửa hàng loạt import khi chưa có lỗi thực tế.

Minh chứng build: [source-audit-elearning.json](evidence/local/source-audit-elearning.json), gồm source SHA, lệnh, toolchain, checksum artifact và các phần chưa kiểm chứng. Artifact đang ở checkout tạm; chưa đóng gói vào image MiniCloud.

Flutter hỗ trợ xuất thư mục `build/web` để đưa lên web server ([hướng dẫn Flutter](https://docs.flutter.dev/deployment/web)). Firebase có bộ emulator cho phát triển và kiểm thử ([tài liệu Firebase](https://firebase.google.com/docs/emulator-suite/connect_and_prototype)); khả năng đáp ứng luồng E-learning hiện tại vẫn phải chạy thử, không được suy ra từ tài liệu.

## 3. Kiến trúc cần giữ đúng đề

- Giữ đủ 9 vai trò: Web, App, SQL database, Auth, Storage, DNS, Prometheus, Grafana và gateway; Node Exporter là thành phần hỗ trợ đã có.
- Flask giữ `/hello`, `/notes`, `/student`, `/secure`; thêm `/students-db` để chứng minh dữ liệu SQL trên giao diện nếu thực hiện.
- MariaDB giữ `minicloud.notes`; thêm đúng `studentdb.students`. Firestore/MongoDB không thay thế schema SQL này.
- Keycloak tạo realm theo MSSV, `sv01`/`sv02`, public client `flask-app`; đăng nhập Firebase/JWT của ứng dụng cũ không thay cho E04.
- MinIO vẫn thực hiện upload/download, avatar công khai và lưu PDF; Firebase Storage/Cloudinary không thay cho E05.
- Giữ network `cloud-net`, restart policy, healthcheck và volume; mọi container bổ sung phải xuất hiện trong sơ đồ và bảng kiểm thử.
- Giữ `/api/hello`, `/api/student`, `/api/secure`, `/student/`, `/auth/`, `/blog/`; trang demo có thể dùng `/demo/` để không chiếm các URL bắt buộc. Ghi rõ host port và internal port.

## 4. Task, output, cách làm và điều kiện đạt

Tên file minh chứng bên dưới là **đầu ra dự kiến**, chưa phải file đã có. Chỉ đánh dấu DAT sau khi đã chạy test và kiểm tra nội dung minh chứng.

| Thứ tự / branch mới | Task và cách làm | Output cần bàn giao | Kiểm thử để tích hợp main |
|---|---|---|---|
| L0 `docs/local-completion-plan` | Chốt phạm vi local trước AWS, đối chiếu repo tái sử dụng, lập bảng E01–E10 | Kế hoạch này, quy ước và tracker cập nhật | Link/file hợp lệ, không ghi các output triển khai mới là đạt |
| L1 `feat/student-api-database` | E02: JSON UTF-8 đúng 5 sinh viên; Flask đọc file đóng gói trong image. E03: SQL tạo `studentdb.students`; áp dụng an toàn trên volume đang có. E09: gateway `/student/` tới `/student` | `students.json`, SQL migration/seed, API và proxy config | Direct `/student`, `/api/student`, `/student/` đều trả 200 và cùng dữ liệu. DESCRIBE đúng schema, SELECT >=3 dòng. Chạy lại hello/notes và xác minh dữ liệu cũ còn |
| L2 `feat/demo-web-content` | E01: 3 bài blog riêng có ảnh và link quay lại; làm giao diện demo sinh viên dùng API L1 và trang thông tin nhóm | `/blog/blog1.html`–`blog3.html`, danh sách bài; trang demo hoạt động qua gateway | HTTP 200, ảnh tải thật, link đúng; UI đọc JSON/API SQL nếu bổ sung; refresh trang không 404. Không dùng dữ liệu giả trong UI thay cho API đang lỗi |
| L3 `feat/identity-extensions` | E04: realm `realm_521H0092`, 2 user, public client `flask-app`, cấu hình issuer/JWKS/audience, export cấu hình dựng lại | Realm/client/users; token endpoint; `/api/secure` thành công | Token hợp lệ trả 200, `Secure resource OK` và username; thiếu/sai/hết hạn/sai audience bị từ chối. Không tắt kiểm tra chữ ký/issuer/audience. Log không chứa token/mật khẩu |
| L4 `feat/storage-dns-extensions` | E05: avatar.jpg trong profile-pics, quyền đọc công khai đúng object; documents chứa PDF. E06: thêm App/MinIO/Keycloak, tăng SOA serial | 2 bucket và objects; URL avatar; zone file và kết quả dig | Avatar tải bằng phiên không đăng nhập, khớp file; PDF tải bằng quyền phù hợp và hash khớp. App trả 10.10.10.20; MinIO/Keycloak trả IP đã khai báo; Web cũ vẫn 10.10.10.10 |
| L5 `feat/observability-extensions` | E07: Web stub_status → Nginx exporter → Web /metrics → Prometheus job web. E08: provision dashboard cá nhân 3 panel | Exporter/config; target web; `System Health of 521H0092`; JSON dashboard | `up{job="web"}=1`, `nginx_up{job="web"}=1`; target đúng `web-frontend-server:80`, metric tăng khi có traffic. CPU/RAM/Network có mẫu thật, đúng đơn vị và rate |
| L6 `feat/round-robin-balancing` | E10: 2 Web có tên web-frontend-server1/2, nội dung hoặc header phân biệt; Nginx upstream round robin, route demo `/lb/` | 2 Web, upstream config, chuỗi request có nhận diện backend | Ít nhất 6 request tuần tự cho thấy luân phiên khi cả hai khỏe. Kiểm tra lại E07 và các route cũ; sơ đồ phản ánh đúng số container |
| L6a `feat/elearning-web-demo` | Pin source E-learning đã build; tạo build Web với base path; cấu hình Firebase emulator trong Docker với dữ liệu giả, persistence/export/import; proxy đường dẫn ứng dụng | Source provenance, image Flutter Web/Nginx, môi trường demo và tài khoản giả | Đăng nhập vai trò giảng viên/sinh viên, mở dashboard, xem/tạo khóa học và đọc lại dữ liệu sau restart. Refresh/assets không lỗi; không request Firebase thật; các route MiniCloud vẫn đạt. Luồng E-learning chưa test phải liệt kê riêng |
| L7 `test/local-release-readiness` | Chạy lại toàn bộ core, E01–E10, UI, network và persistence; sửa công cụ kiểm thử để chọn môi trường | Ma trận expected/actual, log/ảnh mới trong evidence/local; công cụ kiểm thử local/cloud tách đầu ra | Không test bắt buộc lỗi; có đọc/ghi thật, recreate giữ dữ liệu; không xóa volume hoặc tác động container project khác |
| L8 `chore/local-release-images` | Build/tag/push image custom đã đổi; ghi digest, thử pull và dựng lại từ bộ source/config hướng dẫn | Image cuối trên namespace katie217; manifest/digest; hướng dẫn dựng lại | Pull manifest thực tế, chạy image khớp tag/digest. Kiểm tra config không yêu cầu đường dẫn chỉ có trên máy tác giả |
| L9 `docs/final-local-delivery` | Cập nhật sơ đồ, báo cáo 5 chương, ảnh/log, video, README và bảng output; upload PDF cuối vào documents | PDF/DOCX/Markdown, video local, link Hub/video, tracker đã đạt/cần fix/chưa làm | Mở được file và link; video phản ánh bản cuối; đủ 10 mở rộng nếu đã đạt thực tế; ghi rõ cloud chưa có. PDF trong MinIO khớp bản cuối bàn giao |
| L10 `chore/cloud-deployment` | Chỉ bắt đầu sau người dùng xác nhận local đạt; hướng dẫn AWS trong chat, deploy và test cùng bản release | R14 và bằng chứng evidence/ec2, phần cloud bổ sung báo cáo/video | Full stack EC2 Ubuntu, Web/API qua public IP, kiểm thử từng server, network/volume/metrics/token đúng môi trường |

**Điều chỉnh theo chỉ dẫn mới nhất:** bảng L ở trên là nhóm công việc tổng quan; branch thực thi tách theo từng chức năng trong bảng sau. Mỗi chức năng bắt đầu từ main đã tích hợp và kiểm thử chức năng trước; code, test, minh chứng và tracker của chức năng được commit ngay trong branch đó.

| Chức năng | Branch thực thi |
|---|---|
| E02 JSON student API | feat/student-json-api |
| E03 student SQL database | feat/student-sql-database |
| E09 student gateway route | feat/student-proxy-route |
| E01 blog cá nhân | feat/personal-blog |
| Giao diện cổng demo | feat/demo-portal |
| E04 Keycloak realm/token | feat/student-identity |
| E05 avatar/documents | feat/profile-object-storage |
| E06 DNS mở rộng | feat/service-dns-records |
| E07 Web metrics | feat/web-metrics |
| E08 dashboard cá nhân | feat/personal-health-dashboard |
| E10 round robin | feat/round-robin-balancing |
| Flutter E-learning demo | feat/elearning-web-demo |
| Regression bản release | test/local-release-readiness |
| Image bản release | chore/local-release-images |
| Báo cáo bản cuối | docs/final-local-report |
| Video bản cuối | docs/final-local-video |
| Tổng hợp đầu ra | docs/final-output-summary |

## 5. Checklist chi tiết cho 10 mở rộng

| ID / trang PDF | Kết quả bắt buộc cần xác minh | Minh chứng dự kiến |
|---|---|---|
| E01 / 21 | Đúng 3 file blog, mỗi bài có ảnh, link quay lại và danh sách hyperlink | E01-blog.json; ảnh trang danh sách và 3 bài |
| E02 / 22 | File students.json đúng 5 bản ghi id/name/major/gpa; Flask /student; proxy /api/student | E02-student-api.json |
| E03 / 23 | studentdb.students: id INT auto primary; student_id VARCHAR(10); fullname VARCHAR(100); dob DATE; major VARCHAR(50); >=3 dòng | E03-student-database.json gồm schema và query |
| E04 / 23–24 | Realm MSSV, sv01/sv02, public client flask-app, token và secure resource đúng username | E04-keycloak.json đã che bí mật; ảnh realm/users/client; export cấu hình |
| E05 / 24 | profile-pics/avatar.jpg đọc công khai; documents chứa PDF báo cáo cuối | E05-storage.json; ảnh bucket/object; URL avatar; hash PDF |
| E06 / 25 | app-backend.cloud.local = 10.10.10.20; thêm minio/keycloak; giữ bản ghi Web | E06-dns.json; zone file |
| E07 / 25 | Job web đúng target web-frontend-server:80, UP, metrics thật | E07-web-metrics.json; Targets screenshot |
| E08 / 25–26 | System Health of 521H0092, CPU%, Memory, Network có dữ liệu; export/lưu dashboard | E08-system-health.json và PNG; dashboard JSON |
| E09 / 26 | /student/ qua Nginx trả đúng JSON /student của Flask | E09-student-proxy.json |
| E10 / 26–27 | 2 Web, round robin, kết quả luân phiên có nhận diện backend | E10-round-robin.json; upstream config; container listing |

IP DNS 10.10.10.x là bản ghi ví dụ của đề, chưa chứng minh IP container thật. Nếu không cấu hình subnet/static IP tương ứng thì chỉ kết luận test DNS đạt, kiểm tra kết nối dùng tên service Docker riêng. Không trình bày kết quả dig như bằng chứng truy cập ứng dụng qua IP đó.

## 6. Kiểm thử bản local cuối và chuẩn bị EC2 khi chưa thuê server

- Chạy bộ kiểm thử core hiện có; bổ sung test hành vi E01–E10, không chỉ kiểm tra container Running.
- Test UI: Home/Blog, dữ liệu sinh viên, Auth, MinIO, Prometheus, Grafana và round robin. Thu log lỗi trình duyệt và request thất bại liên quan luồng demo.
- Test persistence với dữ liệu đánh dấu riêng cho DB, Keycloak, MinIO, Prometheus, Grafana. Recreate từng service, không dùng down -v hoặc xóa dữ liệu để đạt test.
- Dựng lại bản release trong môi trường Docker cô lập: tránh trùng container_name, host port và cloud-net của stack đang chạy; ghi đúng giới hạn nếu chưa có máy sạch để kiểm chứng.
- Chuẩn bị biến PUBLIC_ORIGIN, issuer/JWKS, đường dẫn Linux, mount, healthcheck và cấu hình port. Sửa các check DNS dùng host.docker.internal và check issuer hardcode localhost trước khi dùng ở Linux.
- Công cụ nhận môi trường/địa chỉ đích và ghi evidence/local hoặc evidence/ec2 tách biệt; không ghi đè bằng chứng local khi chạy cloud sau này.
- Node Exporter trên Docker Desktop đo CPU/RAM Linux VM và network theo namespace hiện tại; ghi rõ giới hạn. Không gọi đó là số liệu Windows hay toàn bộ container.
- Lưu cấu hình mẫu không có bí mật, hướng dẫn sinh .env trên máy đích; ghim version/tag đã kiểm thử. Chưa chạy lệnh tạo/kết nối AWS ở bước chuẩn bị này.

## 7. Tiến độ dự kiến cho phần còn lại

Đây là **ước lượng phần việc còn lại từ bản nền đã có**, không phải bắt đầu lại hai ngày mới và không phải cam kết giờ hoàn tất. Không tính thời gian chờ người dùng hoặc triển khai EC2.

| Khối | Thời gian dự kiến | Kết quả |
|---|---|---|
| L1–L2 | 3–4 giờ | Student API/SQL/proxy, Web demo, blog |
| L3–L4 | 2–3 giờ | Token hợp lệ, storage, DNS |
| L5–L6 | 2–3 giờ | Metrics Web, dashboard, round robin |
| L7–L8 | 2–3 giờ | Regression, dựng lại, image release |
| L9 | 2–3 giờ | Báo cáo/video/tracker bản local cuối |
| Dự phòng sửa lỗi | 1–2 giờ | Khép lỗi ảnh hưởng output |

Tổng dự kiến **12–18 giờ làm tập trung** cho phần MiniCloud. L6a cần dự phòng thêm khoảng **3–5 giờ để thử tích hợp**, có thể tăng nếu emulator không đáp ứng code hiện tại; đây chưa phải ước lượng chắc chắn. Không hứa hoàn tất toàn bộ tính năng của đồ án E-learning trong thời gian này. Nếu L6a vượt thời gian dự phòng, báo rõ lỗi và đề xuất dùng cổng demo MiniCloud hiện có; không tự cắt 10 mở rộng để đưa thêm tính năng ngoài đề.

## 8. Gói người dùng kiểm tra trước AWS

- README chỉ rõ lệnh setup/run/test và các URL demo; bảng service/port khớp cấu hình cuối.
- Từng output local có trạng thái, branch/commit, lệnh kiểm thử và minh chứng trong TIEN_DO_OUTPUT.md.
- Không còn lỗi khiến output local bắt buộc hoặc mục mở rộng đã công bố đạt bị trượt; các giới hạn được ghi rõ.
- Báo cáo đủ 5 chương + phụ lục, thống kê đúng số mở rộng; video xem được và link truy cập phù hợp cách nộp bài.
- Docker Hub có image cuối đã kiểm chứng; source/config đủ dựng lại; secrets và volume không ở Git.
- Liệt kê riêng: phần AWS chưa làm, hồ sơ cloud cần bổ sung, MSSV Diệp Yến Nhi còn thiếu và avatar thật nếu chưa được cung cấp. Không đánh dấu hồ sơ nhóm đầy đủ khi còn thiếu thông tin.
- Người dùng kiểm tra và xác nhận local đạt, sau đó mới thuê EC2 và bắt đầu L10. Hai người sử dụng SSH key riêng; không chia sẻ private key trong Git/chat.

## 9. Quy ước theo dõi và commit

Trạng thái: CHUA_LAM → DANG_LAM → CHO_KIEM_THU → DAT; lỗi quan sát được ghi CAN_FIX. Viết code/cấu hình hoặc lập kế hoạch không được tính là output đạt. Tracker luôn phân biệt kết quả của bản nền với bản release đã tích hợp.

Commit tiếng Anh, 4–5 từ sau tiền tố, ví dụ `feat: expose student JSON endpoint`, `feat: seed required student database`, `test: verify complete local release`, `docs: refresh final local evidence`. Review diff → kiểm thử liên quan → cập nhật tracker → commit file liên quan; không đưa log công cụ ngoài project hoặc dữ liệu thật vào commit.
