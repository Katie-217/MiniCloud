# G07 — Dashboard nền trắng và sidebar trái

Trạng thái **CHUA_LAM**. Chỉ thực hiện khi Codex giao sau G11/G05/G10/G06 đã nghiệm thu và tích hợp main. Không làm đồng thời với task khác.

Đọc `AGENTS.md`, [đặc tả UI mới](../DAC_TA_PORTAL_TRANG_API_CONSOLE.md), [phạm vi Portal/Blog](../PHAM_VI_CHOT_PORTAL_VA_BLOG.md), hợp đồng `/api/dashboard` và test secure hiện có.

## Branch và phạm vi

Tạo `feat/portal-health-dashboard` từ main đã tích hợp task trước. Được sửa source Portal dưới `web-frontend-server/html/portal/**`, test UI/dashboard và bằng chứng `evidence/local/ui-portal/`, dòng task/nhật ký liên quan trong tracker. Không sửa Blog, backend metrics, DB/Auth/config gateway, Compose, release lock, báo cáo/video. Phát hiện lỗi upstream thì báo Codex, không trộn fix backend vào branch UI.

## Đầu ra

1. Nền trắng/chữ đen; sidebar trái, Tổng quan đầu tiên, API Console thứ hai. Desktop/mobile không tràn ngang; menu mobile đóng/mở được bằng bàn phím, focus rõ.
2. Chỉ view đang chọn được hiển thị; URL hash có thể mở lại đúng view. `/#secure-demo` kích hoạt Xác thực, giữ form/labels và hành vi secure hiện có. API Console dùng giao diện hiện có ở view thứ hai; G08 mới làm lại console, không dựng response mẫu.
3. 4 KPI và biểu đồ 15 phút dùng `/api/dashboard` thật. Có đơn vị, timestamp, loading/error/empty/partial/stale; null không thành 0. Ghi ngắn phạm vi VM/exporter. Không badge “17 Containers Up”/“9/9 Active” từ hằng số.
4. Refresh khoảng 10 giây, không chồng request/timer; điều hướng không tạo thêm polling hoặc gọi LB ngầm. Không dùng Docker socket/cAdvisor mới trong task này.
5. Card công cụ có tên, một câu nhiệm vụ và nút mở đúng đích theo đặc tả. MariaDB/Bind9 chuyển view nội bộ, không link HTTP vào cổng SQL/DNS. Một card Blog mở website riêng, không chứa danh sách bài/iframe hoặc E-learning.
6. Bỏ hero/đoạn mô tả thừa; giữ nhận diện bắt buộc, label, lỗi và nguồn số liệu cần để kiểm chứng. CSS Portal không ảnh hưởng Blog.

## Kiểm tra và bàn giao

- Build preview Web và hai replica theo mục 7 [kế hoạch UI](../KE_HOACH_NANG_CAP_GIAO_DIEN.md). Không chạy pinned release để vô tình ghi đè preview; không publish tag trong G07.
- Browser kiểm tra desktop/mobile, sidebar/deep-link, metric so với API, timer sau chuyển view; tạo trường hợp lỗi/empty bằng intercept hoặc test cô lập, không dừng service chung. Không chỉ chụp screenshot có số bất kỳ.
- Chạy các test Web/Blog/gateway/secure liên quan; giữ assertion secure sv01/sv02, thiếu token 401 và che bí mật. Không bỏ kiểm tra do sidebar thay đổi.
- Bàn giao base SHA, HEAD, diff, lệnh/kết quả PASS/FAIL/NOT_RUN, URL preview, image/source đã build, ảnh và hạn chế. Cập nhật đúng dòng G07, không tự tính các task khác đạt.
- Commit gợi ý `feat: build light portal dashboard`, `test: verify portal sidebar behavior`. Không tự merge/push main, chuyển sang G08 hoặc thao tác AWS. Dừng để Codex nghiệm thu độc lập.
