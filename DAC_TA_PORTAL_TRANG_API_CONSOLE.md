# Đặc tả Portal nền trắng và API Console

Chốt **09/11/2026** theo yêu cầu người dùng. Đây là tiêu chí giao việc, **chưa phải UI đã triển khai/nghiệm thu**. Khi mô tả giao diện cũ mâu thuẫn với tài liệu này, áp dụng tài liệu này; giữ tiêu chí kỹ thuật trong [phạm vi Portal/Blog](PHAM_VI_CHOT_PORTAL_VA_BLOG.md) và PDF.

## 1. Bố cục và màu sắc

- Canvas, sidebar và card nền trắng; chữ chính đen/gần đen (`#111827`), viền xám nhạt (`#e5e7eb`). Không nền slate tối, gradient trang trí hoặc hero lớn.
- Màu dùng cho series biểu đồ, HTTP method và trạng thái khi cần; luôn kèm chữ/đơn vị, không chỉ dựa vào màu. Console kết quả cũng dùng nền sáng, chữ monospace đen.
- Sidebar dọc bên trái khoảng 224px ở desktop; mobile thu gọn thành menu có thể mở/đóng. Chỉ một mục nội dung hiện tại được hiển thị, không xếp mọi chức năng thành trang landing dài.
- Mục đầu **Tổng quan**, mục thứ hai **API Console**. Tiếp theo: **Xác thực**, **Lưu trữ**, **Mạng & DNS**, **Load Balancer**, **Dịch vụ**, **Ứng dụng**. Monitoring/logs truy cập bằng card ở Tổng quan/Dịch vụ; SQL là nhóm thao tác trong API Console.
- Giữ URL hash/deep-link có nghĩa; đặc biệt `/#secure-demo` phải mở đúng mục Xác thực để luồng kiểm thử hiện có hoạt động. Chuyển mục không reset form đang thao tác ngoài ý muốn hoặc tạo nhiều vòng polling.
- Bỏ đoạn giới thiệu dài, slogan, mô tả nội bộ triển khai không giúp thao tác, khối thông tin nhóm lớn và nhãn trạng thái giả. Giữ label, đơn vị, nguồn đo ngắn, thời điểm và lỗi cần để hiểu kết quả.
- HTML/CSS/JS hiện có, asset local, không thêm framework/CDN bắt buộc. Tiêu đề/nhận diện Home và Blog theo đề vẫn còn trong trang tương ứng.

```text
MyMiniCloud       | Tổng quan                 Cập nhật ... [Làm mới]
                  | [CPU %] [RAM %] [Network B/s] [Web req/s]
> Tổng quan       | [Biểu đồ CPU/RAM] [Biểu đồ Network/Requests]
  API Console     | Node: ...   Web: ...    Nguồn đo: Docker VM
  Xác thực        | [Grafana] [Prometheus] [Nhật ký]
  Lưu trữ         |
  Mạng & DNS      | (Chỉ nội dung mục đang chọn)
  Load Balancer   |
  Dịch vụ         |
  Ứng dụng        |
```

## 2. Tổng quan: số thật, mô tả gọn

4 KPI lấy `/api/dashboard` của G06: CPU %, RAM %, network receive B/s, Web requests/s. Biểu đồ 15 phút có timestamp, đơn vị và khoảng trống khi thiếu dữ liệu. Loading, unavailable, partial, stale được thể hiện rõ; không dùng dữ liệu mẫu, random hoặc đổi null thành 0.

CPU/RAM đo Linux VM Docker Desktop; network thuộc namespace exporter; Web request-rate thuộc Nginx được scrape. Chỉ có target node/web hiện được giám sát, không suy tất cả container khỏe. Số service/volume theo cấu hình phải ghi là cấu hình, không có badge “17 Containers Up” hoặc “9/9 Active” viết tĩnh.

Refresh khoảng 10 giây, không chồng request; mất upstream giữ mốc lần thành công gần nhất và báo dữ liệu cũ. Rời view/tắt tab phải dọn timer hoặc tạm dừng; không polling Load Balancer trong nền.

## 3. API Console: chọn thao tác, nhập đúng trường, Execute

Tham khảo cách chọn operation và nhập tham số của [tài liệu API tương tác FastAPI](https://fastapi.tiangolo.com/tutorial/first-steps/#interactive-api-docs). **Backend vẫn là Flask**; đây là yêu cầu trải nghiệm giao diện, không phải chuyển framework hay thêm server FastAPI.

```text
API Console
Nhóm [Dữ liệu v]     Thao tác [Sinh viên SQL v]
GET /api/students-db
Tham số: Không có
[Execute] [Xóa kết quả]

Response                          HTTP 200 · 32 ms · 14:32:10
┌─────────────────────────────────────────────────────────┐
│ [                                                       │
│   { "id": 1, "student_id": "...", "fullname": "...", ... }│
│ ]                                                       │
└─────────────────────────────────────────────────────────┘
[Sao chép kết quả]   [JSON | Bảng (nếu phù hợp)]
```

Kết quả chính là console/terminal nền sáng hiển thị response JSON có thụt dòng hoặc text lỗi thực tế. Không mở tab JSON làm luồng chính. Đây là viewer kết quả HTTP, không thực thi shell, Docker command hoặc SQL tùy ý. Bảng chỉ là chế độ xem phụ cho response dạng danh sách.

| Operation đã có | Trường nhập đúng hợp đồng hiện tại | Kết quả cần giữ |
|---|---|---|
| `GET /api/hello` | Không có | JSON thông điệp đúng theo đề |
| `GET /api/student` | Không có | 5 sinh viên JSON, trường id/name/major/gpa |
| `GET /student/` | Không có | Cùng dữ liệu qua route E09 |
| `GET /api/students-db` | Không có | Ít nhất 3 dòng SQL, id/student_id/fullname/dob/major |
| `GET /api/notes` | Không có | Dữ liệu MariaDB minicloud.notes |
| `GET /api/secure` không token | Không có | HTTP 401 là kết quả bảo vệ mong đợi |
| Lấy token Keycloak rồi `GET /api/secure` | Chọn sv01/sv02, mật khẩu masked; client/grant theo cấu hình đang dùng | Thành công 200 có username; thất bại hiển thị đúng status của bước lỗi |

GET dữ liệu hiện không hỗ trợ query/body: không tạo ô tìm kiếm/ID rồi bỏ qua giá trị nhập. Nếu bổ sung bộ lọc hiển thị phía client phải ghi rõ chỉ lọc kết quả đã nhận, không gọi đó là truy vấn backend. Không đổi contract API hoặc thay dữ liệu sinh viên bắt buộc bằng Blog.

Mỗi lượt Execute có trạng thái đang gửi, HTTP status thật, thời lượng đo ở browser bằng đồng hồ đơn điệu, thời điểm gọi; không gọi thời lượng browser là latency server. Lỗi mạng chưa có HTTP response phải ghi “Không nhận được phản hồi”, không tạo HTTP 500 giả. Response không phải JSON vẫn đọc được. 401/403/503 được phân biệt và không bị đổi thành 200.

Chỉ gọi endpoint whitelist cùng origin. Không có ô URL upstream/PromQL/SQL/command tùy ý. Dynamic response render qua `textContent` hoặc DOM an toàn. Giới hạn chiều cao console và cho cuộn riêng; payload quá lớn có thông báo cắt hiển thị, không làm treo trang. Không lộ token, mật khẩu, cookie trong console, nút copy, request preview, ảnh/log hoặc localStorage; mật khẩu xóa sau submit, token chỉ giữ trong bộ nhớ đủ gọi secure. Giữ luồng anonymous và cả sv01/sv02.

Load Balancer có view riêng: số lượt nhập là tham số của vòng lặp client (mặc định 8, giới hạn 1–20), không phải query API mới. Gửi tuần tự `/lb/whoami`; bảng/console chứa HTTP/header/body/backend và biểu đồ đếm response thực tế. Không retry/poll ngầm làm sai số lượt.

## 4. Card dịch vụ: mở đúng đích

Mỗi card có tên, một câu ngắn về nhiệm vụ, nút hành động có nghĩa. Web UI bên ngoài Portal mở tab mới với `noopener`; các mục nội bộ chuyển đúng view. Trạng thái chỉ hiện nếu có probe thật và timestamp.

| Card | Mô tả gợi ý | Hành động / đích local |
|---|---|---|
| Grafana | Biểu đồ CPU, RAM và mạng | Mở `http://localhost:3000/d/system-health-521h0092` |
| Nhật ký | Xem log dịch vụ MiniCloud | Mở `http://localhost:3000/d/minicloud-service-logs` |
| Prometheus | Query metrics và xem target | Mở `http://localhost:9090/` |
| Keycloak | Quản lý realm, user và client | Mở `http://localhost:8081/auth/admin/` |
| MinIO | Quản lý bucket và tệp | Mở `http://localhost:9001/` |
| MariaDB | Lưu dữ liệu SQL | **Xem API dữ liệu SQL** → API Console chọn `/api/students-db`; cổng 3306 là SQL, không có HTTP Web UI |
| Bind9 | Phân giải tên miền lab | **Xem DNS** → view Mạng & DNS; cổng 1053 không phải trang Web |
| App/API | Xử lý request và truy xuất dữ liệu | **Thử API** → API Console |
| Blog | Website học thuật được host bằng Nginx | **Mở website Blog** → `http://localhost:8080/` |

Không tự thêm Adminer/phpMyAdmin để tạo link MariaDB. Card dịch vụ có thể kèm thông tin đọc-only cổng/network/volume trong phần chi tiết, không biến Portal thành công cụ sửa Compose. Danh mục 9 vai trò phải đối chiếu cấu hình thực tế; các card shortcut ở trên không phải phép đếm 9 server.

## 5. Blog: đóng gói từ repo, host trên Nginx

**Người dùng đã chọn:** source Blog trong repo MiniCloud → build image Web → triển khai Nginx qua Compose → phát hành Docker Hub/tag/digest đã kiểm tra. Portal chỉ có một card mở ứng dụng. Không xây chức năng upload ZIP, tự deploy source hoặc CMS trên Portal.

Blog có Home và `/blog/`, 3 card ảnh trái/chữ phải, 3 trang HTML chi tiết đúng E01, menu/CSS riêng. Dùng nền trắng/chữ đen nhưng không mang sidebar hạ tầng vào Blog. Giữ các đường dẫn/HTTP 200 và proxy hiện có theo [phạm vi chốt](PHAM_VI_CHOT_PORTAL_VA_BLOG.md). G05 làm nội dung/card; G10 tách frontend/routing; G09 chốt image đúng source để partner mở bằng release. Không cần thêm container chỉ để tách giao diện.

## 6. Phân chia task và nghiệm thu

Thứ tự vẫn **G11 → review prototype → G05 → G10 → G06 → G07 → G08 → G09** rồi hồ sơ, QA và người dùng duyệt local. Chưa thao tác AWS.

- G07 theo [phiếu dashboard/sidebar](handoff/G07_LIGHT_SIDEBAR.md): nền trắng, shell/sidebar, metrics, card công cụ, deep-link. Không lập trình giả chức năng API để lấp chỗ trống.
- G08 theo [phiếu API Console](handoff/G08_API_CONSOLE.md): chọn operation, form đúng contract, Execute, terminal kết quả, Auth và RR. Không đổi Flask/SQL/schema.
- Codex kiểm tra desktop 1440×900/mobile 390×844, thao tác bàn phím/sidebar/deep-link, console error và failed request trong luồng chính. Giữ E01–E10 và các test core, secure, gateway, LB; thêm test có ý nghĩa cho UI mới.
- Chụp ảnh sau khi dữ liệu tải thật, ghi branch/SHA source build và image đang chạy. Source mới chưa build không phải output UI mới đã đạt. G09 chốt digest mới; không đè tag cũ.

Các phiếu/spec này chỉ thay đổi kế hoạch. Tiến độ runtime cập nhật riêng khi có code và kiểm thử; giữ nguyên kết quả lịch sử R/E đến lúc có kết quả mới.
