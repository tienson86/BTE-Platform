# Tin nhắn và Trao đổi kiến thức V0.1

Cập nhật ngày 01/11/2026.

## Sử dụng

- Thành viên: `/messages` để đọc/gửi tin riêng với Admin; `/community` để hỏi đáp chung.
- Admin: `/admin/messages` và `/admin/community`. Hai mục này cũng có trong menu quản trị.
- Hộp thư riêng có phân trang, lịch sử tin cũ và số tin chưa đọc. Tài khoản đang chờ thanh toán hoặc hết hạn vẫn liên hệ hỗ trợ được.
- Khu trao đổi chỉ dành cho Admin, thành viên còn hạn đã thanh toán và tài khoản cũ đã được Admin cấp quyền.
- Mọi chủ đề, kể cả Admin tạo, đều chờ duyệt. Admin chọn Duyệt hiển thị hoặc Chưa chấp thuận. Tác giả sửa chủ đề thì gửi duyệt lại.
- Thành viên sửa/xóa bình luận của mình; Admin gỡ mọi bình luận hoặc chủ đề không phù hợp. Admin không sửa lời bình luận của người khác.
- Các thao tác nhắn tin, đọc bài, đăng bài và bình luận không trừ hạn mức tư vấn.

## Dữ liệu và phân quyền

API lưu vào `communications.sqlite3` cạnh cơ sở dữ liệu hoạt động `customer_activity.sqlite3`, hoặc đường dẫn `BTE_COMMUNICATIONS_DB_PATH`. Sao lưu cả hai cùng `users.json`; dùng SQLite backup API hoặc dừng dịch vụ trước khi sao chép, không bỏ qua WAL khi máy chủ đang chạy.

Liên hệ cũ có chủ sở hữu tài khoản được xác thực sẽ xuất hiện trong hộp thư của đúng người đó. Chỉ nội dung khách gửi được đưa vào hội thoại. **Ghi chú nội bộ của Admin vẫn chỉ Admin đọc được**, không chuyển thành phản hồi cho thành viên. Liên hệ khách vãng lai hoặc ghi nhận cuộc gọi do Admin tạo không tự ghép theo tên/số điện thoại.

Máy chủ kiểm tra chủ sở hữu cho từng yêu cầu đọc/gửi, quyền thành viên cho mọi API diễn đàn, quyền Admin khi duyệt/gỡ, và phiên bản nội dung khi sửa/xóa/duyệt. Mã gửi của trình duyệt giúp tránh đăng trùng khi thử lại. Nội dung hiển thị dạng văn bản, không thực thi HTML.

Gỡ nội dung là ẩn mềm, giữ dữ liệu và nhật ký thao tác phục vụ quản trị. Nội dung đã gỡ không được trả về cho người đọc diễn đàn.

## Chạy và kiểm tra

Chạy theo trình quản lý dịch vụ hiện có của dự án, gồm Main API, Customer Portal và Web Admin. Không đổi cổng đang cấu hình. Sau khi cập nhật mã nguồn, khởi động lại ba dịch vụ này; dịch vụ tư vấn vẫn chạy như trước.

Kiểm thử mới: `applications/api/tests/test_communications.py`, `applications/customer_portal/tests/test_communications_pages.py`, `applications/customer_portal/tests/js/communications.test.ts`.

## Giới hạn V0.1

Chưa gửi email, thông báo đẩy, tệp đính kèm hoặc cập nhật tức thì. Nhấn **Tải lại** để nhận tin/bình luận mới. Số tin chưa đọc trên menu cập nhật khi mở trang hoặc đọc hội thoại. Chưa có tìm kiếm nội dung, thông báo riêng khi chủ đề chờ duyệt, hay khôi phục nội dung đã gỡ trong giao diện.
