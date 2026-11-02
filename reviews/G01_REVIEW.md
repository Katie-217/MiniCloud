# Codex review G01 — Cần sửa trước khi nghiệm thu

Ngày review: **02/11/2026**. Branch được review: `docs/reconcile-local-status`, HEAD `14d5399b69619ce58bca78a405f8545e6af50795`, base `fd0b4e6e15faca736441f686734248e3be321c32`.

**Kết luận: CHANGES_REQUESTED. Chưa merge G01; chưa giao G02.**

Kết quả kiểm tra chi tiết: [G01-review-14d5399.json](G01-review-14d5399.json). Đây là review độc lập trong worktree/branch `test/review-g01-status`; không sửa branch Gemini hoặc minh chứng runtime lịch sử.

## Các điểm cần sửa

| ID | Mức | Vị trí ở bản Gemini | Sai lệch / ảnh hưởng | Điều kiện đóng |
|---|---|---|---|---|
| G01-F01 | P2 | `KE_HOACH_HOAN_THIEN_LOCAL.md:116` | Gọi `scripts/check_stack.py` là bộ 27 bước. Script này chỉ kiểm tra trạng thái container/restart/network; dùng theo hướng dẫn sẽ bỏ qua kiểm thử chức năng. | Ghi `.venv/Scripts/python scripts/check_all.py --screenshots` cho 27 bước. Nêu persistence/E-learning bổ sung chạy riêng hoặc dùng `run_release.py --verify`; không tính chúng nằm sẵn trong 27 bước. |
| G01-F02 | P2 | `KE_HOACH_HOAN_THIEN_LOCAL.md:38`, `:54`; `TIEN_DO_OUTPUT.md:119` | Web chính bị mô tả là alias của 2 replica; restart policy bị gán cho volume. Thông tin sai có thể bị đưa tiếp vào sơ đồ/báo cáo G02. | Ghi 3 container Web độc lập: Web chính `web-frontend-server` và 2 replica server1/server2. `restart: unless-stopped` áp dụng cho service/container; 8 named volume lưu dữ liệu. Sửa cả hai tài liệu. |
| G01-F03 | P3 | `handoff/G01.md:69`, working tree | Có thay đổi chưa commit là dòng trắng cuối file; `git diff --check` hiện trả exit 2. Diff commit `main...HEAD` đạt, working tree chưa đạt. | Bỏ dòng trắng thừa, chạy lại kiểm tra trên diff commit và working tree, commit các chỉnh sửa liên quan; trả branch sạch. |

Các số dòng trên áp dụng cho HEAD và working tree tại thời điểm review, không phải file ở main.

## Những phần đã đạt

- Chỉ 3 file trong phạm vi được sửa; không có thay đổi runtime, Compose, test assertion hoặc evidence ngày 29/10.
- Đúng 14 dòng R DAT và 10 dòng E DAT; R14 CHO_THONG_TIN, R16–R18 CHO_KIEM_THU.
- Link Markdown được kiểm tra đều tồn tại; file đọc UTF-8; không tìm thấy giá trị mật khẩu/token `.env` trong các file thay đổi.
- Nhật ký lịch sử ngày 26–28/10 được giữ; FIX-005 dẫn đúng hai lần chạy: commit `1f27f82` có recreate true, JSON mới nhất tại baseline ghi false cho lượt test thường.
- Branch bắt đầu từ main đúng base, author giữ nguyên, commit message đúng 4–5 từ sau tiền tố.

## Trạng thái môi trường tại lượt review

`docker info` hiện **kết nối được**, server 29.0.1. Compose config hợp lệ: **17 service, 8 volume**; `docker ps` thấy 17 container MyMiniCloud đang Up, các service có healthcheck hiển thị healthy. Đây là kiểm tra cấu hình/trạng thái, **không phải full regression mới**.

Không chạy lại bộ 27 bước/persistence chỉ để review thay đổi tài liệu. Kết quả chức năng vẫn lấy minh chứng ngày 29/10. Khi sửa tài liệu, ghi việc engine chưa kết nối là **ở lần rà soát ban đầu**, tránh mô tả như trạng thái hiện tại cố định; không đổi lịch sử hoặc tự tuyên bố suite hôm nay đã PASS.

## Prompt trả Gemini

```text
Codex đã review G01 commit 14d5399: CHANGES_REQUESTED, chưa merge và chưa chuyển G02.

Tiếp tục trên docs/reconcile-local-status. Chỉ sửa TIEN_DO_OUTPUT.md, KE_HOACH_HOAN_THIEN_LOCAL.md và handoff/G01.md:

1. Sửa hướng dẫn kiểm thử: check_stack.py không phải bộ 27 bước. Dùng check_all.py --screenshots; persistence/E-learning riêng hoặc run_release.py --verify.
2. Sửa mô tả Web: web-frontend-server là container chính độc lập, cùng hai replica web-frontend-server1/2; không phải alias. Sửa restart policy: thuộc service/container, không thuộc 8 named volume; rà cả hai tài liệu.
3. Bỏ dòng trắng cuối handoff/G01.md đang làm working tree dirty và git diff --check lỗi.
4. Ghi rõ engine chưa kết nối là lần rà soát ban đầu. Codex review hiện đã kết nối Docker 29.0.1 và thấy 17 container Up; chưa chạy lại full suite, không ghi kết quả chức năng mới.

Chạy lại kiểm tra số DAT, link, UTF-8, git diff --check, git diff --check main...HEAD; chỉ stage file của G01. Commit bổ sung với message: docs: correct status review findings

Trả HEAD SHA mới, diff/file thay đổi, lệnh và PASS/FAIL/NOT_RUN; working tree phải sạch. Không sửa runtime/evidence/test, không merge/push main, không làm G02. Không chạm branch/worktree test/review-g01-status của Codex.
```
