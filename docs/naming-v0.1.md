# Tư vấn đặt tên phong thủy V0.1

## Phạm vi

- Menu **Tư vấn đặt tên** dẫn tới `/naming-consulting` trong Customer Portal hiện có.
- Hai chế độ: trẻ em và đổi tên; đổi tên bắt buộc tên hiện tại và loại đúng tên đó khỏi đề xuất.
- Nhập họ/phần tên đệm cố định, giới tính, ngày sinh dương lịch, giờ sinh tùy chọn, nơi sinh và múi giờ IANA. Tư vấn cho người đã sinh, trong phạm vi năm 1900–2100 của Calendar Engine.
- Trả 5–10 tên (mặc định 8), ý nghĩa, hành quy ước, mức phù hợp và giải thích từng tiêu chí.

## Tích hợp thực tế

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
