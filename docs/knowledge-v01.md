# Kiến thức phong thủy V0.1

Ngày cập nhật: 01/11/2026.

## Thành viên

Mở menu **Kiến thức phong thủy** hoặc `/knowledge`. Thư viện hiển thị chín chuyên mục theo thứ tự:

01. Phong thủy cơ bản
02. Luận Bát tự cơ bản
03. Các Nghi thức thờ cúng
04. Phương pháp tính ngày giờ
05. Phương pháp luận dãy số
06. Phong thủy nhà ở
07. Phong thủy phần mộ
08. Các vật phẩm phong thủy
09. Các Nghi lễ phong thủy

Mỗi chuyên mục mới có khung bốn nhóm bài: nhập môn, phương pháp/ứng dụng, ví dụ thực hành, câu hỏi thường gặp. Chưa có bài giáo trình tự đăng sẵn. Bản nâng cấp từ bốn chuyên mục áp dụng một lần, giữ mã chuyên mục, nhóm bài và bài viết hiện có; tên “Luận năng lượng số” đổi thành “Phương pháp luận dãy số”. Các thay đổi Admin thực hiện sau đó không bị đặt lại khi khởi động.

Nhóm bài mặc định thu gọn; bấm tên nhóm để mở. Bài đọc có trang riêng `/knowledge/lesson/{id}`, đường dẫn về chuyên mục, nút bài trước/bài tiếp theo theo thứ tự nhóm rồi thứ tự bài. Trang đầu chỉ hiển thị sáu bài mới cập nhật. Tìm kiếm có phân trang và hỗ trợ tiếng Việt không dấu, tìm trong tiêu đề, giới thiệu và nội dung.

Trong **Câu hỏi thường gặp**, thành viên có thể gửi câu hỏi cho đúng chuyên mục đang học. Câu hỏi chờ Admin duyệt; sau khi duyệt, Admin và cộng đồng cùng bình luận trả lời ngay tại nhóm này. Câu hỏi của tôi hiển thị trạng thái riêng cho tác giả. Bài giải đáp đã biên soạn vẫn được giữ lại phía trên phần hỏi đáp. Admin lọc theo chuyên mục trong mục **Duyệt trao đổi kiến thức** để quản lý chung, không tạo hai bản dữ liệu. Xem thêm `category-questions-v01.md`.

Các API đọc kiểm tra quyền thành viên trên máy chủ. Tài khoản đang chờ kích hoạt/hết hạn không đọc được; tài khoản cũ đã được cấp quyền vẫn dùng như trước. Đọc kiến thức không trừ hạn mức tư vấn.

## Quản trị

Mở `/admin/knowledge` trong quản trị thống nhất, hoặc `/knowledge` trên Web Admin độc lập. Chỉ Admin được thêm/sửa chuyên mục, nhóm bài và bài viết.

1. Mở **Chuyên mục & nhóm bài** để đặt tên, giới thiệu và thứ tự; số nhỏ hiển thị trước. Có thể bổ sung chuyên mục/nhóm mới.
2. Chọn **Soạn bài mới**, chọn chuyên mục/nhóm, nhập tiêu đề, giới thiệu và nội dung.
3. Chia đoạn bằng dòng trống; dùng nút tiêu đề nhỏ và gạch đầu dòng để tổ chức nội dung. **Xem trước nội dung** không đăng bài.
4. Bài mới mặc định là **Bản nháp**. Chọn **Đăng cho thành viên đọc** rồi lưu khi sẵn sàng.
5. Mở lại bài trong danh sách để sửa. Chuyển về bản nháp để ẩn bài khỏi thư viện, tìm kiếm và điều hướng bài học.

Phiên bản nội dung được kiểm tra khi lưu, ngăn một phiên quản trị cũ ghi đè nội dung đã sửa ở phiên khác. Khi báo nội dung đã thay đổi, sao chép phần cần giữ trước khi tải lại.

## Dữ liệu và vận hành

Lưu trong `knowledge_library.sqlite3`, mặc định cạnh `customer_activity.sqlite3`. Có thể đặt `BTE_KNOWLEDGE_DB_PATH` để đổi vị trí. Khung chuyên mục/nhóm chỉ được khởi tạo một lần; không ghi đè tên/thứ tự Admin đã chỉnh. Không thay đổi tài khoản, ngân hàng, phí hoặc hạn mức.

Khởi động lại Main API, Customer Portal và Web Admin theo trình quản lý dịch vụ của dự án sau khi cài mã. Không cần thư viện mới hoặc chạy lại dịch vụ tư vấn. Nhấn Ctrl+F5 nếu trình duyệt còn giữ giao diện cũ. Sao lưu SQLite bằng backup API hoặc dừng dịch vụ để sao chép đủ dữ liệu/WAL.

## Giới hạn

V0.1 tổ chức bài học dạng văn bản với tiêu đề, đoạn và danh sách. Chưa có tải ảnh/video/tệp, đánh dấu đã học, bài yêu thích, bài kiểm tra, tìm kiếm toàn văn cho kho lớn hoặc bình luận trực tiếp dưới bài. Trao đổi chung tiếp tục dùng mục **Trao đổi kiến thức** hiện có.

Chưa xóa chuyên mục/nhóm/bài trong giao diện. Có thể đổi tên/thứ tự, chuyển nhóm sang chuyên mục khác và đưa bài về nháp để ẩn. Trên Web Admin độc lập dùng phần xem trước; nút mở bài ở trang thành viên hiển thị trong quản trị thống nhất cùng Portal.

Kiểm thử: `applications/api/tests/test_knowledge.py`, `applications/customer_portal/tests/test_knowledge_pages.py`, `applications/customer_portal/tests/js/knowledge.test.ts`.
