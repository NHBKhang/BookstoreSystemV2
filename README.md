# Bookstore System V2

Đồ án cuối kỳ cho môn Lập trình Cơ sở dữ liệu. Hệ thống quản lý nhà sách viết bằng Python Django sử dụng CSDL MySQL server.

* **Cài đặt:**
    -
    - C1: Tải về file .zip về máy và giải nén
    - C2: Mở Terminal hay Git Bash nhập lệnh *git clone https://github.com/NHBKhang/BookstoreSystemV2*


* **Chạy project:**
    - 
    - Mở folder project bằng Pycharm IDE và cài đặt môi trường ảo (File->Settings->Project->Python Interpreter->Add->
          Local)
    - Mở Terminal (phím tắt: Alt+F12) và tải các package cần thiết *pip install -r requirements.txt*
    - Sử dụng MySQL workbench để tạo schema mới *CREATE SCHEMA `bookstoredb` DEFAULT CHARACTER SET=utf8mb4
      COLLATE=utf8mb4_unicode_ci*
    - Vào bookstore\settings.py để chỉnh lại các cấu hình cần thiết 
        + DATABASES (đổi password,...)
        + Cloudinary và VNP config (nếu cần)
    - Mở Terminal và tạo bảng cho CSDL (cd tới folder có chứa file manage.py nếu cần)
        + Tạo các tệp migration: *python manage.py makemigrations*
        + Áp dụng các tệp migration được tạo vàp CSDL: *python manage.py migrate*
    - Chạy project: *python manage.py runserver*


* **Kiểm thử project:**
    -
    - Chạy lệnh *python manage.py test* để chạy tất cả các test case có sẵn
  

* **Các lệnh khác:**
    - 
    - *python manage.py createsuperuser* tạo tài khoản admin 
    - *django-admin startproject <project_name>* tạo project django mới
    - *python manage.py startapp <app_name>* tạo app mới
    - *python manage.py test* kiểm thử phần mềm

* Notes: 
  - 
  - Dữ liệu trong CSDL tự thêm vào bằng cách lên trang /admin do user tự tạo
  - Tài khoản test VNPAY:
    + Ngân hàng: NCB
    + Số thẻ: 9704198526191432198
    + Tên chủ thẻ: NGUYEN VAN A
    + Ngày phát hành: 07/15
    + Mật khẩu OTP: 123456
  - Tài khoản test VNPAY:
    + Username: nhbkhang12@gmail.com
    + Password: Khang2003
  - Tài khoản test mail server Ethereal:
    + Email: josh.johnston@ethereal.email
    + Password: eqaUJhQGnhduwAK7CT
  - Các website liên quan tới hệ thống:
    + VNPAY Admin: https://sandbox.vnpayment.vn/merchantv2/
    + VNPAY Test case: https://sandbox.vnpayment.vn/vnpaygw-sit-testing/user/login
    + Ethereal Web: https://ethereal.email/
    + Pythonanywhere: Nothing here
    + GG Drive: https://drive.google.com/drive/folders/1iLbAZDfFQ2MM5kR3MuzpbPS_KPjXvou_?usp=drive_link
  - Ngôn ngữ: Html, Css, Javascript, Python
  - Framework: Django, REST API
  - Tools: MySQL Workbench, PyCharm

