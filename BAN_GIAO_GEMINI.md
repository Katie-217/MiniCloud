# Bàn giao Gemini — Codex điều phối và kiểm thử

Ngày rà soát nền tảng: **02/11/2026**, bổ sung yêu cầu giao diện **09/11/2026**. Workspace: `D:\Điện toán đám mây`. Repo: `Katie-217/MiniCloud`.

> **Giao ngay G11 theo yêu cầu mới nhất 09/11:** [Bỏ E-learning khỏi project hiện hành](handoff/G11_REMOVE_ELEARNING.md), giữ Git history và dữ liệu volume. Sau nghiệm thu G11 mới review prototype Portal → G05 → G10 → G06 → G07 → G08 → G09 → G02/G03/G04 và QA cuối. [Phạm vi Portal/Blog](PHAM_VI_CHOT_PORTAL_VA_BLOG.md) giữ nguyên: Portal quan sát/kiểm thử, Blog website riêng; không làm Docker admin. G01 đã đạt. Các kết quả nền tảng dưới đây là lịch sử, chưa tính chức năng mới đạt.

## 1. Phân công và nguyên tắc tích hợp

- **Codex (leader/tester):** đối chiếu đề, quyết định phạm vi, review diff, chạy kiểm thử độc lập, kiểm tra minh chứng và tích hợp branch đạt vào main. Ghi rõ PASS/FAIL/NOT_RUN, không coi một lời báo “đã xong” là nghiệm thu.
- **Gemini (thực hiện):** chỉ làm task được giao; viết/sửa code hoặc tài liệu, tự chạy kiểm tra phù hợp, commit trong branch task rồi trả kết quả cho Codex. **Không tự merge/cherry-pick/push vào main, không tự chuyển sang task tiếp theo.**
- **Người dùng:** chuyển prompt và kết quả giữa hai bên, kiểm tra giao diện bản cuối; quyết định thời điểm bắt đầu AWS và bổ sung MSSV Diệp Yến Nhi khi có.

Làm tuần tự theo ưu tiên hiện hành ở đầu file; Codex nghiệm thu và tích hợp mỗi task trước khi giao task kế tiếp. Không để hai công cụ cùng sửa workspace hoặc chạy Compose/test làm recreate đồng thời. Mỗi task bắt đầu từ main đã tích hợp task trước; dùng branch riêng. Với G05, tiếp tục branch E01 `feat/personal-blog` sau khi đưa lên main hiện tại bằng fast-forward. Không đưa sửa runtime vào branch tài liệu.

Không yêu cầu người dùng duyệt từng thao tác Git thông thường. Gemini chỉ dừng ở điểm bàn giao để Codex review theo quy trình này. AWS vẫn là cổng riêng, cần người dùng xác nhận local trước.

## 2. Trạng thái đã kiểm tra

Baseline triển khai và minh chứng đã commit vào main: **`fefd263` — `test: verify pinned local delivery`**. Commit tài liệu bàn giao sau baseline không phải một lượt kiểm thử runtime mới.

Biên bản rà soát có cấu trúc: [handoff-audit-20261102.json](evidence/review/handoff-audit-20261102.json). File ghi riêng kết quả lịch sử, tình trạng engine hôm nay và các branch local chưa có trên remote lúc kiểm tra.

| Nhóm | Kết quả có căn cứ | Giới hạn / việc còn lại |
|---|---|---|
| R01–R13 và R15 | 14/18 nhóm đang DAT trong bảng; chức năng cơ bản local đã có minh chứng | Không tính đây là điểm chấm hoặc toàn bộ đề đã hoàn thành |
| E01–E10 | 10/10 dòng DAT, có JSON/ảnh và branch chức năng | Dùng kết quả 29/10; không ghi đã chạy lại 02/11 nếu chưa chạy |
| Kiểm thử | `local-suite.json`: 27 bước đạt; log `final-verification-20261029.log` | Các bài persistence/E-learning riêng nằm ngoài 27 bước này |
| Release | `local-20261029.1`; 17 runtime image ghim digest, 6 custom image gồm tools | `release-pull-startup.json` ghi 17 image ID khớp; chưa chứng minh chạy trên máy sạch/EC2 |
| Persistence | Core5, Firebase và Loki đã có kết quả sau recreate | 8 volume cấu hình; Alloy positions chưa có bài test resume riêng |
| E-learning | Source main `9e9ebd539c7f08092ea6855c9aceafe645bd28e0`; hai vai trò, khóa học, số ghi danh/F5, dữ liệu emulator | Không thay Flask/SQL/Keycloak/MinIO; chưa xác nhận mọi chức năng repo gốc |
| Runtime hôm nay | `docker info` và `docker compose ps` không kết nối được pipe Docker Desktop Linux engine | **NOT_RUN cho kiểm thử runtime 02/11**; không kết luận là regression ứng dụng |
| R14 / cloud | Chưa triển khai AWS theo yêu cầu người dùng | Không tạo/truy cập tài nguyên AWS; không đổi R14 thành DAT |
| R16–R18 | Có báo cáo/video/ảnh local nhưng cần đồng bộ bản cuối, cloud còn thiếu | Giữ CHO_KIEM_THU cho output tổng thể, ghi riêng trạng thái local |

Các lỗi/hở hồ sơ quan sát trực tiếp:

1. `KE_HOACH_HOAN_THIEN_LOCAL.md` và `TIEN_DO_OUTPUT.md` còn đoạn 0/10, chưa nhập E-learning, 10 container… mâu thuẫn với bảng/JSON đã cập nhật.
2. Báo cáo Markdown còn **13 container**, **5 dòng SQL** (thực tế 3), image Web 1.0.0; chỉ có **1 ảnh nhúng** là sơ đồ. Chương 4 cần ảnh minh họa mỗi server theo PDF trang 3, không chỉ liệt kê tên ảnh.
3. `scripts/record_demo.py` còn caption 13 container, chưa có cảnh E-learning/logging/form API bảo vệ, và tự đặt R17 DAT dù cloud chưa làm.
4. `TONG_HOP_OUTPUT_LOCAL.md` chưa tồn tại. Một số branch chức năng chỉ có local, cần leader kiểm tra việc công bố branch trước bàn giao cuối.
5. README nháp trước đó bị lỗi mã hóa; Codex đã sửa UTF-8 trong đợt bàn giao này và giữ hướng dẫn `HUONG_DAN_TEST_LOCAL.md`. Đây không phải sửa runtime.

## 3. Các điều phải giữ nguyên

- Đọc `AGENTS.md`, PDF và bảng đối chiếu trang trước khi sửa. Nếu mẫu mâu thuẫn, ghi căn cứ và cách điều chỉnh, không bỏ yêu cầu để dễ test.
- Giữ 9 vai trò và 17 container của release hiện tại, service names, `cloud-net`, routes/cổng/volume. Không đổi kiến trúc, thêm MongoDB hay thay hệ thống Auth để quay demo cho thuận tiện.
- Giữ dữ liệu, `.env` hiện có và author Git. Không `down -v`, prune, reset/clean/stash bừa, force push, sửa global SDK/cache hoặc tác động container ngoài project.
- Không dùng dữ liệu Firebase thật, không push sang repo E-learning nguồn. Không ghi mật khẩu, token, private key, URL ký có token vào Git, ảnh, video hay log.
- Dùng PowerShell và `curl.exe`; ghi file **UTF-8**. PowerShell pipe sang Python có thể làm hỏng tiếng Việt; kiểm tra nội dung thực tế sau khi ghi.
- Không sửa/bỏ assertion để test xanh, không bịa timestamp/HTTP status/log/ảnh, không thay test lỗi bằng dữ liệu mẫu.
- CPU/RAM = Linux VM Docker Desktop; network = namespace Node Exporter. DNS 10.10.10.x = bản ghi lab, không phải Docker IP thực. Không cam kết điểm chấm, không ghi 17 Prometheus target khi chỉ có job node/web.
- Nhi chưa có MSSV, ghi chờ bổ sung; avatar chữ K đã được người dùng chọn. Hai việc này không chặn task kỹ thuật local.

## 4. Task G01 — Đồng bộ trạng thái và kế hoạch

**Branch mới:** `docs/reconcile-local-status` từ main. **Commit gợi ý:** `docs: reconcile current local status`.

**File được sửa:** `TIEN_DO_OUTPUT.md`, `KE_HOACH_HOAN_THIEN_LOCAL.md`. Có thể thêm `handoff/G01.md` cho bản bàn giao. Không sửa runtime, test script, report/video hay bằng chứng 29/10.

**Cách làm:**

1. Đối chiếu bảng R/E, các JSON, Git log/branch và cấu hình release; phân biệt lịch sử và trạng thái hiện tại.
2. Bỏ mâu thuẫn trong phần trạng thái hiện hành: 14/18 nhóm tổng thể DAT, 10/10 mở rộng theo kiểm thử đã lưu; 17 container/9 vai trò, 6 custom image, release ghim digest; E-learning/logging đã tích hợp. Không xóa nhật ký cũ có ngày rõ ràng.
3. Cập nhật FIX-005 theo commit `1f27f82`: `git show 1f27f82:evidence/local/E10-round-robin.json` có `details.verified_after_replica_recreation: true`. File hiện tại ở `fefd263` ghi trường này `false` vì lượt sau chỉ test thường. Dẫn riêng commit có test recreate; không sửa false thành true hoặc gán kết quả một lần chạy cho lần khác.
4. Đổi kế hoạch sang phần việc còn lại G01–G04 và QA; giữ mapping E01–E10, branch theo chức năng và thứ tự local trước AWS. Tách công việc đã làm khỏi task chưa làm.
5. Không ghi hồ sơ local cuối đã xong: report/video còn task G02/G03, tổng hợp G04. Ghi runtime 02/11 chưa kiểm thử vì engine không sẵn sàng, không phủ định kết quả lịch sử 29/10.

**Nghiệm thu Codex:** đếm dòng DAT đúng 14 R / 10 E; R14 chờ, R16–R18 CHO_KIEM_THU; không còn trạng thái hiện hành 0/10/10 container; link/file/commit đúng; diff chỉ trong phạm vi; UTF-8 và `git diff --check` đạt. Có thể làm G01 khi Docker chưa chạy.

## 5. Task G02 — Báo cáo cuối đúng bản release

**Branch mới:** `docs/refresh-local-report` từ main sau G01. **Commit gợi ý:** `docs: refresh final local report`.

**File được sửa:** `report/BaoCao_Local_521H0092.md` và HTML/PDF/DOCX sinh từ nó; `report/architecture.svg/.png`; `scripts/build_report.py` nếu cần để tạo đúng output. Chỉ cập nhật dòng R16/E05 của tracker khi có kết quả liên quan; bằng chứng build/report/E05 do kiểm tra thực tế sinh ra. Không sửa cấu hình runtime hoặc release digest.

**Đầu ra bắt buộc:**

- Đủ 5 chương và phụ lục theo PDF trang 3: mục tiêu; kiến trúc/network/request flow; Dockerfile/Compose/config với đoạn code thực tế đã bỏ bí mật; demo/kiểm thử có ảnh mỗi vai trò server; đánh giá/khó khăn/hướng mở rộng.
- Kiến trúc đúng **17 container / 9 vai trò / 8 volume**, gồm 2 Web replica, exporter, E-learning/Firebase, Loki/Alloy. Phân biệt host port/internal port.
- Kết quả đúng 27 bước với `--screenshots`, 5 sinh viên JSON / 3 sinh viên SQL, token hợp lệ/từ chối, public avatar K/private PDF, DNS lab, Web metrics, dashboard cá nhân, round robin, E-learning và logging. Không trình bày 22 bước cũ như lượt cuối.
- Nhúng ảnh thật đọc được cho Web, App/API, SQL, Keycloak realm/client, MinIO, DNS, Prometheus, Grafana/logging, Gateway/RR; thêm ảnh hai vai trò E-learning và API bảo vệ. Không chỉ ghi tên file. Không dùng ảnh cũ để minh họa một trạng thái mới chưa chụp.
- Phụ lục có link GitHub, 6 image Hub/tag/digest, video và log. URL dự kiến của video: `https://raw.githubusercontent.com/Katie-217/MiniCloud/main/report/Demo_Local_521H0092.webm`; ghi chờ xác minh nếu chưa kiểm tra được. Không bịa link đã public.
- Ghi rõ giới hạn monitoring, repo E-learning, bản local/cloud, MSSV Nhi còn thiếu. Không ghi đã sẵn sàng deploy cloud hoàn toàn khi script đang hardcode localhost.

**Kiểm tra:** chạy `build_report.py`; mở PDF/DOCX/HTML, xác nhận đủ chương, ảnh có trong PDF và DOCX, không tràn/mất chữ. Chạy `check_profile_storage.py` sau khi PDF cuối đổi để upload documents và xác minh SHA256 file tải về khớp PDF hiện tại. Nếu Docker chưa chạy: ghi NOT_RUN bước upload, không tuyên bố E05/PDF mới đã đồng bộ. Việc upload MinIO chỉ đi `localhost:9000`, không phải AWS.

**Nghiệm thu Codex:** review nội dung với source/PDF đề; kiểm tra artifacts bằng parser và nhìn trang mẫu; kiểm tra hash PDF trong MinIO độc lập khi engine có; R16 tổng thể vẫn CHO_KIEM_THU vì cloud chưa có.

## 6. Task G03 — Video local theo hệ thống hiện tại

**Branch mới:** `docs/refresh-local-video` từ main sau G02. **Commit gợi ý:** `docs: refresh complete local walkthrough`.

**File được sửa:** `scripts/record_demo.py`, `report/Demo_Local_521H0092.webm/.html`, `evidence/local/demo-chapters.json`, bằng chứng playback mới; chỉ dòng R17 của tracker. Không sửa code ứng dụng để dàn dựng kết quả.

**Đầu ra:**

- Video xem được, chú thích đúng **17 container/9 vai trò**, thể hiện đủ các nhóm server và E01–E10 qua UI hoặc kết quả lệnh thực tế; riêng SQL/DNS/network/persistence có thể quay trang minh chứng đã ghi đúng thời điểm.
- Cảnh rõ: Portal/3 bài blog, 5 JSON và 3 SQL, realm/user/public client, form secure trả 200 đúng user rồi 401 khi thiếu token, MinIO avatar K/PDF, Prometheus UP, Grafana 3 panel có dữ liệu, log HTTP thật, RR hai backend, E-learning hai vai trò/khóa học.
- Không quay ô mật khẩu đang có giá trị hiển thị, JWT, cookie/session hoặc trang lỗi/spinner làm minh chứng đạt. Đợi dữ liệu thật tải xong; không dùng sleep để giả lập thành công.
- Sửa script giữ **R17 CHO_KIEM_THU** cho toàn đề, ghi local video đã có và cloud pending. Không hardcode độ dài/số cảnh theo video cũ; sinh chapter JSON theo cảnh thực sự quay.
- Kiểm tra playback bằng trình duyệt: metadata hợp lệ, duration > 0, phát được tới giữa/cuối; trả dung lượng, duration và số cảnh thực tế. Kiểm tra link public sau khi leader tích hợp/push, không tự push main.

**Nghiệm thu Codex:** xem video/metadata, đối chiếu cảnh với runtime/evidence, không lộ bí mật; kiểm tra các assertion trong script không bị nới lỏng. Docker engine phải sẵn sàng để quay UI runtime mới.

## 7. Task G04 — Tổng hợp bàn giao cho người dùng

**Branch mới:** `docs/local-output-handoff` từ main sau G03. **Commit gợi ý:** `docs: summarize final local outputs`.

**File được sửa:** tạo `TONG_HOP_OUTPUT_LOCAL.md`; cập nhật `README.md`, `HUONG_DAN_TEST_LOCAL.md`, `TIEN_DO_OUTPUT.md`, `KE_HOACH_HOAN_THIEN_LOCAL.md` để cùng phản ánh kết quả Codex đã nghiệm thu. Không tự đổi baseline test thành ngày mới.

**Nội dung:**

- Bảng output đã đạt / cần fix / chưa làm / phụ thuộc người dùng, có branch/commit/lệnh test/minh chứng. Dẫn đến PDF/DOCX/video/Hub và hướng dẫn kiểm tra từng giao diện.
- Hướng dẫn từ môi trường mới dùng image release không cần Flutter; phân biệt chạy lần đầu `run_release.py --verify` và mở lại `run_release.py`. Chỉ ghi “đã thử trên máy sạch” nếu có test riêng thật.
- Bảng URL/tài khoản chỉ ghi tên khóa `.env`, không mật khẩu. Hai vai trò E-learning dùng browser profile tách biệt; 401/403 mong đợi không bị báo nhầm là lỗi.
- Chốt số trang PDF, duration/số cảnh video theo bản mới nếu có ghi; không giữ số liệu 18 trang/75 giây/14 cảnh cũ khi chưa xác minh.
- Ghi rõ chưa triển khai EC2, chưa có public IP và hồ sơ cloud; MSSV Nhi bổ sung sau. Không tự tạo deadline/điểm chấm bảo đảm.

**Nghiệm thu Codex:** toàn bộ file/link local tồn tại, UTF-8 đúng, không mâu thuẫn số liệu; không lộ bí mật; bảng cuối chỉ dùng bằng chứng thực tế. Sau đó mới chạy QA cuối và mời người dùng test giao diện.

## 8. Kiểm thử và quy trình leader nhận branch

Mỗi lần Gemini trả kết quả, Codex làm:

1. Ghi branch, base SHA, HEAD SHA; kiểm tra working tree và `git diff --name-status main...<branch>`. Không merge nếu lẫn file ngoài task.
2. Review diff và `git diff --check`; xác minh không sửa yếu assertion, không hardcode token/data nhằm che API lỗi; kiểm tra bí mật mà không in giá trị.
3. Chạy kiểm tra tương ứng task. Với tài liệu thuần túy, kiểm tra cấu trúc/link/ảnh thay vì tạo unit test hình thức. Runtime engine chưa có thì ghi NOT_RUN và giữ kiểm tra phụ thuộc ở hàng chờ.
4. Nếu đạt, Codex tích hợp branch vào main theo lịch sử hiện có, không force. Nếu lỗi, trả task sửa đúng branch, chỉ rõ expected/actual/log. Không yêu cầu Gemini tự giải quyết conflict bằng cách bỏ thay đổi khác.
5. Chỉ giao task kế tiếp khi task hiện tại đã tích hợp. Khi chạy test độc lập tạo lại evidence/tracker, Codex giữ các artifact đó trên branch QA, không trộn với patch Gemini đang viết.

**QA cuối thuộc Codex**, branch `test/final-local-handoff` từ main cuối:

```powershell
docker info
.venv/Scripts/python scripts/run_release.py --verify
.venv/Scripts/python scripts/collect_logs.py
.venv/Scripts/python scripts/capture_evidence.py
```

Runner gồm 27 bước khi có screenshots, core persistence, hai vai trò E-learning, Firebase persistence và logging sau Loki recreate. Xem implementation hiện tại trước khi kết luận coverage. Kiểm tra thêm image ID runtime khớp `release-images.json`; PDF MinIO hash khớp file cuối; RR sau recreate nếu thay đổi có liên quan. Không lặp full suite vô ích sau chỉnh câu chữ.

Các kết quả phải chứng minh: Home/Blog/API/SQL/Auth/Storage/DNS/metrics/log/gateway đạt; E01–E10 không hồi quy; đủ 17 thành viên cloud-net; volume không bị mất; video/report/source/link thống nhất. So sánh container ngoài project trước/sau, không tác động chúng. Theo dõi giới hạn kiểm chứng thay vì hứa không có mọi lỗi ngoài luồng đã thử.

Codex kiểm tra branch chức năng nào chưa có remote và push branch tương ứng bằng lệnh thông thường nếu được; không force và không push sang repo nguồn. Chỉ phát hành image mới nếu sửa runtime cần rebuild; không ghi đè tag release cũ bằng nội dung khác.

## 9. Prompt dùng cho Gemini

G01 đã nghiệm thu. **Prompt cần gửi Gemini ngay là G11**, tại [G11_REMOVE_ELEARNING.md](handoff/G11_REMOVE_ELEARNING.md), mục 8. Không giao đồng thời G05/G10. Phiếu Blog vẫn giữ cho lượt sau: [G05_BLOG_CARDS.md](handoff/G05_BLOG_CARDS.md). Mẫu dưới đây là quy tắc chung; dùng đúng phiếu của task đang được giao:

```text
Bạn là người thực hiện task cho dự án MyMiniCloud; Codex là leader và tester độc lập.

Workspace: D:\Điện toán đám mây
Repo: https://github.com/Katie-217/MiniCloud
TASK_ID: G11

Đọc AGENTS.md, BAN_GIAO_GEMINI.md, KE_HOACH_NANG_CAP_GIAO_DIEN.md và phiếu giao task. Chỉ làm TASK_ID được giao theo phạm vi file, đầu ra và tiêu chí nghiệm thu; không thực hiện toàn bộ kế hoạch một lượt.

Kiểm tra git status, branch và SHA trước khi sửa. Nếu còn thay đổi dở không thuộc bạn, không reset/clean/stash hoặc commit gộp. Bắt đầu từ main mới nhất đã tích hợp task trước, theo branch mới/branch chức năng được chỉ định trong phiếu, giữ author Git. Không tự merge/cherry-pick/push vào main. Mỗi output liên quan một commit, message tiếng Anh dạng type: summary với 4–5 từ sau tiền tố; chỉ stage file thuộc task. Không chạy script tự động commit/merge main.

Đã có baseline fefd263, 27 bước local đạt ngày 29/10, 10/10 mở rộng, release local-20261029.1 gồm 17 runtime image và 6 custom image. G01 đã đạt sau đó. Đây là kết quả lịch sử, không phải kết quả UI mới. Xác minh engine tại lúc chạy test, không bịa timestamp/trạng thái. Image source preview và digest release cũ khác nhau; đọc kỹ quy trình build preview trước khi chạy.

Giữ nguyên runtime, cloud-net, route/cổng/volume và release digest, trừ khi task chỉ rõ được sửa. Không down -v/prune/xóa dữ liệu, tác động container ngoài project, dùng Firebase/database thật hoặc truy cập AWS. Không in/commit mật khẩu, token hay key. Avatar chữ K; MSSV Diệp Yến Nhi chờ bổ sung, không chặn kỹ thuật. Dùng PowerShell, curl.exe và kiểm tra file UTF-8 thực tế.

Chạy kiểm tra phù hợp, giữ assertion, không bịa log/ảnh/kết quả. Nếu có lỗi ngoài scope, báo expected/actual và đề xuất task riêng; không sửa lan rộng. Không đổi số liệu thành mock hoặc sửa test yếu đi để UI đạt.

Kết thúc bằng: task + branch + base/HEAD SHA; source HEAD đã build preview; file thay đổi; output đã làm; bảng lệnh kiểm tra với PASS/FAIL/NOT_RUN và evidence; hạn chế/chưa làm; commit; điểm Codex cần review. Sau đó dừng chờ Codex nghiệm thu, không làm task kế tiếp hoặc tự merge main.
```

Chỉ đổi TASK_ID và phiếu giao sau khi Codex đã nghiệm thu/tích hợp task trước. Khi Gemini trả kết quả, gửi lại Codex **branch/SHA, danh sách file và kết quả kiểm tra** để leader review trên source thật. G02/G03/G04 vẫn theo tiêu chí cũ nhưng chờ UI release G09.
