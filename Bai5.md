# BÁO CÁO THIẾT KẾ HỆ THỐNG RIKKEIMART
## Chủ đề: Phân tích Vai trò UML & Danh mục Sơ đồ Hệ thống RikkeiMart

---

### PHẦN 1: GIẢI THÍCH VAI TRÒ UML & LẬP BẢNG ĐỊNH HƯỚNG SƠ ĐỒ UML

#### 1. 2 Lý do sử dụng sơ đồ UML giúp Dev, BA và Tester không bị hiểu nhầm kịch bản hết hàng
* **Trực quan hóa luồng nghiệp vụ phức tạp & loại bỏ rào cản ngôn ngữ tự nhiên:**
  * Ngôn ngữ tự nhiên (mô tả bằng lời hoặc văn bản) dễ gây ra hiểu nhầm đa nghĩa giữa BA, Dev và Tester, đặc biệt khi xử lý các kịch bản ngoại lệ (Edge Cases) như hết hàng tại cửa hàng hay khách hàng không nghe máy.
  * UML (đặc biệt là Activity Diagram / Sequence Diagram) cung cấp cú pháp đồ họa chuẩn hóa quốc tế với các điểm rẽ nhánh (Decision Node), luồng công việc (Control Flow) và khoảng thời gian chờ (Timeout Event). Nhờ đó, tất cả các bên có cùng một góc nhìn trực quan duy nhất về luồng xử lý: *Khi hết hàng -> Tài xế chọn món thay thế -> Gửi thông báo -> Đợi 3 phút -> Timeout tự động ngắt mạch (Auto-substitute / Auto-cancel)*.

* **Định nghĩa chính xác giao ước hệ thống (Contract) và điều kiện biên (Boundary Conditions):**
  * UML Class Diagram và State Machine / Activity Diagram xác định rõ ràng các thuộc tính, trạng thái đơn hàng (ví dụ: `PENDING_SUBSTITUTE`, `AUTO_CANCELLED`, `AUTO_SUBSTITUTE_CONFIRMED`) cùng các sự kiện kích hoạt chuyển trạng thái.
  * Điều này giúp **Dev** biết chính xác phải cài đặt hàm timeout/exception gì; **Tester** có căn cứ chính xác để xây dựng các kịch bản test case (Test matrix cho trường hợp phản hồi đúng hạn, phản hồi quá hạn, tắt máy); và **BA** đảm bảo quy tắc nghiệp vụ không bị bỏ sót.

---

#### 2. Bảng định hướng danh mục sơ đồ UML cho dự án RikkeiMart

| STT | Phân nhóm Sơ đồ | Tên Sơ đồ UML | Mục đích cụ thể trong Dự án RikkeiMart |
|---|---|---|---|
| **1** | **Hành vi (Behavioral)** | **Use Case Diagram** | Thể hiện tổng quan các chức năng chính của hệ thống và sự tương tác giữa các tác nhân (Khách hàng, Tài xế mua hộ, Hệ thống tự động). Làm rõ phạm vi hệ thống cho chức năng mua hộ thực phẩm, xử lý đổi món thay thế và tự động hủy/đổi đơn khi hết hạn. |
| **2** | **Hành vi (Behavioral)** | **Activity Diagram** | Mô tả chi tiết luồng công việc (Workflow) khi tài xế phát hiện cửa hàng hết hàng: bao gồm các bước đề xuất sản phẩm thay thế tương đương, gửi thông báo xác nhận đến App khách hàng, luồng đếm ngược Timeout 3 phút và điểm rẽ nhánh xử lý an toàn (Auto-substitute / Auto-cancel). |
| **3** | **Cấu trúc (Structural)** | **Class Diagram** | Định nghĩa cấu trúc dữ liệu và mô hình lớp đối tượng cho hệ thống (ví dụ các lớp `Order`, `OrderItem`, `Product`, `Driver`, `CustomerNotification`, `TimeoutHandler`). Thể hiện thuộc tính, phương thức và mối quan hệ giữa các lớp nhằm làm cơ sở cho Dev lập trình. |

---

### PHẦN 2: TRIỂN KHAI MÃ NGUỒN MÔ PHỎNG (PYTHON)

Dưới đây là mã nguồn Python mô phỏng luồng xử lý đơn hàng RikkeiMart với thuật toán đếm ngược Timeout 3 phút, bắt trọn các ngoại lệ hết hàng và phản hồi của khách hàng mà không làm sụp đổ (crash) chương trình.

Mã nguồn chi tiết được lưu trữ tại file: [`solution_bai5.py`](file:///home/PageNguyen/Learning/RIKKEI/IT105_Analysis&Design_System/Session02/solution_bai5.py).
