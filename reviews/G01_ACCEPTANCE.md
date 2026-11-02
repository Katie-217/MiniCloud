# Nghiệm thu G01 — PASS

Codex kiểm tra ngày **02/11/2026**, HEAD Gemini **`b31a1ef62de3b9b9519d44b360f3fe8dc7f8d565`**, base **`fd0b4e6`**. Task G01 được nghiệm thu; có thể chuyển **G02** sau khi main chứa commit này và biên bản nghiệm thu.

**20/20 kiểm tra nghiệm thu/cấu hình đạt**, chi tiết trong [G01-acceptance-b31a1ef.json](G01-acceptance-b31a1ef.json). Đây không phải bộ 27 bước chức năng.

| Hạng mục | Kết quả |
|---|---|
| Phạm vi diff | Chỉ tracker, kế hoạch và handoff G01; không sửa code runtime, Compose, assertion hoặc evidence lịch sử |
| Git | Working tree sạch, diff commit và working diff không lỗi whitespace; author giữ nguyên, commit message đúng quy ước |
| Trạng thái | Đúng 14 R DAT / 10 E DAT; R14 chờ, R16–R18 CHO_KIEM_THU |
| Nội dung | Giữ nhật ký lịch sử; phân biệt minh chứng 29/10 và kiểm tra hiện tại; FIX-005 dẫn đúng recreate true tại 1f27f82 và test thường false tại baseline |
| Link/mã hóa/bí mật | Link Markdown tồn tại, UTF-8 hợp lệ, không có giá trị bí mật từ .env trong file sửa |
| G01-F01 | Đóng: bộ 27 bước được ghi đúng `check_all.py --screenshots`, persistence/E-learning là kiểm tra bổ sung |
| G01-F02 | Đóng: 3 Web là 3 container độc lập; restart policy thuộc service/container, 8 volume lưu dữ liệu |
| G01-F03 | Đóng: không còn dòng trắng thừa hay thay đổi dở |
| Compose và trạng thái | Config parse được, 17 service/8 volume, service restart unless-stopped; 17 container đang chạy, healthcheck khai báo đều healthy |

**Giới hạn:** chưa chạy lại full suite chức năng/persistence trong lượt nghiệm thu tài liệu. Kết quả chức năng ngày 29/10 vẫn giữ nguyên ngày, không đổi thành kết quả ngày 02/11. AWS chưa được truy cập hoặc triển khai. Engine hiện kết nối Docker 29.0.1; Running/healthy không thay cho kiểm tra chức năng.

## Task kế tiếp

G02: branch mới `docs/refresh-local-report` từ main đã tích hợp G01. Phạm vi và tiêu chí ở [BAN_GIAO_GEMINI.md](../BAN_GIAO_GEMINI.md), mục 5. Cần báo cáo 5 chương + phụ lục, sơ đồ 17 container/9 vai trò/8 volume, ảnh thật từng server, đúng số liệu và release digest; build PDF/DOCX/HTML và xác minh PDF cuối trong MinIO. R16 tổng thể vẫn CHO_KIEM_THU vì chưa có cloud.

Gemini chỉ làm G02 rồi trả branch/base/HEAD SHA, file đổi, lệnh kiểm tra và kết quả, đường dẫn artifacts và hạn chế để Codex nghiệm thu. Không tự merge main hoặc chuyển G03.
