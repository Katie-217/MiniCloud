# Object Storage — MinIO

Sử dụng source chính thức tag `RELEASE.2025-04-22T22-12-26Z`, SHA256 archive:
`1a63209927b9d1fb239b2a776b7b01d1902eff19379a108f4bc7005edcc0968c`.

Tại thời điểm kiểm tra, image `minio/minio` và `minio/mc` trên Docker Hub trả 404; manifest tương ứng trên Quay không có; URL binary archive trả 410. Vì vậy Dockerfile build source chính thức thay vì phụ thuộc image không còn tải được.

Nguồn: https://github.com/minio/minio/releases/tag/RELEASE.2025-04-22T22-12-26Z

Source giữ Console đầy đủ cho bài lab; binary tự build không có release metadata do không chạy pipeline phát hành của upstream. Image ghi rõ tag nguồn ở OCI label, giữ LICENSE AGPL-3.0. Dockerfile/source URL công khai đi cùng repository này để tái tạo image. Đây là phiên bản dành cho bài lab local.

- API: http://localhost:9000
- Console: http://localhost:9001
- Credentials: đọc `MINIO_ROOT_USER` và `MINIO_ROOT_PASSWORD` trong `.env` local.
- Dữ liệu: named volume `minio-data`; không lưu vào Git.
- `.venv/Scripts/python scripts/check_storage.py` tạo bucket demo, upload HTML và tải về đối chiếu SHA256.
