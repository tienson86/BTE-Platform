# Menu và thành viên trả phí V0.1 — 29/10/2026

## Trải nghiệm sử dụng

Thanh đầu luôn có ba công cụ miễn phí: Trang chủ (ngày giờ tốt/xấu), Phân tích tên, Xem Năng lượng số. Không cần đăng nhập để dùng ba công cụ này.

Sau khi dịch vụ xác nhận phiên đăng nhập, cột trái dưới logo hiện bảy mục theo thứ tự: Xem lá số, Chọn ngày tốt, Tư vấn hôn nhân, Tư vấn sinh con, Tư vấn đặt tên, Tư vấn hợp tác, Tính vận hạn. Tài khoản mới chưa được duyệt vẫn thấy không gian thành viên sau đăng nhập; mở công cụ tính phí sẽ dẫn về trạng thái đăng ký. Máy chủ kiểm tra quyền trước tính toán, đọc hồ sơ hoặc xuất tài liệu. Menu ẩn không thay thế kiểm soát quyền ở API.

`/membership` là trang đăng ký và xem trạng thái. `/admin-membership` là trang dành cho tài khoản có vai trò ADMIN, liên kết trong phần cuối cột trái. Các tài khoản cũ giữ quyền, hạn mức và dữ liệu hiện có. Không tự đổi vai trò tài khoản cũ.

## Cấu hình ban đầu

Chủ dự án cung cấp ngân hàng SHB, số tài khoản 28676875, chủ tài khoản Nguyễn Tiến Sơn. Các giá trị này xuất hiện sẵn trong biểu mẫu quản trị. Cấu hình đã lưu được đọc từ `BTE_DATA_DIR/membership_settings.json`, có ưu tiên hơn giá trị mặc định trong mã nguồn.

Chưa tự đặt mức phí, thời hạn hoặc mở thu phí. Quản trị viên cần nhập mức phí VNĐ, số ngày sử dụng, tùy chọn hạn mức tạo lá số, kiểm tra thông tin nhận tiền, đánh dấu Mở đăng ký rồi Lưu cấu hình website. Khi chưa cấu hình đủ, trang công khai ghi Đang cập nhật biểu phí và không nhận đăng ký trả phí. Có thể cấu hình tiêu đề, giới thiệu trang thành viên, hướng dẫn chuyển khoản và thông báo chung trên website ngay tại trang này. Nội dung là văn bản thuần, không chạy HTML/script.

## Quy trình chuyển khoản và duyệt

1. Khách nhập **Họ và Tên**, tên đăng nhập và mật khẩu. Tài khoản mới luôn có vai trò CUSTOMER, trạng thái pending, chưa có quyền công cụ tính phí.
2. Nội dung chuyển khoản là **họ và tên + dấu cách + tên đăng nhập**, ví dụ `Nguyễn Văn An an123`. Giữ tiếng Việt có dấu và đúng tên đăng nhập; chuẩn hóa Unicode và khoảng trắng. Nội dung được lưu theo đăng ký, không đổi khi tên hiển thị được sửa về sau. Mức phí, thời hạn, hạn mức và ngân hàng cũng được giữ theo cấu hình tại thời điểm đăng ký.
3. Khách chuyển khoản và bấm Tôi đã chuyển khoản. Đây chỉ là thông báo để đối chiếu, không tự kích hoạt quyền.
4. Quản trị viên kiểm tra giao dịch thật, đúng nội dung chuyển khoản và số tiền. Tích xác nhận đã đối chiếu, rồi bấm Xác nhận đã nhận tiền và mở quyền. Chỉ API dành cho ADMIN mới thực hiện được bước này.
5. Thời hạn bắt đầu từ lúc duyệt. Khách kiểm tra lại trạng thái hoặc tải lại trang, sau đó sử dụng các công cụ và tải tài liệu được từng module hỗ trợ. Không nhận tài khoản ADMIN hoặc quyền tải hồ sơ của người khác.

Mỗi mã chỉ được duyệt một lần. Yêu cầu lặp không cộng thêm ngày hoặc lượt. Khi hết hạn, quyền công cụ tính phí bị chặn theo dữ liệu máy chủ, dù token cũ còn hiệu lực. Gia hạn tự phục vụ, nhiều gói, hoàn tiền và tự đối soát ngân hàng chưa thuộc V0.1; khách liên hệ quản trị để xử lý tiếp. Không có giao dịch thanh toán trực tuyến hoặc tự trừ tiền.

Mã đăng ký BTE chỉ dùng nội bộ: không hiển thị trên trang hoặc phản hồi API dành cho khách. Trang quản trị có cả mã nội bộ và nội dung chuyển khoản để đối chiếu; yêu cầu duyệt vẫn kiểm tra mã nội bộ để tránh xử lý nhầm hồ sơ. Đăng ký cũ chưa có nội dung mới sẽ hiển thị họ tên và tên đăng nhập khi tải lại, không cần sửa hàng loạt kho tài khoản. Quản trị vẫn thấy **Nội dung chuyển khoản trước đây** để nhận diện khách đã chuyển theo mã BTE. Khi khách gửi thông báo chuyển khoản hoặc quản trị duyệt, hệ thống lưu cả nội dung mới và nội dung cũ; xem trạng thái đơn thuần không ghi dữ liệu. Khách đã chuyển theo hướng dẫn cũ không cần chuyển lại.

## Lưu trữ và quyền

Tái sử dụng kho `users.json`, bộ băm mật khẩu và JWT của dự án. Thêm trường membership tùy chọn: tài khoản cũ không có trường này được coi là tài khoản hiện có; tài khoản mới có hồ sơ pending/active/rejected và thời hạn rõ ràng. Không lưu mật khẩu thô. Cấu hình được ghi tệp tạm, fsync và thay thế nguyên tử; cập nhật thành viên dùng khóa kho tài khoản hiện có và hoàn tác bộ nhớ nếu lưu thất bại. Phù hợp mô hình một tiến trình API đang dùng; chưa hỗ trợ nhiều tiến trình cùng ghi kho JSON.

Main API kiểm tra nhóm tạo/luận lá số, API `/analysis`, chọn ngày cá nhân, xuất tài liệu, kho hồ sơ và tính vận hạn. `/analysis` cùng các API phân tích trước đây công khai nay yêu cầu tài khoản có quyền; đây là thay đổi theo phân chia miễn phí/tính phí mới. API calendar và date-selection month/day, number-energy vẫn công khai. Dịch vụ tư vấn riêng kiểm tra `member_access` từ `/auth/me` của Main API trước xử lý. Quyền sở hữu hồ sơ và kiểm tra ADMIN cũ vẫn được giữ.

## Chạy và triển khai

Cần nạp lại Main API và Customer Portal qua bộ chạy BTE sau khi cập nhật nội dung chuyển khoản; consulting API không cần nạp lại cho thay đổi này. Các cổng đang dùng là Main API 8000, consulting API 8082 và Portal 8686. Không khởi động thêm bản trùng cổng. Mở `/membership` hoặc `/admin-membership` trên địa chỉ Portal thực tế; nhấn Ctrl+F5 để nhận bố cục mới.

Không cần xây dựng lại gói React cho thay đổi này. Tên menu lấy từ danh mục i18n và vỏ trang chung. Trang kết quả lá số cũng dùng cùng cột menu; bố cục thu gọn thành nút mở menu trên màn hình nhỏ. Phiên bản JS trang thành viên/quản trị: `member-transfer-02`; CSS giữ `member-01`.

Các bài kiểm thử mới bao gồm đăng ký chờ duyệt, mật khẩu băm, ngăn khách tự cấp quyền, phân quyền ADMIN, cấu hình lưu lại, duyệt một lần, hết hạn, giữ quyền tài khoản cũ, tải tài liệu đúng chủ sở hữu, quyền ở dịch vụ tư vấn, ba mục miễn phí và cột bảy mục thành viên. Có kiểm thử giao diện quản trị yêu cầu tích xác nhận giao dịch. Toàn bộ dữ liệu thử dùng thư mục riêng; không tạo tài khoản hay duyệt thanh toán trong kho thật khi triển khai.
