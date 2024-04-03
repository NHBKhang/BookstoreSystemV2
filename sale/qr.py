import cv2
from pyzbar.pyzbar import decode


def scan_qr_code():
    # Mở camera
    cap = cv2.VideoCapture(0)

    while True:
        # Đọc frame từ camera
        ret, frame = cap.read()

        # Quét mã QR từ frame
        decoded_objects = decode(frame)

        # Nếu nhận được mã QR, trả về dữ liệu của mã QR
        if decoded_objects:
            for obj in decoded_objects:
                cap.release()
                cv2.destroyAllWindows()
                # Giải mã dữ liệu từ mã QR và trả về nó
                return obj.data.decode('utf-8')

        # Hiển thị frame
        cv2.imshow('Camera', frame)

        # Thoát vòng lặp nếu nhấn phím 'q'
        if cv2.waitKey(1) & 0xFF == ord('q'):
            break

    # Giải phóng camera và đóng cửa sổ
    cap.release()
    cv2.destroyAllWindows()
