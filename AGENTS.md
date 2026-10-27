# Quy ước làm việc MyMiniCloud

## Phạm vi và thứ tự

- Ưu tiên yêu cầu bắt buộc trên local của `Báo Cáo Cuối Kỳ.docx.pdf`, sau đó hoàn tất đủ 10 mục mở rộng, Docker Hub, báo cáo, video và minh chứng local trước khi người dùng kiểm tra bản cuối.
- Theo chỉ dẫn mới nhất ngày 27/10/2026: chỉ triển khai AWS sau khi người dùng kiểm tra và xác nhận bản local đạt. Không tự tạo/truy cập tài nguyên AWS trong giai đoạn này. R14 và hồ sơ cloud vẫn chưa hoàn thành dù local đã đạt.
- Đối chiếu `KE_HOACH_MINICLOUD_2_NGAY.md` để tra yêu cầu theo trang PDF; dùng `KE_HOACH_HOAN_THIEN_LOCAL.md` cho công việc tiếp theo. `KE_HOACH_TRIEN_KHAI_BAT_BUOC.md` lưu giai đoạn nền tảng đã thực hiện.
- Repo đang đánh giá để tái sử dụng là `Katie-217/E-learning-Management-App` theo chỉ dẫn mới nhất; Coffee Shop là phương án đã khảo sát trước. Kiểm tra branch và source commit trước khi nhập. Không tự push thay đổi sang repo nguồn, không dùng database thật hoặc chạy seed xóa dữ liệu của repo nguồn.
- Tuân thủ hướng dẫn trong đề khi khả thi. Nếu mẫu có lỗi hoặc mâu thuẫn, ghi rõ căn cứ, cách điều chỉnh và kết quả kiểm thử trong `TIEN_DO_OUTPUT.md`.

## Git và commit theo yêu cầu người dùng

- Mỗi nhóm yêu cầu có một branch riêng theo bảng trong kế hoạch triển khai.
- Mỗi thay đổi chức năng hoặc mỗi output hoàn thành có một commit riêng; không gom nhiều chức năng độc lập vào một commit lớn.
- Commit message dùng **tiếng Anh**, ngắn gọn, đúng ý chính. Định dạng: `<type>: <English summary of 4–5 words>`. Số từ tính phần sau tiền tố; dùng `feat`, `fix`, `chore`, `test`, `docs` phù hợp.
- Ví dụ hợp lệ: `feat: serve home and blog`, `feat: add hello API endpoint`, `fix: correct authentication proxy routing`, `docs: update output tracking status`.
- Kiểm tra diff, chạy kiểm thử phù hợp, cập nhật tiến độ rồi commit các file liên quan. Không đánh dấu output đạt nếu mới viết cấu hình mà chưa kiểm thử thực tế.
- Branch chức năng bắt đầu từ `main` đã tích hợp nhóm trước; hoàn tất và kiểm thử nhóm hiện tại trước khi tích hợp nhóm kế tiếp. Tránh để các nhóm phụ thuộc nằm ở những branch chưa được tích hợp.
- Không thay đổi author Git đã được cấu hình trừ khi người dùng yêu cầu.
- Không ghi đè lịch sử remote, không force push, không loại bỏ nội dung repo người dùng đã tạo.

## Theo dõi và minh chứng

- `TIEN_DO_OUTPUT.md` là bảng trạng thái hiện tại: đã đạt, đang làm, cần fix, chưa làm và phụ thuộc người dùng.
- Cập nhật bảng khi thay đổi trạng thái output; ghi rõ branch/commit, lệnh kiểm thử, kết quả và đường dẫn minh chứng.
- Lưu bằng chứng riêng cho local và EC2. Viết rõ giới hạn của số liệu monitoring và những phần chưa kiểm chứng.
- Không commit `.env` chứa mật khẩu, private key, access token hay dữ liệu volume. Dùng `.env.example` cho cấu trúc cấu hình.
- Không dừng hoặc xóa container ngoài project; không xóa volume dữ liệu để sửa lỗi thông thường.

## Cách dùng môi trường

- Shell hiện tại là PowerShell trên Windows; dùng `curl.exe` để tránh alias và chỉ dùng cú pháp Bash khi chạy trong môi trường Bash xác định.
- Giữ tên service nhất quán, phân biệt cổng host và cổng nội bộ, dùng network `cloud-net` theo đề.
- Không tự coi quyền EC2, Docker Hub hay quyền push repo là đã kiểm chứng; xác minh trước khi đánh dấu sẵn sàng.
