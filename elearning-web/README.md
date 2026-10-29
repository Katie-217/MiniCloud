# E-learning demo trong MyMiniCloud

Source gốc: [Katie-217/E-learning-Management-App](https://github.com/Katie-217/E-learning-Management-App), branch main, commit `9e9ebd539c7f08092ea6855c9aceafe645bd28e0`. Chi tiết nguồn và phạm vi nhập trong `provenance.json`. Giữ thông tin tác giả trong mã nguồn. README gốc mô tả MIT nhưng checkout khảo sát không có file LICENSE riêng; không tự tạo tuyên bố giấy phép thay tác giả.

Bản điều chỉnh dùng Flutter Web + Firebase Emulator trong Docker. Không mang Firebase project configuration thật, service account hoặc database thật vào MiniCloud. Demo này bổ sung giao diện ứng dụng; Flask/MariaDB/Keycloak/MinIO vẫn thực hiện riêng đầy đủ các output trong đề.

Build từ source bằng Flutter 3.35.7 / Dart 3.9.2:

```powershell
.venv/Scripts/python.exe scripts/build_elearning.py
docker compose up -d --build --wait firebase-emulator-server elearning-web-server
.venv/Scripts/python.exe scripts/seed_elearning.py
docker compose exec -T api-gateway-proxy-server nginx -t
docker compose exec -T api-gateway-proxy-server nginx -s reload
```

URL: `http://localhost/elearning/`. Tài khoản `instructor@example.test` và `student@example.test`; mật khẩu được sinh trong `.env` dưới khóa `ELEARNING_INSTRUCTOR_PASSWORD` / `ELEARNING_STUDENT_PASSWORD`, không in ra log hay commit. Đây là tài khoản giả trong emulator.

Auth/Firestore/Storage emulator chỉ publish cổng host loopback 9099/8180/9199. Chỉ demo trên chính máy chạy Docker ở bước local này; truy cập từ máy khác cần thiết lập đường dẫn kết nối riêng, chưa coi đã đạt phần EC2. Dữ liệu export/import ở volume `firebase-data`; dừng container bình thường để có export, hoặc chạy `firebase emulators:export /data/export --force --project demo-minicloud` trong container trước khi sao lưu.

Không triển khai Cloud Functions/Google Sign-In/email thật; chức năng xem trước link ngoài chưa nằm trong luồng demo đã cam kết. Syncfusion license không được nhúng lại từ repo nguồn; nếu cần bỏ watermark, cung cấp license hợp lệ bằng biến build `SYNCFUSION_LICENSE`. Không tự coi mọi chức năng của đồ án E-learning đã kiểm thử chỉ vì build thành công.

Điều chỉnh đã thực hiện: sửa script build cho đường dẫn Windows có dấu bằng thư mục tạm; bỏ cấu hình Firebase thật; phục vụ Web dưới `/elearning/`; dùng account/data emulator riêng; kết nối nút Manage; thay số sinh viên “Loading…” cố định bằng truy vấn ghi danh thật. `vendor/firebase_auth_web` giữ bản 5.15.3 và LICENSE BSD, bổ sung một nhánh khởi tạo Auth emulator trước khôi phục phiên trong release, chỉ khi có build flag `MINICLOUD_LOCAL_EMULATORS=true`. Không sửa SDK Flutter hoặc package cache toàn máy.

Kiểm thử: `scripts/check_elearning.py` cho hai vai trò, xem khóa học, tạo khóa học bằng UI, số ghi danh và giữ phiên sau refresh; `scripts/check_elearning_persistence.py` cho read/write, hai UID, khóa học và object qua recreate. Minh chứng trong `evidence/local/elearning-*.json/.png`. Các chức năng khác của đồ án gốc chưa được xác nhận đầy đủ.
