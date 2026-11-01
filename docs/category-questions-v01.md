# Hỏi đáp theo chuyên mục kiến thức

Cập nhật ngày 01/11/2026.

## Thành viên

Vào Kiến thức phong thủy, mở một trong chín chuyên mục rồi mở nhóm **Câu hỏi thường gặp**. Nhấn **Đặt câu hỏi về chuyên mục này**, nhập tiêu đề và nội dung, gửi Admin duyệt. Câu hỏi được gắn với chuyên mục đang học. Trong **Câu hỏi của tôi**, tác giả xem được trạng thái chờ duyệt và ghi chú của Admin.

Câu hỏi chỉ hiển thị chung và mở bình luận khi được duyệt. Admin và các thành viên còn quyền sử dụng có thể trả lời trực tiếp tại đó. Thành viên sửa/xóa bình luận của mình; Admin gỡ bình luận hoặc câu hỏi không phù hợp. Sửa câu hỏi đã duyệt sẽ gửi duyệt lại, giữ nguyên chuyên mục.

Bài giải đáp Admin đã biên soạn trong nhóm FAQ vẫn hiển thị phía trên phần hỏi đáp cộng đồng. Hỏi đáp không trừ lượt tư vấn.

## Quản trị

Vào **Duyệt trao đổi kiến thức**, dùng ô **Chuyên mục** để lọc hàng chờ, đọc câu hỏi và chọn duyệt/chưa chấp thuận. Có thể duyệt ngay tại nhóm FAQ bằng tài khoản Admin. Tất cả dùng chung chủ đề và bình luận với Trao đổi kiến thức, không tạo hai bản nội dung.

Trao đổi kiến thức vẫn có thể đăng chủ đề chung hoặc chọn một chuyên mục. Chủ đề cũ được giữ nguyên ở trao đổi chung; không tự suy đoán chuyên mục từ nội dung cũ. Chuyên mục của câu hỏi được giữ cố định sau khi gửi; V0.1 chưa chuyển câu hỏi giữa chuyên mục.

## Dữ liệu và cập nhật

Thêm trường nullable `category_id` và chỉ mục trong bảng `knowledge_topics` của `communications.sqlite3`. Nâng cấp trong giao dịch SQLite, không sửa nội dung/chủ sở hữu/trạng thái của các chủ đề cũ. Chuyên mục được đối chiếu với `knowledge_library.sqlite3` khi tạo/lọc câu hỏi; quyền thành viên và duyệt được kiểm tra trên máy chủ.

Nhóm FAQ của chín chuyên mục gốc được nhận diện bằng mã nhóm ổn định, không dựa vào tên hiển thị hoặc số thứ tự. Đổi tên/sắp xếp nhóm không làm mất chức năng hỏi đáp. Các nhóm tự tạo ngoài khung gốc chưa có tùy chọn đổi vai trò thành FAQ trong giao diện.

Sao lưu hai cơ sở dữ liệu bằng SQLite backup API trước khi cập nhật, rồi nạp lại Main API và Portal. Không cần thư viện mới. Nhấn Ctrl+F5 nếu còn giao diện cũ. Chưa có thông báo đẩy; nhấn Tải lại để nhận câu hỏi/bình luận mới.
