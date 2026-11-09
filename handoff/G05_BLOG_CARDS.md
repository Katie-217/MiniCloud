# G05 — Phiếu giao Gemini: Blog card và nội dung học thuật

Ngày giao: **09/11/2026**. Trạng thái **CHUA_LAM**, chưa phải biên bản nghiệm thu.

> **Chờ G11:** theo chỉ dẫn mới nhất, [gỡ E-learning](G11_REMOVE_ELEARNING.md) được ưu tiên trước. Không thực hiện G05 đồng thời; Codex sẽ giao lại sau nghiệm thu G11.

> **Bổ sung phạm vi chốt:** [Portal và Blog là hai frontend riêng](../PHAM_VI_CHOT_PORTAL_VA_BLOG.md). G05 làm website Blog có menu/CSS và trang bài riêng; không thêm danh sách bài vào Portal. G10 phụ trách việc tách source Portal và Blog Home/cấu hình route; G05 không tự đổi gateway/root Portal hoặc xóa E-learning.

> **Thiết kế mới nhất:** Blog nền trắng/chữ đen, card ảnh trái/chữ phải, menu riêng; không sidebar hạ tầng. Người dùng chọn source trong repo → build image → Nginx host, Portal có card mở ứng dụng. Không làm upload ZIP/CMS. Xem [đặc tả mới](../DAC_TA_PORTAL_TRANG_API_CONSOLE.md).

## Phạm vi

Đọc `AGENTS.md`, [kế hoạch UI](../KE_HOACH_NANG_CAP_GIAO_DIEN.md), PDF trang 12–13 và 21, `scripts/check_blog.py`, `scripts/check_web.py` và source Blog.

Tiếp tục branch chức năng **`feat/personal-blog`**, đưa branch này lên main mới nhất bằng fast-forward trước khi sửa. Không quay lại source cũ của branch rồi ghi đè main. Nếu branch không thể fast-forward, báo trạng thái Git để Codex xử lý; không reset/force.

Được sửa: `web-frontend-server/html/blog/**`; ưu tiên CSS riêng trong thư mục Blog, tránh phụ thuộc style Portal; script/ảnh/JSON test liên quan E01; dòng E01/nhật ký/task G05 trong tracker. Không sửa Portal, Flask, Keycloak, gateway, Compose/release lock, Flutter, báo cáo hoặc video trong G05.

## Đầu ra

1. `/blog/` hiển thị 3 card ngang xếp dọc: ảnh bên trái, title/description 2–3 dòng bên phải; một anchor chính mỗi bài; hover/focus rõ.
2. Mobile 390px: ảnh trên, chữ dưới, không tràn toàn trang. Desktop 1440px: ảnh thực sự nằm trái chữ, không biến thành grid card vuông.
3. Giữ `/blog/blog1.html`, `blog2.html`, `blog3.html`; click card mở trang chi tiết riêng, có ảnh, cấu trúc đọc dễ nhìn, tác giả nhóm, mục h2/h3, ví dụ, link đọc thêm và điều hướng Blog/Home.
4. Viết mới 3 bài chia sẻ học thuật tiếng Việt theo dàn ý mục 3.4 của kế hoạch UI; khoảng 500–700 từ/bài là mục tiêu biên tập. Chủ đề tự chọn được PDF cho phép; không bịa dữ kiện, không sao chép nguyên bài nguồn.
5. Có ảnh minh họa phù hợp. Ưu tiên SVG local hiện có; asset không phụ thuộc hotlink/CDN. Không sửa ảnh/avatar hoặc tạo thông tin MSSV còn thiếu.
6. Giữ nhận diện `MyMiniCloud – Blog`, trả HTTP 200 qua cổng Web 8080 và gateway 80, Home hiện tại không bị CSS mới làm hỏng.
7. Blog là ứng dụng demo riêng: menu/nội dung học thuật của Blog, không chứa dashboard hạ tầng hoặc bảng sinh viên. Liên kết về Blog/Home vẫn theo yêu cầu; Portal chỉ mở Blog sang tab mới sau G10.

## Preview và kiểm tra

Xem mục 7 trong kế hoạch UI trước khi build. Dockerfile COPY nội dung Web vào image nên cần build/recreate Web chính và hai replica; giữ nguyên App và volume. Không chạy `run_release.py` sau đó để vô tình quay về UI release cũ. Không tự đổi release digest; Codex sẽ làm G09 sau các task UI.

Chạy các bài Web/Blog hiện có; bổ sung kiểm tra trình duyệt có ý nghĩa cho bố cục desktop/mobile, ảnh tải thật và navigation. Không thay assertion đúng thành kiểm tra lỏng để đạt.

Minh chứng mới: `evidence/local/ui-blog/` gồm ảnh index desktop/mobile, chi tiết 3 bài, JSON hoặc ghi chú có lệnh/kết quả/viewport/HEAD đã build. Kết quả chỉ ghi PASS khi đã chạy; nếu Docker chưa sẵn sàng ghi NOT_RUN.

Commit gợi ý: **`feat: redesign academic blog cards`**. Các commit bổ sung liên quan G05 cũng dùng type + 4–5 từ tiếng Anh. Không stage file ngoài task, không merge/push main, không làm G06.

## Bàn giao cho Codex

Trả task, branch, base/HEAD SHA, các file đổi, source HEAD đã build lên URL preview, ảnh/evidence, lệnh kiểm tra với PASS/FAIL/NOT_RUN, giới hạn và chỗ cần review. Dừng chờ nghiệm thu. Codex sẽ kiểm tra diff, mở UI, đối chiếu E01 và chạy regression trước khi tích hợp.

## Prompt copy cho lượt giao đầu

```text
Thực hiện riêng G05 của MiniCloud. Codex là leader/tester.
Workspace: D:\Điện toán đám mây

Đọc AGENTS.md, KE_HOACH_NANG_CAP_GIAO_DIEN.md và handoff/G05_BLOG_CARDS.md; đối chiếu PDF trang 21.
Kiểm tra Git sạch và main mới nhất. Tiếp tục feat/personal-blog bằng fast-forward từ main, không reset/force hoặc sửa trên baseline cũ.

Làm danh sách Blog thành 3 card ngang: thumbnail trái, title/mô tả ngắn phải; mobile ảnh trên chữ dưới. Mỗi card mở trang blog1/2/3.html riêng. Viết mới 3 bài chia sẻ học thuật theo dàn ý kế hoạch, có ảnh, ví dụ và nguồn đọc thêm. Giữ HTTP 200, title MyMiniCloud – Blog, liên kết Blog/Home; CSS mới scope riêng, không làm hỏng Portal.

Chỉ sửa file thuộc G05. Build preview Web theo hướng dẫn trong kế hoạch; không đổi release lock và không chạy run_release.py làm quay UI về bản cũ. Chạy test Web/Blog và kiểm tra desktop/mobile; lưu ảnh và kết quả thật trong evidence/local/ui-blog/.

Commit tiếng Anh, ví dụ feat: redesign academic blog cards. Trả branch/base/HEAD SHA, file đổi, URL và HEAD đã build, lệnh/kết quả và ảnh. Không lộ bí mật, xóa volume, đổi runtime khác, merge/push main hoặc làm G06. Dừng để Codex nghiệm thu.
```
