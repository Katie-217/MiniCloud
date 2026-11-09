# Nâng cấp Portal, dashboard, API và Blog

Chốt yêu cầu người dùng ngày **09/11/2026**. Codex điều phối và kiểm thử; Gemini thực hiện từng task sau khi người dùng chuyển prompt. Tài liệu này bổ sung phạm vi UI trước đợt hoàn thiện báo cáo/video, không đánh dấu UI mới đã triển khai.

> **Thiết kế mới nhất:** [Portal nền trắng và API Console](DAC_TA_PORTAL_TRANG_API_CONSOLE.md). Nền trắng/chữ đen, sidebar trái, Tổng quan đầu và API Console thứ hai; response chính là terminal sáng. Blog từ repo → image → Nginx, không upload ZIP/CMS. Áp dụng thay lựa chọn nền tối/card kết quả trước đây.

> **Phạm vi chốt mới nhất:** [PHAM_VI_CHOT_PORTAL_VA_BLOG.md](PHAM_VI_CHOT_PORTAL_VA_BLOG.md). Portal là control panel quan sát/kiểm thử; Blog là website demo có frontend riêng, mở từ card ứng dụng sang tab mới. Không nhúng danh sách bài Blog vào Portal. E-learning bỏ khỏi phạm vi demo; G10 tách hai frontend và G11 thu gọn phụ thuộc EL được thêm trước release cuối. Các mốc 17 container dưới đây mô tả release hiện có, không cố định cho bản sau G11.

> **Task ưu tiên đầu:** [G11_REMOVE_ELEARNING.md](handoff/G11_REMOVE_ELEARNING.md). Gỡ app khỏi project hiện hành, giữ Git history/volume; sau khi Codex nghiệm thu mới tiếp tục prototype/Blog/dashboard. Không cần phát triển thêm tính năng E-learning để đáp ứng đề.

## 1. Đối chiếu đề và vai trò E-learning

| Thành phần | Căn cứ / vai trò | Kết luận triển khai |
|---|---|---|
| Home và Blog | PDF trang 1, 12–13: Web server phục vụ index/blog, HTTP 200, nhận diện MyMiniCloud Home/Blog | Portal qua gateway `/`; website Blog riêng qua Web 8080, giữ `/blog/` và 3 file bài theo đề |
| Blog cá nhân | PDF trang 21: ít nhất 3 bài HTML, chủ đề tự chọn; blog1/2/3.html có ảnh, liên kết về trang chính; index có danh sách hyperlink | Giữ đúng các URL, trình bày danh sách bằng card ảnh trái/chữ phải, nội dung học thuật tự biên soạn |
| Dashboard trên Portal | Cải tiến giao diện theo yêu cầu người dùng; yêu cầu monitoring gốc nằm ở R08/R09, E07/E08 | Hiển thị dữ liệu thật từ Prometheus; giữ nguyên dashboard Grafana theo đề |
| Gọi API trên Portal | Cải tiến trải nghiệm kiểm chứng R03/R04 và E02/E03/E04/E09/E10 | Chọn operation/nhập đúng tham số/Execute; kết quả chính là terminal JSON/text, status/ms; bảng là chế độ xem phụ |
| E-learning | Ứng dụng bổ sung từ repo người dùng để minh họa triển khai Flutter Web trên Nginx | Không có mục riêng bắt buộc trong E01–E10; không dùng làm bằng chứng thay Flask/SQL/Keycloak/MinIO |

E-learning đã được tích hợp trong giai đoạn cũ, nhưng người dùng đã chọn không dùng cho bài demo này. Không giữ card/link E-learning trong Portal hoặc phát triển thêm app đó. G11 sẽ tách nó khỏi startup/verify/release mặc định theo quy trình riêng; giữ dữ liệu volume và lịch sử, không xóa để sửa giao diện. Flask/MariaDB/Keycloak/MinIO vẫn thực hiện các yêu cầu đề độc lập.

## 2. Những gì quan sát được trước khi sửa

- Home đã có CSS tối và một số card giới thiệu, nhưng chưa có KPI/biểu đồ live trên Portal; nhãn “100% UP” đang viết tĩnh, không thể coi là trạng thái đo thật.
- Blog index hiện là danh sách `ul/li` với link mặc định, chưa có card/thumbnail/preview; 3 bài hiện rất ngắn.
- Một số link API mở tab JSON; phần tương tác chưa thống nhất loading/error/result. Dữ liệu trả về đang được ghép qua `innerHTML` ở vài chỗ; UI mới cần render dữ liệu bằng text an toàn.
- Ngày 09/11 đã gọi thử Prometheus bằng các query CPU/RAM/network/request-rate: đều có series số thực; job node/web trả up = 1 ở lúc kiểm tra. Đây là quan sát baseline, không phải nghiệm thu dashboard mới.
- Release `local-20261029.1` đang ghim digest. Chỉ sửa source sẽ chưa đổi giao diện trong image chạy; cần build preview và phát hành image mới sau khi Codex kiểm thử.

## 3. Thiết kế cần đạt

### 3.1. Ngôn ngữ giao diện chung

- Canvas/sidebar/card nền trắng, chữ đen, viền xám nhạt; màu chỉ cho số liệu/series/status/method khi cần, kèm label. Không nền slate tối hoặc gradient trang trí.
- Portal có sidebar dọc bên trái, chỉ hiện view đang chọn: Tổng quan, API Console, Xác thực, Lưu trữ, Mạng & DNS, Load Balancer, Dịch vụ, Ứng dụng. Blog có menu/CSS riêng; Portal chỉ có card mở Blog, không có nội dung bài viết hoặc E-learning.
- Bỏ hero/slogan/đoạn giới thiệu dài; giữ label/đơn vị/nguồn đo ngắn/thời điểm/lỗi. Sidebar mobile đóng/mở được và `/#secure-demo` vẫn mở đúng view Xác thực.
- Nội dung chia khu rõ ràng, khoảng cách đều, giới hạn chiều rộng; văn bản thường khoảng 16px, focus bàn phím rõ, label/form dễ hiểu.
- Responsive tối thiểu desktop 1440×900 và mobile 390×844. Không tràn ngang toàn trang; bảng rộng có vùng cuộn riêng nếu cần.
- Dùng HTML/CSS/JavaScript hiện có; không chuyển framework hoặc thêm CDN bắt buộc để mở các trang chính. Biểu đồ có thể dùng SVG/canvas hoặc thư viện đóng gói local.
- Giữ nội dung nhận diện `MyMiniCloud – Home`, `MyMiniCloud – Blog` theo bài kiểm tra; các đường dẫn bắt buộc tiếp tục hoạt động.
- Cổng Web 8080 giữ Home/Blog HTTP 200; chức năng API/metrics dùng gateway cổng 80. Nếu người dùng mở Portal ở cổng tĩnh 8080, hướng dẫn chuyển sang gateway thay vì giả dữ liệu hoặc để lỗi 404 âm thầm.

### 3.2. Dashboard Portal

```text
MyMiniCloud      | Tổng quan                  Cập nhật ... [Làm mới]
> Tổng quan      | [CPU %] [RAM %] [Network B/s] [Web req/s]
  API Console    | [Biểu đồ CPU/RAM] [Biểu đồ Network/Requests]
  Xác thực       | Node: ...   Web: ...    Nguồn đo: Docker VM
  Lưu trữ        | [Grafana] [Prometheus] [Nhật ký]
  Mạng & DNS     |
  Load Balancer  | (Chỉ view đang chọn, không xếp tất cả trên một trang)
  Dịch vụ        |
  Ứng dụng       |
```

KPI phải lấy dữ liệu thật, có đơn vị, mốc cập nhật và trạng thái chờ/lỗi/thiếu dữ liệu. CPU/RAM dùng thang 0–100%, mạng là B/s, request-rate là req/s. Có lịch sử 15 phút với thời gian trên trục; dữ liệu rỗng không vẽ đường 0 giả.

Nguồn đo: CPU/RAM Linux VM Docker Desktop, network của namespace Node Exporter, Web metrics của Web chính. Ghi chú ngắn tại dashboard; không đổi thành đo Windows hay từng container.

“9 vai trò” và “17 container theo cấu hình” là thông tin kiến trúc. Không hiển thị “17 container đang khỏe” từ hai job Prometheus; trạng thái UP chỉ gắn với những target/probe thật đã đo. Các card vai trò không có probe thì mô tả/link, không tự có badge Healthy.

Refresh mặc định khoảng 10 giây, có nút làm mới, không chồng request; khi tab ẩn có thể tạm dừng. Nếu mất kết nối, hiện lỗi/stale và thời điểm lần dữ liệu hợp lệ gần nhất; không tiếp tục tô xanh số cũ như số hiện tại.

### 3.3. Khu gọi API

- Cho chọn operation cố định, hiển thị method/path, form tham số thực sự được backend hỗ trợ và nút Execute. GET dữ liệu hiện không nhận query/body: ghi không có tham số, không dựng input rồi bỏ qua. Không điều hướng sang tab JSON làm kết quả chính.
- Mỗi lần gọi có trạng thái loading, HTTP status, thời gian phản hồi quan sát từ trình duyệt (ms) và thời điểm gọi.
- Kết quả chính là terminal nền sáng/chữ monospace đen, JSON thụt dòng hoặc text response thật. Giữ đúng fields của hello, student, students-db và notes; bảng dữ liệu là chế độ xem phụ, không thay console.
- Đếm số bản ghi từ response, phân biệt nguồn JSON và SQL. Fixture hiện có 5 JSON/3 SQL; không hardcode số dòng để che API lỗi.
- Console có xóa/copy an toàn và vùng cuộn riêng; không in token/credentials. Lỗi HTTP/network/JSON rỗng rõ ràng, không dùng alert làm UI chính; chưa có HTTP response thì không tạo status giả.
- Duy trì form secure sv01/sv02, password masked, xóa password sau submit, token chỉ trong bộ nhớ. Không lưu JWT vào localStorage hoặc đưa token vào log/UI.
- Secure: thành công 200 có thông điệp/username dễ đọc; thiếu token 401 hiển thị là phản hồi bảo vệ mong đợi, không sửa API thành 200. Giữ khả năng kiểm chứng response gốc.
- RR: header/body backend, danh sách request có thời gian; biểu đồ cột đếm phản hồi của từng replica từ các request thật của phiên demo. Chạy tuần tự, giới hạn lịch sử; không tự poll `/lb/` làm nhiễu bài test luân phiên.
- Dữ liệu động dùng `textContent`/DOM an toàn, không ghép response thành HTML chưa xử lý.

Chi tiết operation/form/card công cụ và wireframe tại [đặc tả API Console](DAC_TA_PORTAL_TRANG_API_CONSOLE.md). Tham khảo trải nghiệm Swagger UI, giữ backend Flask; không thêm FastAPI, shell, arbitrary SQL/URL upstream. MariaDB hiện không có Web UI: card chuyển đến thao tác SQL trong Portal, không mở HTTP cổng 3306.

### 3.4. Danh sách và chi tiết Blog

```text
MyMiniCloud – Blog                         [Trang chủ]
Chia sẻ học thuật về điện toán đám mây
┌─────────────────────┬─────────────────────────────────────┐
│ Thumbnail bài 1     │ Chủ đề · thời gian đọc ước tính      │
│                     │ Tiêu đề bài viết                    │
│                     │ Mô tả ngắn 2–3 dòng · Đọc bài →      │
└─────────────────────┴─────────────────────────────────────┘
[Card bài 2 cùng bố cục]
[Card bài 3 cùng bố cục]
```

Desktop: một bài là một card ngang, ảnh bên trái khoảng 220–280px, nội dung bên phải; các card xếp dọc, không chuyển thành lưới ô vuông. Mobile: ảnh trên, chữ dưới. Có hover/focus, ảnh có alt, title/description đủ tương phản. Mỗi bài có **một anchor chính** bọc card để giữ đúng bài kiểm tra index hiện có; không tạo hai hyperlink cùng URL chỉ để ảnh/title đều click được.

Blog nền trắng/chữ đen, menu riêng; không sidebar hạ tầng. Người dùng chọn đóng gói source trong repo và triển khai lên Nginx bằng image/Compose; Portal chỉ có card mở ứng dụng. Không phát sinh upload ZIP/CMS.

Chi tiết là trang riêng theo đúng `/blog/blog1.html`, `blog2.html`, `blog3.html`, không dùng modal thay trang. Có ảnh đầu bài, tiêu đề, tác giả nhóm, các mục h2/h3, đoạn giải thích, ví dụ, kết luận ngắn, liên kết đọc thêm và nút về Blog/Home. Giới hạn cột đọc khoảng 720–800px, line-height thoáng, không để ảnh/text tràn mobile.

Nội dung do Gemini viết mới bằng tiếng Việt, dạng chia sẻ học thuật của sinh viên, khoảng **500–700 từ/bài là mục tiêu biên tập**, không phải số từ bắt buộc trong PDF. Không sao chép nguyên bài nguồn, không bịa số liệu nghiên cứu hoặc nói đã test khi chưa chạy.

| Bài / file | Chủ đề và dàn ý | Ảnh gợi ý |
|---|---|---|
| 1 — blog1.html | **Vì sao ứng dụng nhiều dịch vụ cần mạng riêng?** Tách trách nhiệm Web/App/DB; user-defined bridge và service name; localhost trong container; host port/internal port; ví dụ request qua cloud-net; phân biệt DNS lab và Docker DNS | `network.svg`, có thể chỉnh hình đúng nội dung |
| 2 — blog2.html | **Dữ liệu bền vững trong thế giới container** Container/image/volume; vòng đời dữ liệu; volume và bind mount; ví dụ MariaDB/MinIO; recreate và backup là hai vấn đề khác nhau; bài học thực hành không xóa volume để chữa lỗi | `storage.svg` |
| 3 — blog3.html | **Đọc metrics để hiểu hệ thống đang làm gì** Metrics và logs; CPU/RAM/mạng; counter và rate; Prometheus/exporter/Grafana; đọc biểu đồ có đơn vị/mốc thời gian; giới hạn đo trên Docker Desktop | `metrics.svg` |

Giữ tính chất blog cá nhân/nhóm của Võ Thị Thiên Kim — 521H0092 và Diệp Yến Nhi — MSSV chờ bổ sung; không tự tạo thông tin nhóm mới.

Nguồn đọc thêm chính thức cho kiến thức nền: [Docker bridge networking](https://docs.docker.com/engine/network/drivers/bridge/), [Docker volumes](https://docs.docker.com/engine/storage/volumes/), [Prometheus HTTP API](https://prometheus.io/docs/prometheus/latest/querying/api/), [Prometheus query functions](https://prometheus.io/docs/prometheus/latest/querying/functions/). Nội dung và ví dụ về project phải đối chiếu source thực tế, không suy từ một tài liệu công cụ thành kết quả triển khai.

## 4. Thứ tự giao việc và branch

**Thứ tự hiện hành:** **G11 gỡ EL** → review prototype Portal → G05 → G10 tách frontend → G06 → G07 → G08 → G09 → G02 báo cáo → G03 video → G04 tổng hợp → QA cuối → người dùng duyệt → AWS. G01 đã đạt, không giao lại. Không làm nhiều task song song trong workspace.

| Task | Phụ trách / branch | Output / phạm vi |
|---|---|---|
| G05 Blog card và nội dung học thuật | Gemini, tiếp tục `feat/personal-blog` sau khi fast-forward từ main hiện tại | `html/blog/**`, CSS Blog được scope riêng, kiểm tra/ảnh E01; [phiếu giao G05](handoff/G05_BLOG_CARDS.md) |
| G10 Tách Portal và Blog | Gemini, `feat/separate-portal-blog-sites` | Hai frontend/menu/CSS riêng, Portal qua gateway, Blog Home qua Web trực tiếp; giữ HTTP 200 và các route đề |
| G06 API số liệu Portal | Gemini, branch mới `feat/portal-metrics-api` từ main sau G10 | Flask endpoint cố định `/dashboard` → gateway `/api/dashboard`; test metric response/lỗi; không làm frontend ở task này |
| G07 Dashboard Portal | Gemini, branch mới `feat/portal-health-dashboard` từ main sau G06 | [Phiếu G07](handoff/G07_LIGHT_SIDEBAR.md): nền trắng/sidebar trái, KPI/charts/refresh/card dịch vụ; Tổng quan đầu, API Console thứ hai |
| G08 Giao diện API demo | Gemini, branch mới `feat/api-console-interface` từ main sau G07 | [Phiếu G08](handoff/G08_API_CONSOLE.md): operation/form/Execute/terminal; secure 200/401, RR thật, UI failure states |
| G11 Gỡ bỏ E-learning — ưu tiên đầu | Gemini, `chore/retire-elearning-demo` | Theo phiếu G11: gỡ active source/config/caller; giữ Git history/volume; candidate gọn kiểm chứng thật, không giảm test đề |
| G09 Kiểm thử và image release UI | Codex, `chore/ui-release-images` từ main đã tích hợp G08 | Regression, digest mới, pull/start và cập nhật hướng dẫn chạy; không ghi đè release cũ |

Mỗi task có commit liên quan riêng, summary tiếng Anh 4–5 từ. Ví dụ G05 `feat: redesign academic blog cards`, G06 `feat: expose live dashboard metrics`, G07 `feat: build live portal dashboard`, G08 `feat: improve API demo interface`. Gemini không tự merge/push main hoặc chuyển task tiếp theo.

## 5. Đặc tả giao G06 sau khi G10 đạt

Thêm `GET /dashboard` trên Flask, truy cập từ trình duyệt cùng origin bằng `/api/dashboard`. Flask gọi Prometheus nội bộ `http://monitoring-prometheus-server:9090`; không để frontend gọi trực tiếp cổng 9090 hoặc phụ thuộc iframe Grafana có phiên đăng nhập.

Query cố định/whitelist, không nhận PromQL/URL upstream tùy ý từ client. Query tức thời và lịch sử dùng [HTTP API Prometheus](https://prometheus.io/docs/prometheus/latest/querying/api/) đã có. Mục tiêu lịch sử 15 phút, step 30 giây, số điểm giới hạn. Tái sử dụng requests đã có, timeout và giới hạn thời gian tổng, fail sớm khi Prometheus không kết nối; không chặn `/hello`/healthz vì một request monitoring treo.

| Key dự kiến | PromQL đã thử có series trên stack hiện tại | Đơn vị |
|---|---|---|
| cpu_pct | `100 * (1 - avg(rate(node_cpu_seconds_total{job="node",mode="idle"}[5m])))` | % |
| memory_pct | `100 * (1 - node_memory_MemAvailable_bytes{job="node"} / node_memory_MemTotal_bytes{job="node"})` | % |
| network_rx_bps | `sum(rate(node_network_receive_bytes_total{job="node",device!="lo"}[5m]))` | B/s |
| web_requests_per_sec | `sum(rate(nginx_http_requests_total{job="web"}[5m]))` | req/s |
| targets | `up{job=~"node|web"}` | trạng thái target |

Thống nhất schema để G07 dùng: `status` (ok/partial/unavailable), `queried_at` (UTC), `scope`, `metrics` (key/value/unit/series), `targets` (job/up). Điểm series có timestamp/value. Thời điểm truy vấn không được mô tả thành thời điểm scrape thật nếu không có dữ liệu đó.

NaN/Inf/series rỗng trả `null` kèm trạng thái, không đổi thành 0; CPU/RAM ngoài miền hợp lệ cần báo dữ liệu bất thường, không che bằng số giả. Nếu target down, không tô xanh metric cũ còn trong cửa sổ rate. HTTP 200 cho dữ liệu hợp lệ/partial được giải thích; 503 khi toàn bộ upstream không khả dụng. Không trả stack trace, credential hoặc URL query chứa thông tin nhạy cảm.

Phạm vi G06: app.py/module mới, Dockerfile nếu cần COPY module, script test/ảnh JSON liên quan. Giữ nguyên JSON của `/hello`, `/student`, `/students-db`, `/notes`, `/secure`. Không đổi mạng, cổng, database, Keycloak hoặc mở Docker socket cho Flask. Không thêm cAdvisor/metrics từng container trong task này.

Codex kiểm tra direct/proxy, numeric units/series, so sánh Prometheus cùng thời điểm, thiếu mẫu và upstream lỗi bằng test cô lập/mock; không dừng Prometheus của stack người dùng chỉ để tạo lỗi kiểm thử.

## 6. Tiêu chí nghiệm thu G07/G08

- Kiểm tra trình duyệt desktop/mobile, không chỉ có screenshot đẹp. Nút có label, keyboard focus, loading/error/empty; không lỗi console và không request thất bại bị bỏ qua trong luồng chính.
- Dashboard có 4 KPI thật, đồ thị từ timestamp thật, 2 target đúng trạng thái; mất dữ liệu không thành đường 0. So sánh số với API và Prometheus trong sai số do thời điểm truy vấn.
- API console trả đúng số bản ghi và nguồn; 503/401/network lỗi có giải thích. Thời gian hiển thị được đo thật ở browser, không gán thành latency server.
- Secure vẫn kiểm tra sv01/sv02 và anonymous; giữ label/selector có nghĩa đang được test (`secureForm`, `secureResult`, label tài khoản/mật khẩu) hoặc cập nhật test hành vi tương đương mà không giảm kiểm tra 200/401 và che bí mật.
- RR request tuần tự, header/body khớp, biểu đồ đếm đúng số response đã quan sát; không có poll LB nền làm thay đổi kiểm thử.
- Chạy lại các bài Web, Blog, student API/SQL, gateway, secure portal và round robin liên quan; phần E07/E08 Grafana/Prometheus vẫn đạt.
- Giữ 9 vai trò và cấu hình đã nghiệm thu sau G11; số container/volume theo release thực tế, không cố định 17/8 của baseline. Số theo cấu hình không phải phép kiểm tra health toàn hệ thống.
- Ảnh minh chứng mới có ngày/branch/commit, tách thư mục `evidence/local/ui-portal/` hoặc `ui-api/`; không thay nhãn minh chứng cũ thành một lượt chạy mới chưa có.

## 7. Preview source và phát hành release

Image Web COPY HTML/CSS khi build; sửa file trên host chưa tự đổi Web chạy trong container. Khi Codex giao task UI, Gemini build preview **chỉ các service liên quan**, dùng base Compose, giữ stack/volume khác. Với G05:

```powershell
docker compose -f docker-compose.yml build web-frontend-server
docker compose -f docker-compose.yml up -d --no-deps --force-recreate --wait web-frontend-server web-frontend-server1 web-frontend-server2
```

Các lệnh preview giả định stack và network đang chạy. G06 build/recreate App riêng; G07/G08 build lại ba Web như trên. Kiểm tra `.env` IMAGE_TAG đang dùng trước khi chạy; không tự đổi cấu hình secret.

**Điểm cần nhớ:** trước G09, `run_release.py` vẫn đọc digest release cũ và có thể đưa UI về bản cũ. Không tự sửa digest trong từng task hoặc ghi đè tag `local-20261029.1` để tránh hiện tượng đó. Khi bàn giao task, nói rõ URL đang chạy preview và HEAD source đã build.

G09 thuộc Codex: kiểm thử source đã tích hợp, phát hành tag mới theo ngày thực hiện, đọc lại registry digest, tạo release lock, pull/start đúng image rồi kiểm tra lại. Số bước suite được ghi theo runner thực tế sau khi bổ sung test; không mặc định mọi lượt vẫn đúng 27 bước cũ. Khi release mới ổn định mới chụp báo cáo/quay video và cập nhật tài liệu partner.

## 8. Trạng thái và giới hạn

Các task UI G05–G11 chưa được tính đạt khi mới lập kế hoạch. R/E DAT hiện có vẫn là kết quả của release đã kiểm chứng. Prototype Portal `616f2e9` còn chờ review, không được suy ra UI đã nghiệm thu. G02–G04 chờ sau release UI; AWS vẫn chờ người dùng xác nhận bản local.
