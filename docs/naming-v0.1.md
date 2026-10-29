# Tư vấn đặt tên phong thủy V0.1

## Phạm vi

- Menu **Tư vấn đặt tên** dẫn tới `/naming-consulting` trong Customer Portal hiện có.
- Hai chế độ: trẻ em và đổi tên; đổi tên bắt buộc tên hiện tại và loại đúng tên đó khỏi đề xuất.
- Nhập họ/phần tên đệm cố định, giới tính, ngày sinh dương lịch, giờ sinh tùy chọn, nơi sinh và múi giờ IANA. Tư vấn cho người đã sinh, trong phạm vi năm 1900–2100 của Calendar Engine.
- Trả 5–10 tên (mặc định 8), ý nghĩa, hành quy ước, mức phù hợp và giải thích từng tiêu chí.

## Tích hợp thực tế

### Phân tích tên hiện tại cho khách

Trang `/name-analysis` và menu **Phân tích tên** dùng được khi chưa đăng nhập, có liên kết từ trang chủ và trang tư vấn đặt tên. Khách nhập họ tên, giới tính và năm sinh dương lịch; trang không lưu hồ sơ hoặc yêu cầu tài khoản.

API riêng: `POST /api/v1/public/naming/analyze-current`, chuyển tiếp từ Portal qua `/backend/api/v1/public/naming/analyze-current`. Chỉ endpoint phân tích công khai này được thêm; các endpoint tư vấn/hồ sơ cũ vẫn giữ xác thực.

Phần đọc tên dùng lại danh mục 25 tên và bổ sung `name_words.json` để giải thích các tiếng thường gặp. Hành tên lấy từ tên ghép đã có trong danh mục, hoặc nghĩa của tiếng tên chính nếu đủ cơ sở; không suy ra hành từ họ, không bỏ dấu tiếng Việt khi tra cứu. Từ không biết hoặc đa nghĩa không có hành chắc chắn được báo rõ, không tự phân loại.

Nạp Âm và Cung Phi lấy trực tiếp từ `jiazi_row_for_year` và `personal_cung_phi_from_year_ganzhi` của Calendar Engine theo năm khách nhập. Không tạo ngày/giờ sinh giả, không chạy Bát Tự, Dụng/Hỷ thần hoặc chấm điểm vận mệnh từ năm sinh đơn lẻ. Sinh vào đầu năm cần ngày/tháng để xác minh mốc năm. Các quan hệ sinh/khắc dùng chung quy tắc ngũ hành của phân hệ đặt tên hiện có.

### Tư vấn đặt tên đầy đủ

Portal là FastAPI với HTML/JavaScript thuần cho trang này; không cần build React hoặc thêm thư viện. Luồng:

`/naming-consulting` → `POST /backend/api/v1/consulting/naming/analyze` → consulting API → `POST /api/v1/consulting/naming/analyze`.

Router mới dùng chung tiến trình `consulting.marriage.api.http:create_marriage_api_app`, cùng xác thực hiện có. Portal chuyển tiếp token qua `consulting_session.js`. Chưa đăng nhập nhận HTTP 401. Router không ghi hồ sơ, không sửa cơ sở dữ liệu hoặc kết quả gốc.

`CanonicalOrchestratorAdapter` gọi OrchestratorService đang có. `build_marriage_snapshot` đọc Tứ Trụ, Dụng/Hỷ/Kỵ thần và Nạp Âm trụ năm. Cung Phi và hành cung lấy từ Calendar Engine (`calendar.cung_phi`, `calendar.hanh_cung`), không tính lại bằng năm dương lịch riêng. Nạp Âm được ghi rõ là **Nạp Âm trụ năm BTE**, theo quy ước trụ năm của hệ thống hiện có.

## Quy tắc danh mục và xếp hạng

`consulting/naming/catalog.json` chứa 25 tên tuyển chọn, mỗi hành 5 tên; mỗi giới tính có 15 tên đủ điều kiện. Mỗi tên có mã ổn định, giới tính thường dùng, ý nghĩa và lý do gán hành. Không sinh tên tự do từ AI. Danh mục đã được rà soát về nội dung, tính đầy đủ, trùng lặp và độ phủ cho bản V0.1; **chưa có thẩm định độc lập của chuyên gia phong thủy/ngôn ngữ**.

Hành tên là quy ước biên tập theo hình ảnh/ý nghĩa, không phải kết luận khách quan và có thể khác trường phái. Điểm nội bộ chỉ sắp xếp các tên trong danh mục:

- Trùng Dụng thần: +60; nếu không trùng Dụng nhưng trùng Hỷ thần: +30.
- Trùng Kỵ thần: -100, ưu tiên cảnh báo ngay cả khi cùng hành được công bố trong nhóm Dụng/Hỷ.
- Mỗi tiêu chí Nạp Âm/Cung Phi: tên sinh hành đích +10; đồng hành +6; hành đích sinh tên +2; khắc hai chiều -6. Thiếu dữ liệu: 0 và nêu rõ thiếu.
- Không cộng đồng thời Dụng và Hỷ cho cùng một hành; đồng điểm sắp theo mã danh mục để kết quả ổn định.
- Không quy đổi điểm thành xác suất, độ chính xác hoặc dự báo vận mệnh.

Nếu không biết giờ sinh, adapter hiện có vẫn có giờ nội bộ để chạy. Trang mới **không dùng Dụng/Hỷ/Kỵ thần từ giờ giả định**, không hiện trụ giờ và đánh dấu gợi ý sơ bộ. Kết quả dựa trên Nạp Âm/Cung Phi và ý nghĩa; cần xác minh giờ sinh khi gần giao tiết/ngày/năm.

## Cách chạy

Tại thư mục gốc BTE-Platform, dùng môi trường `.venv` hiện có. Khởi động hoặc khởi động lại các dịch vụ qua bộ chạy BTE đang dùng. Trang mới cần Main API để xác thực, consulting API và Customer Portal:

```powershell
.\.venv\Scripts\python.exe -m uvicorn applications.api.app:app --host 127.0.0.1 --port 8000
.\.venv\Scripts\python.exe -m uvicorn consulting.marriage.api.http:create_marriage_api_app --factory --host 127.0.0.1 --port 8082
.\.venv\Scripts\python.exe -m uvicorn applications.customer_portal.app:app --host 127.0.0.1 --port 8686
```

Mỗi lệnh chạy ở một cửa sổ riêng; không chạy thêm nếu cổng đã được dịch vụ BTE sử dụng. Nếu có cấu hình cổng riêng, giữ cấu hình đó, đặt `BTE_API_BASE_URL` và `BTE_MARRIAGE_API_BASE_URL` tương ứng. Đăng nhập rồi mở đường dẫn `/naming-consulting` trên địa chỉ Portal thực tế. Cổng trên là mặc định đọc từ mã nguồn, không phải giả định về dịch vụ đang chạy.

## Kiểm thử

```powershell
.\.venv\Scripts\python.exe -m pytest tests/consulting/test_naming_consulting.py tests/consulting/test_naming_runtime.py applications/customer_portal/tests/test_naming_consulting.py applications/customer_portal/tests/test_ui01_customer_nav.py applications/customer_portal/tests/test_marriage_consulting.py tests/test_childbirth_consulting.py -q
node --check applications/customer_portal/static/js/naming_consulting.js
```

Phủ kiểm tra danh mục, giới tính, số lượng, xếp hạng, xung đột Dụng/Kỵ, giờ không biết, thiếu dữ liệu, tên hiện tại có Unicode, đầu vào không hợp lệ, xác thực 401, chuyển tiếp API, lỗi kết nối và menu các trang cũ. Kiểm tra runtime thật gồm nam, nữ, ngày nhuận 29/02, giờ 00:00 và không biết giờ. Kiểm tra trình duyệt dùng dữ liệu mẫu và tài khoản giả chỉ trong ứng dụng thử riêng, không dùng tài khoản hoặc hồ sơ thật.

## Giới hạn

Chưa lưu lịch sử, xuất báo cáo, so sánh tên cũ/mới, tự sửa họ tên, đánh giá âm điệu, số nét, tên trùng gia đình hoặc toàn bộ họ tên. Giới tính chỉ là cách dùng thường gặp trong danh mục và đầu vào tính Cung Phi của module hiện có. Nơi sinh chưa được đổi thành tọa độ/giờ Mặt Trời. Năm/ngày gần ranh giới lịch và độ tin cậy của Dụng thần vẫn phụ thuộc module BTE hiện có. Nội dung không cam kết tên làm tăng thành công, tài lộc hay danh tiếng.

## Phân tích tên hiện tại công khai — cập nhật 29/10/2026

Trang `/name-analysis` cho khách nhập họ tên, giới tính và **năm sinh âm lịch đã xác định**. Không cần đăng nhập. Portal chuyển tiếp `POST /backend/api/v1/public/naming/analyze-current` tới consulting API. Không lưu thông tin khách.

Hợp đồng mới dùng `lunar_birth_year` (số nguyên 1900 đến năm âm lịch hiện tại). Kết quả ghi `basis=lunar_birth_year_only`, `year_reference.calendar=vietnamese_lunar_year`. Trường cũ `birth_year` bị từ chối với hướng dẫn tải lại biểu mẫu, tránh diễn giải nhầm năm dương lịch cũ thành năm âm lịch. Năm âm lịch được đưa thẳng vào dữ liệu Can Chi/Nạp Âm và bộ tính Cung Phi theo Can Chi có sẵn; không tạo ngày sinh giả, không đổi quy tắc trụ năm Bát Tự/Lập Xuân ở các module khác.

Chỉ có một năm dương lịch thì không đủ để tự xác định năm âm lịch. Bộ chuyển lịch UTC+7 có sẵn xác nhận 01–28/01/1987 thuộc năm Bính Dần 1986; 29/01/1987 là mùng 1 Tết Đinh Mão 1987. Biểu mẫu nhắc người sinh trước Tết kiểm tra đúng năm âm lịch. Bảng đối chiếu HKO cùng xác nhận mốc 29/01: https://www.hko.gov.hk/en/gts/time/calendar/pdf/files/1987e.pdf (HKO dùng lịch Hong Kong; kiểm tra ngày Việt Nam bằng converter UTC+7 của dự án).

`consulting/naming/han_viet.json` phối hợp `name_library.json` cung cấp diễn giải biên tập cho 197 tiếng và 34 tên ghép, trong đó Thị Dung và Ngọc Huỳnh có bài luận riêng ba đoạn. Có thêm 38 mục họ tham khảo. Các chữ Hán là cách viết **có thể tham khảo**, không xác nhận nguyên tự của tên Quốc ngữ. Thanh, Dương, Bảo, Hồng… có nhiều cách hiểu; các tên thuần Việt được đọc theo nghĩa tiếng Việt. Thị có thêm chữ 氏 để giải thích cách dùng tên truyền thống và được phân biệt với Thi 詩. Tên chưa có dữ liệu chỉ được luận phần nhận diện được, không bịa nghĩa, số nét hay hành mới. Các diễn giải ghép là liên tưởng văn hóa do biên tập, không phải nghĩa từ điển nguyên văn hoặc dự báo tính cách/vận mệnh. Quy ước hành và danh mục gợi ý tên cũ được giữ nguyên.

Nguồn đối chiếu từ vựng tiêu biểu: mục từ 進 (Tiến), 山 (Sơn), 明 (Minh), 翠 (Thúy) trên Wiktionary. Các đoạn luận là nội dung viết mới theo nghĩa ngắn của từ; chưa có thẩm định độc lập của chuyên gia Hán Nôm.

- https://en.wiktionary.org/wiki/進#Vietnamese
- https://vi.wiktionary.org/wiki/山
- https://en.wiktionary.org/wiki/明#Vietnamese
- https://en.wiktionary.org/wiki/翠#Vietnamese

Chạy với hai dịch vụ consulting API (8082) và Customer Portal (8686) như hướng dẫn trên, rồi mở `/name-analysis`. Sau khi thay dữ liệu JSON cần khởi động lại consulting API; tải lại trang để nhận JS/CSS có phiên bản `rich-name-03`. Trang công khai không cần Main API để phân tích; các mục tư vấn riêng vẫn dùng xác thực hiện có.

## Nội dung phân tích tên mở rộng V0.3

`name_words.json` và `han_viet.json` giữ các mục nền, `name_library.json` bổ sung từ, các bài luận tên ghép và chữ tham khảo cho họ. Bộ nạp kiểm tra trùng mục, dữ liệu diễn giải và liên kết từ trong tên ghép. Không gọi AI hoặc tra từ bên ngoài trong lúc khách nhập tên; không gửi họ tên khách cho website tham khảo và không lưu lịch sử tra tên.

Kết quả trình bày tóm tắt nghĩa, phân tách họ/tên đệm/tên chính, luận tên ghép, nghĩa các tiếng, thông tin họ ở phần mở rộng và thanh điệu theo dấu viết. Thanh bằng/trắc được xác định từ Unicode NFD (ngang/huyền là bằng, sắc/hỏi/ngã/nặng là trắc); đây là mô tả nhịp viết/đọc, không chấm điểm cát hung. Giữ riêng Dung/Dũng, Thị/Thi, Huỳnh/Huyền/Quỳnh. Chỉ hỗ trợ một số biến thể chính tả xác định như Thùy/Thuỳ, Thúy/Thuý, Thủy/Thuỷ, Hòa/Hoà; không bỏ dấu để đoán tên.

Khi chưa gán được hành tên, giao diện vẫn trình bày đầy đủ phần nghĩa và dữ liệu năm sinh. Không dùng hai thẻ lỗi đối chiếu hoặc dòng “Chưa xác định hành” làm nội dung chính. API tiếp tục trả element=null và quan hệ unresolved để giữ rõ sự khác nhau giữa hiểu nghĩa tên và gán ngũ hành. Không tự gán Kim cho Huỳnh từ sắc vàng, không gán hành cho Dung từ nghĩa bao dung.

Đối chiếu bố cục tham khảo trang bầu.com do chủ dự án đưa, không sao chép bài luận hoặc số liệu thứ hạng/giới tính của họ. Các đoạn luận BTE là nội dung viết mới; không đưa thống kê phổ biến khi không có bộ dữ liệu tương ứng. Nguồn từ vựng tiêu biểu: mục 容, 黃, 氏, 玉 trên Từ điển Hán Nôm; Huỳnh trên Wiktionary. Danh sách nguồn nằm trong `name_library.json`. Các nghĩa từ điển ngắn được tách với phần liên tưởng biên tập; chưa có thẩm định độc lập của chuyên gia Hán Nôm.

Kiểm thử bổ sung gồm đúng hai tên báo lỗi, 20 tên thường gặp khác, phân biệt từ gần âm, vai trò họ Lương so với tiếng tên Lương, biến thể Unicode, thanh điệu, từ chưa nhận diện và hiển thị an toàn. Bộ dữ liệu hữu hạn, chưa bao quát mọi tên địa phương/tên nước ngoài; khi có chữ gốc hoặc ý người đặt tên khác, cần ưu tiên thông tin ấy.
