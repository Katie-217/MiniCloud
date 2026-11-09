# G11 — Bỏ E-learning khỏi dự án đang bàn giao

Yêu cầu người dùng ngày **09/11/2026**: không tích hợp repo E-learning nữa, tập trung Portal MiniCloud và website Blog riêng. **G11 được ưu tiên làm ngay**, trước các task UI tiếp theo. Trạng thái: **CHUA_LAM**; file này là phiếu giao việc, chưa phải kết quả gỡ bỏ.

Codex là leader/tester; Gemini thực hiện và trả branch để nghiệm thu. Đọc `AGENTS.md`, [phạm vi Portal/Blog](../PHAM_VI_CHOT_PORTAL_VA_BLOG.md), [kế hoạch UI](../KE_HOACH_NANG_CAP_GIAO_DIEN.md) và PDF trước khi sửa.

## 1. Mục tiêu và điều không thay đổi

- Bỏ code nhập E-learning/Firebase, giao diện/link demo, cấu hình chạy, test và bước build/publish mặc định của phần không còn dùng. Git history và bằng chứng lịch sử vẫn lưu lại.
- Không còn yêu cầu cài Flutter/Java/Firebase CLI hoặc tài khoản E-learning để chạy bản MiniCloud hiện hành.
- Giữ đủ 9 vai trò bắt buộc: Web, Flask App, MariaDB, Keycloak, MinIO, DNS, Prometheus, Grafana/logging, Gateway/LB. Giữ 3 bài Blog, dữ liệu/schema sinh viên và 2 Web replica của E10.
- Không xóa named volume hoặc dữ liệu cũ. Giữ `.env` hiện có nguyên byte; các khóa ELEARNING cũ trong file ignored có thể để nguyên vì không còn được sử dụng. Gỡ chúng khỏi `.env.example` cho máy mới.
- Không đổi layout Portal/Blog trong G11. Tách frontend vẫn thuộc G10; Blog cards/nội dung thuộc G05; dashboard live/API UX thuộc G06–G08. Không merge prototype UI chưa được Codex duyệt vào branch gỡ bỏ.
- Không truy cập AWS hoặc push sang repo E-learning nguồn. Không xóa image/tag release cũ trên Docker Hub.

## 2. Branch và điểm xuất phát

Tạo **`chore/retire-elearning-demo` từ main mới nhất**, sau khi working tree sạch và mọi thay đổi của Gemini đã được commit đúng branch. Không phát triển tiếp G11 trên `feat/portal-cloud-panel`.

Prototype Portal `616f2e9` là code riêng chưa nghiệm thu; giữ lịch sử của nó, không reset/cherry-pick vào G11. Sau G11, Codex sẽ đối chiếu prototype theo scope mới để tránh đưa lại link E-learning hoặc badge trạng thái viết tĩnh.

Nếu working tree có thay đổi không rõ nguồn gốc, giữ chúng và báo file cụ thể; không tự clean/reset/stash hoặc commit gộp. Giữ author Git đã cấu hình.

## 3. Các điểm phụ thuộc phải xử lý

| Nhóm | File/đường dẫn liên quan | Đầu ra cần có |
|---|---|---|
| Code ứng dụng bỏ dùng | `elearning-web/**`, `firebase-emulator/**` | Gỡ file source được Git quản lý khỏi checkout hiện hành; không tạo thêm bản copy archive trong project. History giữ bản cũ. Không xóa volume hoặc file dữ liệu/đầu ra ignored để ép sạch thư mục |
| Công cụ E-learning riêng | `scripts/build_elearning.py`, `seed_elearning.py`, `check_elearning.py`, `check_elearning_persistence.py` | Gỡ khỏi mã chạy hiện hành; không có import/caller mặc định còn tham chiếu file đã bỏ |
| Compose và Gateway | `docker-compose.yml`, `docker-compose.release.yml`, `api-gateway-proxy-server/nginx.conf` | Không có hai service EL/Firebase và upstream/route `/elearning/`; các route bắt buộc khác giữ đúng hành vi. Volume Firebase cũ không bị xóa trên engine |
| Runner và publisher | `scripts/run_release.py`, `scripts/publish_release.py` | Runner không pull/start/test EL. Publisher không bắt buộc source image EL/Firebase; release metadata chỉ chứa image cần cho stack hiện hành |
| Minh chứng/source inventory | `scripts/capture_evidence.py` và công cụ đang dùng dữ liệu EL | Không còn mục ELM hoặc bắt buộc Dockerfile/provenance/build script của EL. Vẫn render đủ minh chứng core/E01–E10/logging/network/persistence |
| Giao diện | `web-frontend-server/html/**` hoặc Portal source nếu đã có | Gỡ menu/card/CTA/mô tả E-learning; giữ giao diện chức năng đang có. Nhãn số container ghi theo cấu hình; không chuyển “17 Up” giả thành “15 Up” giả |
| Cấu hình mẫu/tài liệu hiện hành | `.env.example`, `README.md`, `HUONG_DAN_TEST_LOCAL.md`, tracker và kế hoạch liên quan | Không hướng dẫn cài/build/login EL; cập nhật số liệu hiện hành theo kiểm tra. Phân biệt lịch sử 17 container/6 image và trạng thái mới |
| Release và bằng chứng | `release-images.json`, `evidence/local/release-images.json`, inventory/lock mới | Candidate mới có manifest/digest thật; không chỉ sửa số đếm. Không xóa/sửa nhãn thời gian của minh chứng lịch sử để biến thành kết quả mới |

Rà thêm bằng `rg` vì danh sách trên không thay cho kiểm tra caller/import. Không xóa mọi chuỗi “E-learning” trong các báo cáo, biên bản và JSON lịch sử; đó là lịch sử có ngày rõ ràng. Báo cáo/video cuối vẫn thuộc G02/G03, không tạo lại nửa chừng trong G11.

Xóa source bằng thao tác Git có scope đúng thư mục đã kiểm tra. Trước thao tác đệ quy, xác minh đường dẫn tuyệt đối chỉ nằm trong các thư mục source chỉ định của repo. Không dùng lệnh shell dựng từ chuỗi để xóa chéo thư mục, không xóa `.venv` hay dữ liệu Docker.

Giữ ignore phù hợp cho artifact build/cache cũ còn trên máy. Không bỏ ignore rồi vô tình stage các file generated/ignored ngoài task; chúng không phải mã ứng dụng còn được triển khai.

## 4. Container cũ và dữ liệu phải được giữ

1. Ghi nhận trạng thái/ID 15 service cần giữ và danh sách volume liên quan trước khi thao tác; không log toàn bộ environment vì có bí mật.
2. Chỉ khi cần chuyển runtime sang bản gọn: xác minh label `com.docker.compose.project=myminicloud` và tên chính xác của `elearning-web-server`, `firebase-emulator-server`.
3. Dừng hai container đó có kiểm soát để Firebase có cơ hội export dữ liệu theo cơ chế hiện có. Có thể loại bỏ container cũ sau khi dừng, **không loại bỏ volume**. Không `down -v`, prune, xóa database hoặc thao tác container ngoài project.
4. Xác minh volume Firebase cũ vẫn tồn tại, và core database/MinIO/Keycloak/Prometheus/Grafana/Loki vẫn giữ dữ liệu. Dữ liệu Firebase giữ lại không được ghi như một volume đang sử dụng trong bản stack gọn.

Dự kiến cấu hình mặc định còn **15 service/container runtime** khi chỉ bỏ đúng hai service và không thêm service khác; lấy số thực tế từ Compose. Không gán cứng 15 rồi bỏ qua lỗi liệt kê hoặc container chưa chạy. Named volume đang dùng dự kiến 7, còn volume Firebase cũ được giữ riêng.

## 5. Bản release phải nhất quán với source gỡ bỏ

Không chỉ xóa service ở base Compose: override release cũ có thể thêm lại service qua merge. Không chỉ xóa link trong source: image Web ghim digest cũ vẫn chứa link cũ.

G11 cần một **release candidate mới** của stack gọn để Codex kiểm thử đúng bản sẽ chạy. Candidate này chưa phải nghiệm thu UI cuối; G09 sẽ phát hành lại sau các task UI.

- Build image thực sự đổi source, đặc biệt Web sau khi gỡ UI E-learning. Image không đổi có thể tái sử dụng nội dung/digest đã kiểm chứng; không build lại MinIO từ đầu chỉ để đổi số container.
- Sửa publisher để bỏ 2 image không còn dùng và yêu cầu version mới rõ ràng; không để mặc định vô tình đẩy đè `local-20261029.1`.
- Candidate gợi ý `local-noelearning-20261109.1`. Kiểm tra tag đã tồn tại trước; nếu có thì chọn hậu tố mới. Không ghi đè tag cũ hoặc `latest`.
- Xác minh quyền Docker Hub bằng thao tác thực tế phù hợp. Có thể push candidate trên namespace `katie217` đã được người dùng chỉ định, rồi đọc lại manifest/digest. Không đưa credential vào log. Nếu thiếu quyền/mạng, ghi NOT_RUN/blocked publish, không bịa digest hoặc tuyên bố release hoàn tất.
- Cập nhật root lock/override và metadata candidate bằng digest registry thật. Theo cấu hình hiện tại, số custom image dùng cho release gọn dự kiến 4: Web/App/MinIO/tools; tools không phải container thường trực. Kiểm tra số thực tế.
- `run_release.py` phải khởi động đúng stack đã gỡ, không kéo lại 2 image/service EL và không in URL E-learning. Blog hiện có thể mở tại `:8080/blog/`; không tuyên bố đã xong tách frontend G10.

Không đổi digest cho một image không build/publish được xác minh. Không xóa các image/release cũ hoặc viết lại lịch sử Git để làm như E-learning chưa từng tồn tại.

## 6. Kiểm tra và minh chứng cần trả

| Kiểm tra | Kết quả cần chứng minh |
|---|---|
| Base + release Compose | Cả cấu hình hợp lệ; service list không có EL/Firebase; đủ core + Web replicas/exporters/logging. Không in config đã expand bí mật để gửi cho nhóm |
| Source/caller/default workflow | Không còn import/build/login/test EL đang được runner mặc định gọi; source EL không còn trong active checkout Git |
| Runtime | Candidate pull/start được; các service cần giữ Running/healthy như khai báo; image ID khớp lock. Hai container cũ đã dừng/loại bỏ có scope; volume cũ vẫn có |
| Core/E01–E10 | Bộ `check_all.py --screenshots` và các kiểm tra bắt buộc giữ assertion; số bước ghi theo runner thật. Hiện baseline là 27 bước, không tính 2 bài EL bổ sung vào số này |
| Persistence/logging | Core5 persistence, logging sau recreate, dữ liệu SQL/MinIO/Auth còn; giữ probe dữ liệu thật, không xóa volume để test đạt |
| UI và routes | Portal/Blog/API/Auth/MinIO/Prometheus/Grafana/LB vẫn hoạt động; không menu/CTA EL. `/elearning/` không còn mở app (404/410 phù hợp), không làm hỏng `/blog/` |
| Evidence renderer | `collect_logs.py`, `capture_evidence.py` chạy được sau khi bỏ ELM; source inventory không phụ thuộc file EL đã xóa |
| Quy trình partner | Hướng dẫn và startup không cần Flutter/Firebase; README không còn yêu cầu tài khoản E-learning. Nêu rõ UI tách website chưa hoàn thành nếu G10 chưa làm |

Lưu kết quả G11 tại `evidence/local/g11-retirement/`: danh sách trước/sau đã lọc bí mật, cấu hình service/volume/image, registry manifests/digest hoặc đường dẫn metadata, lệnh và exit code, ảnh UI, giới hạn chưa test. File trước/sau phải đúng thời điểm kiểm tra, không dựng lại từ giả định.

`R14` vẫn chờ AWS; `R16–R18` vẫn chờ hồ sơ cuối/cloud. Không nâng trạng thái toàn bài vì stack ít container hơn.

## 7. Commit và điểm dừng

Các thay đổi liên quan G11 ở **cùng branch**, mỗi output có commit riêng nếu phù hợp:

- `chore: remove optional elearning integration`
- `test: verify reduced local stack`
- `chore: publish reduced release candidate`

Giữ author, chỉ stage file thuộc task. Không merge/cherry-pick/push main, không sửa prototype Portal khác hoặc làm G05/G10 trong cùng lượt.

Bàn giao task, branch, base/HEAD SHA, danh sách file đổi, source SHA đã build, candidate tag/digest và số service thực tế; bảng lệnh PASS/FAIL/NOT_RUN; minh chứng giữ volume/core data; lỗi/hạn chế và điểm Codex cần review. Sau đó dừng để Codex kiểm thử độc lập.

## 8. Prompt chuyển Gemini

```text
Thực hiện riêng G11: bỏ E-learning/Firebase khỏi dự án MiniCloud hiện hành. Codex là leader/tester.
Workspace: D:\Điện toán đám mây

Đọc AGENTS.md, PHAM_VI_CHOT_PORTAL_VA_BLOG.md và handoff/G11_REMOVE_ELEARNING.md. G11 được ưu tiên làm ngay. Tạo chore/retire-elearning-demo từ main mới nhất, không làm trên feat/portal-cloud-panel và không lấy prototype chưa duyệt vào task này. Giữ thay đổi dở nếu có, không reset/clean/stash.

Gỡ code EL/Firebase được Git quản lý, link/menu và cấu hình service/route, caller/build/seed/test/publish mặc định. Rà Compose base + override, runner, publisher, capture_evidence, .env.example, README và hướng dẫn. Giữ đủ 9 vai trò, E01–E10, SQL/Auth/MinIO/DNS/metrics/logging và hai Web replica.

Không xóa volume hoặc dữ liệu; giữ .env hiện tại nguyên byte. Chỉ dừng/gỡ đúng hai container EL/Firebase đã xác minh thuộc myminicloud. Không đụng project khác/AWS/repo nguồn. Không sửa lịch sử evidence để che việc thay đổi.

Build source thay đổi và phát hành candidate tag mới theo phiếu; verify registry digest thật, không đè release cũ. Stack mới dự kiến 15 runtime service, 4 custom image gồm tools, nhưng phải đếm và test thật. Nếu publish/test không chạy được thì ghi NOT_RUN, không bịa kết quả.

Chạy suite core/E01–E10, persistence/logging và kiểm tra renderer/startup/các giao diện. Không bỏ assertion bắt buộc. Không giữ các nhãn Healthy/Up viết tĩnh từ số cấu hình.

Commit theo phiếu, không merge/push main. Trả base/HEAD SHA, file đổi, source SHA build, tag/digest, số service/volume/image, lệnh/kết quả, đường dẫn evidence và hạn chế. Dừng chờ Codex nghiệm thu, chưa làm G05/G10 hoặc redesign Portal.
```
