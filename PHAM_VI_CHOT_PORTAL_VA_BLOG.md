# Phạm vi chốt: Portal MiniCloud và website Blog riêng

Chốt theo yêu cầu người dùng **09/11/2026**. Tài liệu này ưu tiên hơn các đề xuất cũ gắn danh sách bài viết vào Portal hoặc giữ E-learning trong luồng demo.

**Quyết định:** hai giao diện riêng, cùng hệ thống MiniCloud. **Portal là nơi quan sát/kiểm thử hạ tầng. Blog là ứng dụng Web được triển khai để demo.** E-learning không thuộc phạm vi bài demo chính và không tiếp tục phát triển cho bài này.

Đây là đặc tả đầu ra, chưa phải xác nhận các chức năng mới đã được lập trình/kiểm thử. Giữ nguyên minh chứng lịch sử và dữ liệu hiện có đến khi task triển khai liên quan được nghiệm thu.

## 1. Hai website được tách như thế nào

| Thành phần | Địa chỉ local mục tiêu | Vai trò và trải nghiệm |
|---|---|---|
| Portal MiniCloud | `http://localhost/` | Dashboard/control panel minh chứng dịch vụ: metrics, API, SQL, Auth, Storage, DNS, Logs, Load Balancer; không hiển thị danh sách/nội dung 3 bài Blog bên trong Portal |
| Website Blog | `http://localhost:8080/`, danh sách tại `/blog/` | Có trang chủ, menu, CSS và trang bài viết riêng; độc lập về trải nghiệm với giao diện quản trị Portal |
| Blog qua Gateway | `http://localhost/blog/` và `/blog/blog1.html`… | Giữ các route đề và kiểm thử đang dùng; nội dung vẫn là cùng website Blog, không biến thành một tab quản trị Portal |
| Hai Web replica | `/lb/`, `/lb/whoami` qua Gateway | Phục vụ Web demo và nhận diện backend để kiểm chứng Round Robin |

Portal chỉ có **một card ứng dụng Blog**: tên, URL, thông tin triển khai và nút **Mở website Blog** sang tab mới. Không nhúng iframe hoặc copy toàn bộ Blog vào Portal.

Tách website không bắt buộc thêm repo hoặc container. Phương án ít thay đổi: hai bộ frontend/source riêng trong Web server đã có; gateway dẫn vào Portal, cổng Web trực tiếp phục vụ Blog. Giữ 9 vai trò server, network và dữ liệu của bài.

## 2. Các phần Portal phải thể hiện

| Mục | Chức năng chốt | Nguồn dữ liệu / cách kiểm chứng | Liên hệ yêu cầu |
|---|---|---|---|
| **1. Tổng quan** | Card CPU%, RAM%, network receive B/s, Web requests/s; biểu đồ lịch sử, thời điểm cập nhật, làm mới và trạng thái thiếu/lỗi | Backend đọc Prometheus; số thực, không giá trị random/hardcode. CPU/RAM của Linux VM Docker Desktop, network của namespace exporter | Trình diễn monitoring, hỗ trợ R08/R09/E07/E08; vẫn giữ Grafana theo đề |
| **2. Dịch vụ & kiến trúc** | Card 9 vai trò, service name, chức năng, cổng host/internal, cloud-net và volume; cấu hình chỉ đọc, link đến công cụ liên quan | Metadata ghi rõ “theo cấu hình”; chỉ hiển thị UP/Healthy khi có probe thật, nêu thời điểm/nguồn đo | R01/R11/R12; không suy 17 container khỏe từ 2 target |
| **3. API & Database demo** | Chọn endpoint cố định, gửi request, thấy HTTP status/ms/thời điểm; kết quả dạng card/bảng, JSON mở rộng. Xem 5 sinh viên JSON, ít nhất 3 sinh viên SQL, ghi chú và schema yêu cầu | `/api/hello`, `/api/student`, `/student/`, `/api/students-db`, `/api/notes`. Ghi rõ schema hiển thị lấy từ cấu hình hay truy vấn thực tế; không tự gọi một bản mô tả là kết quả SHOW COLUMNS mới chạy | R03/R04/E02/E03/E09 |
| **4. Xác thực** | Chọn sv01/sv02, đăng nhập Keycloak, gọi secure API; hiển thị username và 200/401; mở Console quản trị khi cần | OIDC/Keycloak thật, `/api/secure`; password masked và xóa sau submit, không in/lưu JWT vào UI/log/localStorage | R05/E04 |
| **5. Lưu trữ** | Card avatar public, thông tin bucket/object/PDF và nút mở MinIO Console để upload/download, kiểm tra quyền | MinIO, `profile-pics/avatar.jpg`, documents/PDF. Avatar 200 ẩn danh, PDF riêng tư 403 ẩn danh là đúng. Form upload trong Portal là cải tiến riêng, không bắt buộc để chấm E05 | R06/E05 |
| **6. Mạng & DNS** | Hiển thị zone, 4 bản ghi, expected/actual và minh chứng dig có thời điểm/môi trường; kết quả network test | Bind9 và kết quả test thực tế. Bản đầu có thể xem minh chứng đã ghi; không gắn nhãn Live nếu chưa chạy probe mới. IP 10.10.10.x là bản ghi lab, khác IP Docker | R07/R11/E06 |
| **7. Monitoring & Logs** | Trạng thái target node/web, liên kết Grafana cá nhân và dashboard logs; thể hiện phạm vi số liệu | Prometheus/Grafana/Loki/Alloy. Link công cụ được ghi đúng là link; không mô tả log đã nhúng khi chỉ mới có nút mở Grafana | R08/R09/E07/E08 và logging |
| **8. Load Balancer** | Nút gửi request tuần tự; hiện backend trong header/body, lịch sử và số phản hồi mỗi replica trong phiên demo | Gateway Nginx Round Robin tới web-frontend-server1/2. Không poll nền làm nhiễu luân phiên; không gọi đây là migrate server | E10 |
| **9. Ứng dụng demo** | Một card Blog và nút mở website độc lập; URL qua Web/Gateway, nguồn/source version nếu đã xác minh | Website Blog thật trên Web server; trạng thái HTTP chỉ hiện khi có kiểm tra tương ứng | R02/E01 và hỗ trợ demo gateway/LB |

Các mục là nhóm chức năng, không bắt buộc xây 9 trang riêng; có thể dùng sidebar/tab nhưng nội dung và thao tác phải rõ. Cấu hình Docker trên Portal ở dạng thông tin chỉ đọc. Không triển khai giao diện nhập Compose rồi chạy/xóa container theo input người dùng.

## 3. Chức năng website Blog riêng

1. Trang chủ Blog có tên/giới thiệu nhóm, nhận diện `MyMiniCloud – Home` để giữ yêu cầu Home ở cổng Web; dẫn tới danh sách bài.
2. Danh sách `/blog/` có nhận diện `MyMiniCloud – Blog`, ít nhất 3 card bài; mỗi card ảnh trái, title/mô tả phải trên desktop; mobile ảnh trên/chữ dưới.
3. Có đủ `blog1.html`, `blog2.html`, `blog3.html`; bài chi tiết có ảnh, đoạn văn học thuật, tiêu đề mục, link danh sách và trang chính. Không dùng modal thay trang HTML.
4. Có menu/CSS riêng của Blog; không hiển thị sidebar quản trị, bảng sinh viên hoặc các card vận hành hạ tầng như một phần của bài viết.
5. Nội dung học thuật về mạng container, dữ liệu bền vững, metrics/logs theo dàn ý đã giao G05; dùng kiến thức chính thức và ví dụ đúng source, không bịa số liệu/chạy thử.
6. Dùng Blog làm Web để thử HTTP 200, assets/ảnh, proxy, Nginx metrics và luân phiên hai Web replica.

E01 cho phép Blog tĩnh. Không bắt buộc CMS, CRUD bài viết, đăng nhập quản trị Blog hoặc database chứa bài viết. API metadata bài viết/tác giả có thể bổ sung riêng nếu muốn minh họa dữ liệu ứng dụng, nhưng không thay API 5 sinh viên và schema `studentdb.students` mà E02/E03 quy định.

## 4. Phương án tách frontend mà giữ các đường dẫn đề

Source mục tiêu trong cùng repo:

```text
web-frontend-server/html/
  index.html                 # Home của website Blog khi mở cổng 8080
  blog/
    index.html               # Danh sách card Blog
    blog1.html … blog3.html
    blog.css, images/
  portal/
    index.html               # Portal riêng
    style.css, script.js …   # Asset Portal, không dùng chung selector toàn cục với Blog
```

Gateway giữ reverse proxy tới Web: root `/` có thể proxy đúng `/portal/index.html` của Web backend; asset `/portal/` được proxy giữ path. Các route `/blog/`, `/api/`, `/auth/`, `/student/`, `/lb/` giữ hành vi theo đề. Không đổi root thành phản hồi giả hoặc bỏ reverse proxy chỉ để tách giao diện.

Web trực tiếp `:8080/` phải trả Home HTML HTTP 200; không thay bằng redirect làm trượt yêu cầu HTTP 200. `:8080/blog/` và `/blog/` qua gateway đều phải trả Blog HTML HTTP 200.

Đây là hướng thiết kế cho task tách frontend, chưa phải cấu hình Nginx đã áp dụng. Codex phải kiểm tra lại route/asset/header và so sánh chức năng sau khi Gemini thực hiện.

## 5. Không phát sinh thêm các hệ thống ngoài đề

- Không dùng E-learning/Firebase làm ứng dụng demo của bài nộp; không thêm chức năng E-learning mới.
- Không xây giao diện tạo/xóa server, chỉnh Compose, Docker shell hoặc quản trị host từ browser.
- Không làm SQL Server Management Studio thu nhỏ: tạo database/bảng và seed theo script; console chỉ kiểm thử endpoint/truy vấn định sẵn, không thực thi SQL tùy ý.
- Không bắt buộc giao diện upload CSV/SQL hoặc CMS Blog. Upload ảnh/PDF theo đề được chứng minh với MinIO.
- Không gán quyền quản trị/secret lên frontend để gọi service. Không coi dữ liệu fixture hoặc thông tin cấu hình là monitoring trực tiếp.

## 6. Thứ tự giao việc đã điều chỉnh

| Bước | Branch / người làm | Đầu ra |
|---|---|---|
| Review prototype Portal đang có | Codex; branch hiện có `feat/portal-cloud-panel` | Commit `616f2e9` chưa được nghiệm thu. Kiểm tra source/evidence và các nhãn “17 Containers Up” viết tĩnh; giữ lịch sử, không đưa vào main chỉ vì đã có card |
| G05 Blog cards/học thuật | Gemini; `feat/personal-blog` cập nhật từ main | Danh sách/bài chi tiết Blog riêng, ảnh/CSS riêng, kiểm tra E01 |
| **G10 Tách hai frontend** | Gemini; `feat/separate-portal-blog-sites` từ main đã tích hợp việc trước | Tách Portal source/asset và Blog Home; root proxy đúng Portal, direct Web Home/Blog và route cũ vẫn đạt; bỏ bài Blog/EL khỏi nội dung Portal |
| G06 Metrics API | Gemini; `feat/portal-metrics-api` | `/api/dashboard` đọc Prometheus thật, lỗi/null/timeout có giới hạn |
| G07 Dashboard | Gemini; `feat/portal-health-dashboard` | KPI/charts/service cards trên Portal riêng, không đưa bài Blog vào dashboard |
| G08 API console | Gemini; `feat/api-console-interface` | API/SQL/Auth/RR trình bày dễ đọc, schema/response đúng, không lộ token |
| **G11 Thu gọn E-learning** | Codex hoặc giao task riêng `chore/retire-elearning-demo` | Bỏ EL khỏi startup/verify/release mặc định, sửa gateway và metadata liên quan; giữ source/lịch sử và volume dữ liệu, không xóa chúng |
| G09 Release UI | Codex; `chore/ui-release-images` | Regression và tag/digest mới đúng source, số service/volume/image ghi theo cấu hình thực tế |
| G02/G03/G04 | Theo branch hồ sơ đã giao | Báo cáo/video/hướng dẫn phản ánh hai frontend và cấu hình cuối, không còn lấy E-learning làm luồng demo |
| QA cuối, duyệt local, AWS | Codex → người dùng → cloud sau duyệt | Kiểm thử đủ output bắt buộc; local không thay cho R14/EC2 |

Mỗi task bắt đầu sau khi main đã tích hợp task trước, không làm đồng thời trong workspace. G10 và G11 đang **CHUA_LAM**. G05/G06/G07/G08/G09 cũng chỉ được tính đạt sau test thật; prototype Portal hiện có không tự thay thế nghiệm thu các task đó.

## 7. Số lượng container và dữ liệu khi bỏ E-learning

Hiện release đã kiểm chứng vẫn có **17 runtime container**, bao gồm 2 container E-learning/Firebase bổ sung. Không tự sửa số hiển thị thành 15 rồi coi đã thu gọn.

Nếu G11 bỏ đúng hai container đó khỏi cấu hình mặc định mà không thêm service khác, mục tiêu sẽ là **15 runtime container**, vẫn đủ 9 vai trò và hai Web replica. Số cuối phải lấy từ Compose/release sau kiểm thử. Volume Firebase cũ được giữ; không gọi toàn bộ volume khai báo/lưu trên máy là số volume đang hoạt động.

Các bài test E-learning có thể giữ như lịch sử/optional, nhưng runner mặc định của bài MiniCloud không được bắt buộc app ngoài phạm vi. Việc thu gọn không được loại bỏ hoặc nới assertion của E01–E10, core SQL/Auth/Storage/DNS/metrics/log/gateway/network/persistence.

## 8. Tiêu chí chấp nhận bản cuối

- Portal và Blog có giao diện/asset/navigation riêng, mở từ hai địa chỉ mục tiêu; Portal chỉ chứa card mở Blog sang tab mới.
- Blog đáp ứng E01 và Web Home/Blog HTTP 200; gateway tiếp tục reverse proxy đúng các route; LB nhận diện cả hai replica.
- Portal hiển thị dữ liệu thật, có loading/error/empty/timestamp, không có badge UP/Healthy suy từ số cấu hình.
- E02/E03 vẫn dùng dữ liệu và schema sinh viên theo PDF; console không biến thành shell/SQL executor tùy ý.
- R06/E05, DNS, Prometheus và Grafana có bằng chứng phù hợp, phân biệt live và snapshot; không công bố link công cụ như một tính năng đã tích hợp đầy đủ.
- Không còn nút/luồng E-learning trong demo chính; sau G11 release mặc định không còn phụ thuộc hai service đó, dữ liệu cũ được giữ.
- Ghi số bài test, container, image, volume và hạn chế theo kết quả thật; không gán 27 bước lịch sử cho suite mới đã đổi.
- Docker Hub, báo cáo/video và EC2 vẫn là các đầu ra của đề; không coi một Portal đẹp là hoàn thành toàn bài.
