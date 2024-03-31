from django.core.mail import EmailMessage
from django.core.mail.backends.smtp import EmailBackend
from django.conf import settings


class Mail:
    error = False

    def __init__(self, email_type, context=None):
        try:
            if email_type == 'order':
                self.subject = 'Thanh toán đơn hàng thành công'
                self.message = (f'Chào {context["name"]},\nĐơn hàng {context["id"]} của bạn đã được thanh toán thành '
                                f'công. Đơn hàng sẽ được đóng gói và vận chuyển đến địa chỉ sớm nhất có thể. Vui lòng '
                                f'theo dõi đơn hàng cùa bạn trên trang web. Cảm ơn bạn vì đã mua sách tại Bookstore.\n'
                                f'Trân trọng\nBOOKSTORE')
            elif email_type == 'subscribe':
                self.subject = 'Đăng ký nhận email về sách'
                self.message = (f'Chào {context["name"]},\nBạn đã đăng ký dịch vụ nhận email về các cập nhật và sự kiện'
                                f' sản phẩm. Bạn sẽ nhận được các thông tin mới nhất về sách thông qua email. Nếu bạn '
                                f'thay đổi ý định, bạn có thể hủy đăng ký bất cứ lúc nào. Cảm ơn bạn vì đã đăng ký dịch'
                                f' vụ của chúng tôi.\nTrân trọng\nBOOKSTORE')
            else:
                raise ValueError(email_type + ' is invalid email_type value')
        except Exception as e:
            print(e)
            self.error = True

    def send_email(self, to_email_list, subject=None, message=None):
        if self.error:
            return

        # Configure Ethereal SMTP settings
        ethereal_backend = EmailBackend(
            host=settings.EMAIL_HOST,
            port=settings.EMAIL_PORT,
            username=settings.EMAIL_HOST_USER,
            password=settings.EMAIL_HOST_PASSWORD,
            use_tls=settings.EMAIL_USE_TLS
        )

        # Create EmailMessage object
        email = EmailMessage(
            subject=subject if subject else self.subject,
            body=message if message else self.message,
            from_email=settings.DEFAULT_FROM_EMAIL,
            to=to_email_list,
            connection=ethereal_backend
        )

        try:
            email.send()
            return True
        except Exception as e:
            print("Error sending email:", str(e))
            return False
