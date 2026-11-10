# Quản trị tài khoản thành viên

## Sử dụng

Admin → **Danh sách thành viên**, giữ đường dẫn `/admin/customers`.

Danh sách hiển thị cấp 1/2/3, trạng thái đăng nhập/thành viên, ngày hết hạn và hạn mức. Có lọc theo cấp và danh sách tài khoản hiện tại/đã xóa. Tài khoản trước đây không có trường cấp được ghi **Chưa phân cấp**, giữ nguyên quyền hiện tại, không suy ra cấp từ hạn mức.

Các nút gồm Xem/Điều chỉnh, Cấp thành viên, Khóa/Mở khóa, Xóa. Danh sách đã xóa có Khôi phục.

### Cấp thành viên thủ công

Chọn tài khoản → Cấp thành viên → chọn cấp 1/2/3, thời hạn theo ngày và lý do → xác nhận.

Quyền theo cấp lấy từ cấu hình ba cấp tại thời điểm cấp, gồm từng chức năng được mở và hạn mức riêng. Thời hạn ban đầu lấy từ cấu hình cấp nếu đã có, Admin được điều chỉnh. Thời hạn tính từ lúc cấp thành công. Mở/đóng đăng ký công khai không hạn chế thao tác cấp thủ công của Admin.

Giữ nguyên vai trò tài khoản, lượt đã dùng, Linh Thạch và khóa học đã mở. Giữ tài khoản đang khóa ở trạng thái khóa. Muốn cho đăng nhập cần bấm Mở khóa riêng. Việc cấp gói không đặt lại bộ đếm sử dụng. Nếu cần chỉnh hạn mức sau cấp, dùng Xem/Điều chỉnh.

Cấp thủ công được ghi rõ nguồn `manual`, số tiền thực thu 0 và không phát sinh thưởng giới thiệu. Không xuất hiện như đơn thanh toán chờ duyệt. Nghĩa vụ thưởng của giao dịch đã duyệt trước đó vẫn giữ nguyên để tránh mất đối soát. Đơn/quyền cũ được lưu trong lịch sử quản trị trước khi thay thế.

### Khóa, xóa và khôi phục

Khóa chặn đăng nhập và việc dùng token/API key hiện có. Mở khóa giữ nguyên cấp và hạn sử dụng, không tự gia hạn.

Xóa là xóa có thể khôi phục: chặn đăng nhập, đưa khỏi danh sách hiện tại, giữ định danh tài khoản và dữ liệu liên quan. Không xóa hồ sơ tư vấn, số dư, tiến độ hay quyền khóa học. Tên đăng nhập vẫn được giữ, không cấp lại cho tài khoản khác. Trước khi xóa cần nhập đúng tên đăng nhập và lý do.

Khôi phục đưa về danh sách hiện tại ở trạng thái khóa để Admin kiểm tra rồi mở khóa. Không cho tự khóa/xóa Admin đang dùng hoặc khóa/xóa Admin cuối cùng. Các API vẫn kiểm tra quyền Admin trên máy chủ.

## Dữ liệu và độ nhất quán

Tài khoản được lưu trong kho người dùng hiện có (`users.json`). Bổ sung `deleted_at`, `account_revision`, `admin_events`, tương thích dữ liệu cũ. Mỗi thao tác lưu người thực hiện, lý do, thời điểm và trạng thái trước đó. Các dữ liệu này không được trả trong hồ sơ công khai.

Giao diện gửi phiên bản tài khoản đã đọc để chặn thao tác trên thông tin cũ. Lưu thất bại khôi phục trạng thái trong bộ nhớ. Cấp thủ công không ghi vào sổ Linh Thạch. Luồng duyệt thanh toán tiếp tục riêng biệt.

Điều chỉnh họ tên/số điện thoại từ danh sách không ghi lại hạn mức nếu hạn mức không thay đổi, để giữ cấu hình số lượt riêng của từng chức năng.

## Kiểm chứng

140 kiểm thử Python liên quan đạt. Bao gồm cấp cả ba gói, thời hạn, quyền Admin, tài khoản cũ, khóa token, xóa/khôi phục, không tự khóa Admin, chống sửa dữ liệu cũ, giữ số dư, đối soát thưởng cũ và khôi phục khi lưu lỗi.

Đã kiểm tra giao diện bằng tài khoản giả lập riêng: cấp 3, hiển thị cấp/hạn mức/ngày hết hạn, xóa, tìm trong danh sách đã xóa, khôi phục và mở khóa. Không thao tác trên tài khoản thực của người dùng. Chưa chạy bộ cài Windows tại máy người dùng.
