# MiniCloud
xây dựng hệ thống Cloud thu nhỏ (MyMiniCloud) gồm 9 loại máy chủ cơ bản, mô phỏng các thành phần trong hạ tầng của một Cloud Platform (như AWS, Azure, GCP).

Nhóm: **Võ Thị Thiên Kim — 521H0092**, **Diệp Yến Nhi — chờ MSSV**.

Ưu tiên hiện tại: hoàn thành và kiểm thử phần bắt buộc trên local. AWS chờ thông tin từ người dùng; các mục mở rộng làm sau phần bắt buộc.

## Chuẩn bị

Docker Desktop dùng Linux containers, Docker Compose v2, Git và Python 3.11+ cho các script quản lý/kiểm thử.

```powershell
python scripts/setup.py
python -m venv .venv
.venv/Scripts/python -m pip install -r scripts/requirements-dev.txt
docker compose config --quiet
```

Mật khẩu local sinh ngẫu nhiên trong `.env`, không commit file này. Không ghi đè `.env` đã có khi chạy lại setup.

## Tài liệu và tiến độ

- [Yêu cầu theo PDF](KE_HOACH_MINICLOUD_2_NGAY.md)
- [Thứ tự triển khai và branch](KE_HOACH_TRIEN_KHAI_BAT_BUOC.md)
- [Output đã đạt, cần fix, chưa làm](TIEN_DO_OUTPUT.md)

Mỗi nhóm có branch riêng; mỗi chức năng/output có commit nhỏ, thông điệp tiếng Anh theo `type: summary`.
