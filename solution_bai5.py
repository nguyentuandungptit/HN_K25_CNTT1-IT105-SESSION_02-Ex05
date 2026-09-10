"""
Dự án RikkeiMart (thuộc RikkeiExpress)
Chương trình mô phỏng luồng xử lý đơn hàng khi hết hàng & Bẫy Timeout 3 phút (Unreachable Customer Trap)
"""

import time
from typing import Optional, Dict, Any

class OutOfStockException(Exception):
    """Ngoại lệ ném ra khi sản phẩm tại cửa hàng hết hàng."""
    def __init__(self, item_name: str, substitute_item: str):
        super().__init__(f"Sản phẩm '{item_name}' đã hết hàng tại cửa hàng!")
        self.item_name = item_name
        self.substitute_item = substitute_item


class CustomerUnreachableException(Exception):
    """Ngoại lệ ném ra khi khách hàng không phản hồi trong khoảng thời gian quy định (Timeout)."""
    def __init__(self, timeout_seconds: int):
        super().__init__(f"Khách hàng không phản hồi sau {timeout_seconds} giây (Timeout).")
        self.timeout_seconds = timeout_seconds


def process_rikkeimart_order(
    item_status: str,
    customer_response: Optional[str] = None,
    response_delay: int = 0,
    timeout_limit: int = 3
) -> Dict[str, Any]:
    """
    Hàm mô phỏng luồng xử lý đơn hàng RikkeiMart.

    Parameters:
    - item_status (str): Trạng thái hàng tại cửa hàng ('AVAILABLE' hoặc 'OUT_OF_STOCK')
    - customer_response (str, optional): Phản hồi của khách ('ACCEPT', 'REJECT', hoặc None nếu không trả lời)
    - response_delay (int): Thời gian (giây) khách hàng phản hồi
    - timeout_limit (int): Giới hạn thời gian Timeout (mặc định mô phỏng 3 giây tương ứng 3 phút)

    Returns:
    - Dict chứa kết quả xử lý đơn hàng.
    """
    print("\n" + "="*60)
    print(f"--> BẮT ĐẦU XỬ LÝ ĐƠN HÀNG RIKKEIMART")
    print(f"    Trạng thái kho: {item_status}")
    print(f"    Phản hồi của khách: {customer_response} (Độ trễ: {response_delay}s)")
    print("="*60)

    order_result = {
        "status": "PROCESSING",
        "message": "",
        "action": ""
    }

    try:
        # 1. Kiểm tra tồn kho tại cửa hàng
        if item_status.upper() == "OUT_OF_STOCK":
            # Ném ngoại lệ hết hàng và đề xuất món thay thế tương đương
            raise OutOfStockException(
                item_name="Táo đỏ Fuji",
                substitute_item="Táo xanh Ninh Thuận (Cùng giá 50.000 VNĐ)"
            )
        
        # Trường hợp hàng còn đủ
        order_result["status"] = "SUCCESS"
        order_result["message"] = "Đơn hàng mua thành công sản phẩm gốc."
        order_result["action"] = "DELIVERING_ORIGINAL_ITEM"
        print("[TC] Sản phẩm sẵn có. Tài xế tiến hành mua hàng và giao đến khách.")
        return order_result

    except OutOfStockException as e:
        print(f"[CẢNH BÁO] {e}")
        print(f"[TÀI XẾ] Chọn sản phẩm thay thế: '{e.substitute_item}'")
        print(f"[HỆ THỐNG] Đã gửi thông báo xác nhận đổi món đến App khách hàng. Bắt đầu đếm ngược Timeout ({timeout_limit}s)...")

        # 2. Mô phỏng chờ phản hồi từ khách hàng và xử lý bẫy Timeout 3 phút
        try:
            # Kiểm tra xem độ trễ phản hồi có vượt quá giới hạn timeout không
            if response_delay > timeout_limit or customer_response is None:
                # Giả lập thời gian trễ
                actual_wait = min(response_delay, timeout_limit)
                time.sleep(actual_wait)
                raise CustomerUnreachableException(timeout_seconds=timeout_limit)
            
            time.sleep(response_delay)
            print(f"[KHÁCH HÀNG] Đã phản hồi sau {response_delay}s với lựa chọn: '{customer_response}'")

            if customer_response.upper() == "ACCEPT":
                order_result["status"] = "SUCCESS"
                order_result["message"] = f"Khách hàng đồng ý đổi sang '{e.substitute_item}'."
                order_result["action"] = "DELIVERING_SUBSTITUTE_ITEM"
            elif customer_response.upper() == "REJECT":
                order_result["status"] = "CANCELLED_BY_CUSTOMER"
                order_result["message"] = "Khách hàng từ chối đổi món. Đơn hàng được hủy theo yêu cầu."
                order_result["action"] = "CANCEL_ORDER"
            else:
                order_result["status"] = "INVALID_RESPONSE"
                order_result["message"] = "Phản hồi không hợp lệ."
                order_result["action"] = "CANCEL_ORDER"

        except CustomerUnreachableException as timeout_err:
            print(f"[HỆ THỐNG NGẮT MẠCH TIMEOUT] {timeout_err}")
            print("[HỆ THỐNG] Thực hiện ngắt mạch an toàn: Tự động đổi món (Auto-substitute) / Hủy đơn an toàn để giải phóng tài xế.")
            
            # Xử lý tự động ngắt mạch (Circuit Breaker)
            order_result["status"] = "AUTO_RESOLVED_TIMEOUT"
            order_result["message"] = "Hết 3 phút khách không phản hồi. Tự động áp dụng quy tắc ngắt mạch an toàn."
            order_result["action"] = "AUTO_SUBSTITUTE_OR_CANCEL"

    except Exception as general_err:
        print(f"[LỖI KHÔNG MONG MUỐN] {general_err}")
        order_result["status"] = "SYSTEM_ERROR"
        order_result["message"] = str(general_err)

    return order_result


# --- CHƯƠNG TRÌNH CHẠY KIỂM THỬ KỊCH BẢN (TEST SUITE) ---
if __name__ == "__main__":
    print("=========================================================")
    print("   DEMO MÔ PHỎNG LUỒNG XỬ LÝ ĐƠN HÀNG RIKKEIMART (UML Bai 5)")
    print("=========================================================")

    # Kịch bản 1: Hàng có sẵn trong kho
    res1 = process_rikkeimart_order(item_status="AVAILABLE")
    print(f"--> KẾT QUẢ: {res1}\n")

    # Kịch bản 2: Hết hàng, khách hàng nghe máy & ĐỒNG Ý đổi món trong 1s
    res2 = process_rikkeimart_order(
        item_status="OUT_OF_STOCK",
        customer_response="ACCEPT",
        response_delay=1
    )
    print(f"--> KẾT QUẢ: {res2}\n")

    # Kịch bản 3: Hết hàng, khách hàng nghe máy & TỪ CHỐI đổi món trong 2s
    res3 = process_rikkeimart_order(
        item_status="OUT_OF_STOCK",
        customer_response="REJECT",
        response_delay=2
    )
    print(f"--> KẾT QUẢ: {res3}\n")

    # Kịch bản 4 (Bẫy dữ liệu): Hết hàng, Khách hàng TẮT MÁY / KHÔNG TRẢ LỜI (Vượt quá 3s timeout)
    res4 = process_rikkeimart_order(
        item_status="OUT_OF_STOCK",
        customer_response=None,
        response_delay=5, # Khách trễ 5 giây (> 3s limit)
        timeout_limit=3
    )
    print(f"--> KẾT QUẢ: {res4}\n")

    print("=> TẤT CẢ CÁC KỊCH BẢN ĐÃ CHẠY HOÀN HẢO MÀ KHÔNG BỊ CRASH!")
