# Khóa học BTE V0.1

## Thành viên

- Menu **Khóa học** dưới **Kiến thức phong thủy**, trang `/khoa-hoc`.
- Mai Hoa Dịch Số nhập môn gồm 8 bài viết, bài tập/đáp án và một video tổng hợp có giọng đọc (5 phút 15 giây).
- Bài Âm Dương và Bát Quái cho học thử. Các bài còn lại kiểm tra quyền trên máy chủ.
- Lưu tiến độ trên máy chủ, theo tài khoản. Học lại không trừ điểm, đánh dấu hoàn thành không cộng điểm.
- Đổi theo cả khóa. Trước khi đổi có xác nhận giá, thời hạn, số dư và số dư còn lại.
- Kinh Dịch nhập môn đang biên soạn, chưa có bài nên chưa cho mở đổi.

## Quản trị

Mở **Admin → Quản lý khóa học**, `/admin/courses`. Admin riêng dùng `/courses`.

Mỗi khóa có tên, giới thiệu, giá Linh Thạch, thời hạn theo ngày hoặc không giới hạn, trạng thái đang chuẩn bị/mở đổi/tạm ngừng đổi mới. Có liên kết từ Cấu hình website.

Hai khóa mặc định **Đang chuẩn bị**. Giá ban đầu 0 chỉ là cấu hình chưa mở bán. Admin phải tự xác định giá, thời hạn và chọn Mở đổi trước khi thành viên có thể đổi. Giá 0 khi mở đổi nghĩa là miễn phí.

Thời hạn tính từ thời điểm mở khóa thành công. Không giới hạn thời gian được lưu bằng `null`, không dùng số 0. Cấu hình thay đổi chỉ áp dụng cho lượt đổi mới. Quyền đã mở lưu nguyên giá, phiên bản cấu hình và ngày hết hạn. Tạm ngừng đổi mới không thu hồi quyền đã mua.

Tài khoản phải còn quyền thành viên để học. Quyền khóa học có thời hạn riêng, không làm gia hạn gói thành viên. Hết hạn khóa thì bài trả phí bị khóa, bài thử và tiến độ vẫn giữ. Thành viên có thể xác nhận đổi lại theo giá/thời hạn hiện tại.

## Dữ liệu và giao dịch

Các bảng `courses_settings`, `courses_access`, `courses_progress` nằm cùng SQLite `customer_activity.sqlite3` với sổ Linh Thạch. Nếu hệ thống đã cấu hình `BTE_USAGE_DB_PATH`, tiếp tục dùng đúng đường dẫn đó.

Trừ điểm và cấp quyền trong cùng giao dịch `BEGIN IMMEDIATE`. Mã giao dịch chống gửi lặp. Khi khóa vẫn còn hiệu lực, gửi lại hoặc bấm đổi lần nữa không trừ thêm. Giá do máy chủ quyết định; đổi từ trang cũ sau thay đổi cấu hình phải tải lại và xác nhận giá mới. Khóa học dùng loại giao dịch `course_purchase`, không can thiệp mức đổi 5 Linh Thạch/lượt tư vấn.

Video lưu tại `applications/api/course_media/mai-hoa-thuc-hanh.mp4`, không nằm trong thư mục static. API kiểm tra quyền trước khi trả video. Giao diện tải video bằng Authorization header rồi phát blob; không đặt token trong đường dẫn.

Không ghi đè dữ liệu thành viên hoặc các bài trong thư viện kiến thức. Cấu hình khóa được khởi tạo một lần bằng INSERT OR IGNORE để giữ chỉnh sửa của Admin qua các lần khởi động.

Nội dung Mai Hoa dùng quy ước giảng dạy hai số nguyên dương, không cộng giờ. Số dư 0 khi chia 8 quy về Khôn, chia 6 quy về hào 6. Đây là quy ước của khóa nhập môn, không đại diện mọi phương pháp Mai Hoa.

## Kiểm chứng

Kiểm thử API/dịch vụ bao gồm quyền thành viên/Admin, học thử, khóa bài/video, lưu cấu hình, xung đột phiên bản, thiếu điểm, đổi đồng thời, chống trừ lặp, hết hạn, đổi lại, không giới hạn, lưu tiến độ riêng và bảo toàn quyền cũ.

Đã kiểm tra giao diện trình duyệt bằng tài khoản và điểm thử nghiệm riêng: menu, danh sách khóa, xác nhận đổi, phát video, lưu tiến độ và chỉnh giá/thời hạn trong Admin. Chưa chạy bộ cài trên Windows của người dùng.
