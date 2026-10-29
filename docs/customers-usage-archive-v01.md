# Khách hàng, hạn mức và kho hồ sơ — 29/10/2026

## Sử dụng

- Đăng ký thành viên yêu cầu Họ và Tên, số điện thoại, tên đăng nhập và mật khẩu. Số điện thoại chuẩn hóa khoảng trắng/dấu phân cách, chấp nhận 8–15 chữ số và dấu cộng quốc tế; đây không phải xác thực OTP. Tài khoản cũ chưa có số điện thoại vẫn dùng được và hiện Chưa bổ sung. ADMIN có thể cập nhật trong Khách hàng.
- `/admin/customers` quản lý mọi tài khoản vai trò CUSTOMER, cả mới đăng ký và được cấp trước đây; có tìm kiếm, số điện thoại để gọi, xem lượt dùng và sửa hạn mức. `/admin/accounts` chỉ hiện quản trị/nhân sự. Danh bạ nhập tay cũ được giữ trong phần mở rộng của Khách hàng.
- Cùng mức N áp dụng riêng cho bảy loại: lá số, chọn ngày cá nhân, hôn nhân, sinh con, đặt tên, hợp tác, vận hạn. Ví dụ N=31: mỗi loại có 31 lượt riêng, không phải tổng cộng 31 lượt cho mọi loại. Tăng N không xóa lượt đã dùng. Giảm N xuống dưới số đã dùng sẽ chặn tạo mới; để trống là không giới hạn.
- Khi hết lượt, máy chủ chặn trước tính toán và thông báo liên hệ ADMIN. Xem lại, lưu lại hồ sơ đã có, tải kết quả, lịch ngày công khai, phân tích tên hiện tại miễn phí và năng lượng số không trừ lượt tạo mới. Hồ sơ và thời hạn thành viên vẫn theo quyền truy cập hiện có.
- `/profile` có bảng lượt dùng riêng từng loại. `/contact` tiếp nhận yêu cầu hỗ trợ, không gửi email/SMS hoặc gọi điện tự động.
- `/admin/cases` đọc kho hồ sơ thống nhất, lọc theo loại/người tạo/từ khóa. Có kết quả mới và dữ liệu cũ còn đọc được. Kết quả mới tự lưu kể cả khi chưa bấm Lưu trên màn hình. ADMIN xem được hồ sơ của mọi vai trò; người dùng thường không được đọc kho toàn hệ thống.
- Liên hệ website nằm chung mục Hồ sơ tư vấn. Cuộc gọi/trao đổi trực tiếp được ADMIN nhập thủ công tại đây; hệ thống không tự ghi nhận cuộc gọi ngoài website. Có trạng thái Mới tiếp nhận/Đang hỗ trợ/Đã xử lý và ghi chú hỗ trợ.

## Dữ liệu và kiểm soát lượt

Giữ `analysis_limit` làm mức chung cho mỗi loại và giữ nguyên bộ đếm lá số cũ `analyses_used`. Không viết lại hàng loạt `users.json`. Số điện thoại là trường tùy chọn trong hồ sơ lưu để tương thích dữ liệu cũ, bắt buộc ở đăng ký mới. Tạo/cập nhật tự lưu qua kho tài khoản hiện có; sửa hạn mức/điện thoại hoàn tác bộ nhớ nếu ghi thất bại.

Kho SQLite mới `customer_activity.sqlite3` nằm cùng thư mục `users.json` (hoặc `BTE_USAGE_DB_PATH`). Có lượt giữ chỗ, kết quả và mốc đối chiếu số lượt cũ. Hôn nhân/hợp tác/sinh con/vận hạn cũ có chủ tài khoản được đối chiếu khi khởi tạo bộ đếm; hồ sơ chưa xác định chủ vẫn hiện cho ADMIN, không tự gán cho một khách hàng. Dữ liệu chưa từng được lưu trên máy chủ trước đây không thể khôi phục từ việc cập nhật này.

API chính là nơi quyết định hạn mức. Dịch vụ tư vấn riêng giữ chỗ qua API chính rồi hoàn tất/lưu kết quả trong giao dịch SQLite; đồng bộ giữa hai dịch vụ cần cùng khóa nội bộ. Khóa lấy từ `BTE_INTERNAL_SERVICE_SECRET` hoặc tệp `BTE_DATA_DIR/consulting-service.key` được tạo ngẫu nhiên, không gửi ra trình duyệt. Hai tiến trình phải dùng cùng thư mục dữ liệu/khóa. Không đưa tệp khóa, kho tài khoản và SQLite vào gói mã nguồn công khai.

Giữ chỗ ngăn yêu cầu đồng thời vượt hạn mức. Kết quả lỗi trả lại giữ chỗ; yêu cầu cùng mã idempotency và đầu vào trả lại kết quả cũ sau khi đã hoàn tất. Nếu không xác nhận được lưu trữ sau các lần thử, lượt chờ được giữ để không tự mở thêm lượt khi kết quả có thể đã tồn tại. ADMIN có nút giải phóng lượt chờ quá 30 phút; không tự động giải phóng giữa một tác vụ đang xử lý. Chỉ API nội bộ có khóa và tài khoản hợp lệ được hoàn tất lượt. Phù hợp cấu hình hiện tại có một API chính quản lý kho tài khoản JSON.

Kho quản trị ghép bản lưu mới với kho lá số/vận hạn và JSON hôn nhân/hợp tác/sinh con cũ; loại trùng theo chủ/loại/mã hồ sơ. Kết quả mới giữ dấu người tạo từ tài khoản đã xác thực, không tin trường người tạo do khách gửi. Các loại có bộ xuất hiện có tiếp tục dùng PDF/DOCX. Đặt tên, chọn ngày, liên hệ và hồ sơ nhập trước đây có thể mở xem/tải dữ liệu JSON; chưa bổ sung bộ xuất PDF/DOCX mới cho các loại này.

## Giấy phép và quyền tác giả

Màn hình Bản quyền được ghi rõ là giấy phép sử dụng phần mềm cho máy chủ; kích hoạt tại đây không phải đăng ký pháp lý. Không thay đổi giấy phép đang dùng hoặc tự khóa hệ thống khi triển khai.

Nên giữ mã tính toán trên máy chủ do chủ dự án quản lý, hạn chế cấp bản sao nguồn, lưu lịch sử đóng góp/phiên bản và rà soát giấy phép các thành phần trước khi lập hồ sơ đăng ký. Nếu phân phối bản cài cho bên khác, cần thiết kế riêng cơ chế cấp phép có chữ ký số/khóa riêng nằm ngoài bản giao; người có toàn bộ mã nguồn có khả năng sửa hoặc gỡ cơ chế kiểm tra. Không có giải pháp kỹ thuật bảo đảm tuyệt đối không bị sao chép.

Nguồn tham khảo đã tra cứu ngày 29/10/2026:
- [WIPO về bảo hộ và chứng cứ sáng tạo](https://www.wipo.int/en/web/copyright/protection).
- [Bộ hướng dẫn đăng ký quyền tác giả trên môi trường số của Cục](https://cov.gov.vn/quyen-tac-gia-quyen-lien-quan/bo-tai-lieu-huong-dan-thu-tuc-hanh-chinh-ve-dang-ky-quyen-tac-gia-quyen-lien-quan-171084.html).

## Triển khai

Nạp lại API chính, API tư vấn, Portal và Web Admin. Portal chính vẫn ở 8686; quản trị tại `/admin`. Các lối Admin cũ dùng cùng mã cập nhật. Không cần xây dựng React. Ctrl+F5 để lấy tài nguyên mới `customers-04`. Giữ nguyên giá, ngân hàng, thời hạn và hạn mức đã được ADMIN thiết lập; không tự kích hoạt tài khoản chờ thanh toán.

Kiểm thử dùng kho riêng: phone, phân quyền, bảy hạn mức độc lập, gửi đồng thời, hoàn lượt lỗi, idempotency, dữ liệu cũ, lưu liên hệ, sửa hạn mức và đọc kho thống nhất. Có kiểm tra hai tiến trình thực để xác nhận tư vấn đặt tên lần đầu 200 và lần tiếp theo 429, rồi đối chiếu hồ sơ và lượt còn lại.
