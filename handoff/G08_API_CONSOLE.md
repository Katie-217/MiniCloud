# G08 — API Console với terminal kết quả

Trạng thái **CHUA_LAM**. Chỉ thực hiện sau khi Codex nghiệm thu G07 và giao task; main đã tích hợp các task phụ thuộc. Không làm song song trong workspace.

Đọc `AGENTS.md`, [đặc tả UI mới](../DAC_TA_PORTAL_TRANG_API_CONSOLE.md), Flask routes trong `application-backend-server/app.py`, test API/SQL/secure/round robin. Backend hiện là Flask, không chuyển FastAPI.

## Branch và phạm vi

Tạo `feat/api-console-interface` từ main đã tích hợp G07. Được sửa frontend Portal `web-frontend-server/html/portal/**`, test/bằng chứng UI API liên quan và dòng task/nhật ký trong tracker. Không sửa backend/data/schema, Keycloak config, Blog, gateway, Compose/release lock hoặc báo cáo/video. Thiếu API thực thì báo rõ, không giả response hoặc âm thầm mở rộng task backend.

## Đầu ra

1. API Console là mục thứ hai trong sidebar. Chọn operation whitelist, hiển thị HTTP method/path; form chỉ chứa trường backend hỗ trợ. GET hello/student/student-proxy/students-db/notes không có query/body, ghi “Không có tham số”. Không tạo input rồi bỏ qua.
2. Execute gửi request thật; loading, HTTP status, thời gian browser ms, thời điểm. Kết quả chính là terminal **nền sáng/chữ monospace đen**, pretty JSON hoặc response text thật; cuộn riêng, xóa/copy an toàn. Bảng danh sách chỉ là tùy chọn phụ, không thay terminal.
3. Chứng minh JSON 5 sinh viên, SQL ít nhất 3 dòng đúng schema, notes, hello và route `/student/`. Đếm từ response. Không thay dữ liệu sinh viên bằng bài Blog hoặc dùng fixture làm fallback khi API lỗi.
4. Xác thực sv01/sv02: chọn username/password masked, lấy token theo flow hiện có rồi gọi secure. Chỉ hiện kết quả secure đã bỏ bí mật, không render token response. Xóa password sau submit, token trong bộ nhớ; không log/localStorage/copy cURL chứa secret. Anonymous 401 hiển thị đúng là từ chối mong đợi. Giữ `/#secure-demo` và labels/IDs test đang dùng hoặc sửa test hành vi tương đương có căn cứ.
5. View Load Balancer nhập số lượt 1–20/default 8, gửi `/lb/whoami` tuần tự, hiển thị header/body/backend, lịch sử và biểu đồ đếm response thật theo từng replica. Không poll/retry ngầm; không tạo query API không có trong backend.
6. 401/403/503, network error, timeout, empty và non-JSON được hiển thị đúng. Không nhận response thì không bịa HTTP status. Request cũ không ghi đè kết quả operation mới; payload lớn không treo UI. Dynamic content render an toàn, không `innerHTML` từ response.

## Kiểm tra và bàn giao

- Build preview Web/replica theo [kế hoạch UI](../KE_HOACH_NANG_CAP_GIAO_DIEN.md); không publish/đổi digest trong task UI.
- Browser kiểm tra Execute từng operation, nội dung/status/số dòng thật, chuyển endpoint/form, Clear/Copy, desktop/mobile, keyboard. Kiểm tra lỗi/timeout/non-JSON/XSS bằng intercept hoặc test cô lập, không phá dữ liệu/service đang chạy.
- Secure kiểm tra cả hai user và anonymous, password xóa, không lộ JWT trong DOM/console/copy/storage. RR kiểm tra số request đúng giá trị nhập, backend header/body khớp và tổng cột bằng số response thực.
- Chạy lại test API, JSON/SQL students, secure portal, gateway, Web/Blog, round robin liên quan. Không nới assertion chỉ để test xanh. Report/video automation sẽ được cập nhật đúng điều hướng ở G02/G03.
- Minh chứng `evidence/local/ui-api/`; bàn giao base/HEAD SHA, diff, lệnh/kết quả, URL preview và image/source build. Trạng thái G08 chỉ được Codex chấp nhận sau kiểm thử độc lập.
- Commit gợi ý `feat: add interactive API console`, `test: verify API console responses`. Không tự merge/push main, chuyển task hoặc truy cập AWS; dừng bàn giao Codex.
