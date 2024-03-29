from core.vnpay import VNPAY
from core import dao
import numpy
from bookstore import settings
from django.urls import reverse
from datetime import datetime
from django.contrib import messages


def pay_with_vnpay(request, order):
    if request.method == "POST":
        order_desc = request.POST.get('order_desc')
        bank_code = request.POST.get('bank_code')
        language = request.POST.get('language')

        dt = dao.get_order_details(order.id)
        amount = numpy.sum([d.quantity * d.price for d in dt])

        vnp = VNPAY()
        if bank_code and bank_code != "":
            vnp.request_data['vnp_BankCode'] = bank_code
        vnp.request_data['vnp_Amount'] = amount * 100
        vnp.request_data['vnp_TxnRef'] = str(order.id) + '-' + datetime.now().strftime('%Y%m%d%H%M%S')
        vnp.request_data['vnp_OrderInfo'] = order_desc
        vnp.request_data['vnp_OrderType'] = 'bill_payment'
        vnp.request_data['vnp_CurrCode'] = settings.VNP_CURRENCY_CODE
        vnp.request_data['vnp_Version'] = settings.VNP_VERSION
        vnp.request_data['vnp_Command'] = settings.VNP_COMMAND
        vnp.request_data['vnp_TmnCode'] = settings.VNP_TMN_CODE
        vnp.request_data['vnp_Locale'] = language if language and language != '' else 'vn'
        vnp.request_data['vnp_CreateDate'] = datetime.now().strftime('%Y%m%d%H%M%S')
        vnp.request_data['vnp_IpAddr'] = settings.VNP_IP_ADDRESS
        vnp.request_data['vnp_ReturnUrl'] = settings.VNP_IP_ADDRESS + reverse('vnpay_return')

        return vnp.get_payment_url(vnpay_payment_url=settings.VNP_URL, secret_key=settings.VNP_HASH_SECRET)

    messages.error(request, 'Invalid request')

    return '/my_orders'
