# Quản trị chung và cảnh báo đăng ký — 29/10/2026

## Sử dụng

Tài khoản ADMIN đăng nhập BTE Portal, chọn **Quản trị hệ thống** ở cột trái hoặc mở `/admin`. Cùng một khung điều hướng có Tổng quan, Quản lý tài khoản, Thành viên & thanh toán, Cấu hình website, Khách hàng, Hồ sơ tư vấn, Báo cáo, Bản quyền, Thống kê, Thông tin hệ thống. Các trang tài khoản, hồ sơ, báo cáo và bản quyền tái sử dụng BTE Web Admin hiện có.

`/admin/memberships` dùng để đối chiếu và duyệt chuyển khoản. `/admin/website-settings` sửa nội dung website, thông báo, biểu phí, thời hạn, hạn mức và ngân hàng. `/admin/settings` hiển thị thông tin môi trường hiện có; không biến các giá trị môi trường chỉ đọc thành cấu hình có thể sửa. Tổng quan có số tài khoản, đăng ký chờ và thành viên còn quyền sử dụng.

Địa chỉ cũ `/admin-membership` chuyển đến `/admin/memberships`. Cổng Web Admin riêng vẫn hoạt động với cùng khung và có thêm hai trang thành viên/cấu hình website để tương thích các lối truy cập cũ. Phiên trên cổng riêng vẫn tách theo nguồn trình duyệt. Trong Portal, quản trị dùng phiên đăng nhập Portal, không truyền JWT qua URL hoặc giữa hai cổng.

## Đăng ký tên trùng

Máy chủ kiểm tra trùng tên không phân biệt hoa thường trong khóa kho tài khoản. Trả HTTP 409, `code=username_taken`, `details.field=username`. Giao diện hiện chữ đỏ và viền đỏ ngay tại ô tên đăng nhập, thông báo: **Tên đăng nhập đã có người dùng rồi. Bạn hãy chọn tên đăng nhập khác.** Giữ các trường đã nhập, đưa con trỏ về ô tên đăng nhập. Sửa ô này sẽ xóa cảnh báo cũ. Chỉ báo tài khoản đã tạo nếu bước đăng ký thành công nhưng bước đăng nhập tiếp theo thất bại.

## Tổ chức mã và quyền

Portal dựng các trang quản trị từ `applications/web_admin` tại `/admin`, tài nguyên riêng tại `/admin/static` và `/admin/portal-static`. Bộ dựng template nhận tiền tố cố định để các liên kết không chạy nhầm ra trang khách. Thư viện REST quản trị tải trước mã của từng trang.

Máy khách xác minh `/auth/me` và yêu cầu vai trò ADMIN trước khi tải dữ liệu quản trị. Khung nội dung ẩn đến khi xác minh xong; hồ sơ ADMIN lưu tạm trong trình duyệt không tự cấp quyền. Các API giữ kiểm soát quyền ADMIN tại máy chủ. Không thay đổi vai trò, hạn mức, tài khoản, biểu phí hoặc ngân hàng khi triển khai. Danh sách tài khoản dùng nội dung văn bản để hiển thị họ tên an toàn.

Màn hình thành viên và cấu hình website dùng chung bộ điều khiển `admin_membership.js`, gọi các API membership hiện có. Mã đăng ký nội bộ và tương thích nội dung chuyển khoản cũ được giữ nguyên.

## Chạy và kiểm tra

Nạp lại Main API, Web Admin và Customer Portal bằng bộ chạy hiện có. Các cổng hiện tại: 8000, 8688, 8686. Không cần nạp lại dịch vụ tư vấn hoặc xây dựng gói React. Mở `/membership` hoặc `/admin` và Ctrl+F5. Phiên bản tài nguyên mới `admin-03`.

Kiểm thử: membership API, auth/quota, điều hướng Portal, trang Web Admin; JavaScript kiểm tra tên trùng, sửa và thử lại, chia mục thanh toán/cấu hình, dùng phiên Portal, chặn khách hoặc người dùng có hồ sơ ADMIN giả lưu sẵn, hiển thị tên an toàn. Trình duyệt thử dùng kho riêng; không đăng ký, duyệt tiền hoặc chỉnh cấu hình trong kho thật.
