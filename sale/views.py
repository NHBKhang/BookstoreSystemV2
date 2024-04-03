from django.shortcuts import render, redirect
from core import dao
from bookstore import settings
from sale.utils import context_processors as cp
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
import json
from django.contrib.auth import logout, login, authenticate
from sale import qr


def index(request):
    books = dao.get_books(kw=request.GET.get('kw'))
    cart = request.session.get(settings.SALE_CART_KEY, {})

    return render(request, 'sale.html', {
        'books': books,
        'customers': dao.get_users(),
        'sale_cart': cart
    })


def sale_login(request):
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')
        user = authenticate(request, username=username, password=password,)
        if user and user.is_active and user.is_staff:
            login(request, user)

            return redirect('sale')
        else:
            return redirect('/sale/?err_msg=Incorrect')
    else:
        return redirect('sale')


def sale_logout(request):
    logout(request)

    return redirect('sale')


@csrf_exempt
def add_to_sale_cart(request):
    if request.method == 'POST' and request.user.is_authenticated:
        cart = request.session.get(settings.SALE_CART_KEY, {})

        data = json.loads(request.body.decode('utf-8'))
        id = str(data.get("id"))

        if id in cart:  # sp da co trong gio
            cart[id]['quantity'] += 1
        else:  # san pham chua co trong gio
            cart[id] = {
                "id": id,
                "name": data.get("name"),
                "price": data.get("price"),
                "quantity": 1,
                # "max_quantity": dao.get_book_inventory(id).quantity
            }

        request.session[settings.SALE_CART_KEY] = cart

        return JsonResponse(cp.count_cart(request))


@csrf_exempt
def alter_sale_cart(request, book_id):
    if request.user.is_authenticated:
        cart = request.session.get(settings.SALE_CART_KEY, {})

        if cart and book_id in cart:
            if request.method == 'PUT':
                cart[book_id]['quantity'] = (
                    int(json.loads(request.body.decode('utf-8')).get('quantity')))

            if request.method == 'DELETE':
                del cart[book_id]

        request.session[settings.SALE_CART_KEY] = cart

        return JsonResponse(cp.count_cart(request))


def invoice(request):
    cart = request.session.get(settings.SALE_CART_KEY, {})
    customer_id = request.POST.get('customer')

    try:
        receipt = dao.save_receipt_from_request(request, cart, customer_id=customer_id)
    except Exception as e:
        print(e)
        return JsonResponse({"status": 500})
    from core.models import Receipt
    return render(request, 'invoice.html', {
        'receipt': receipt,
        'sale_cart': cart
    })


def invoice_return(request):
    del request.session[settings.SALE_CART_KEY]

    return redirect('sale')


def export_invoice(request):
    cart = request.session.get(settings.SALE_CART_KEY, {})
    customer_id = request.GET.get('customer')

    try:
        receipt = dao.save_receipt_from_request(request, cart, customer_id=customer_id)
    except Exception as e:
        print(e)
        return JsonResponse({"status": 500})
    from core.models import Receipt
    return render(request, 'invoice_export.html', {
        'receipt': receipt,
        'sale_cart': cart
    })


def qr_scan(request):
    cart = request.session.get(settings.SALE_CART_KEY, {})

    data = qr.scan_qr_code()
    data = data.replace("'", '"')
    data = json.loads(data)

    id = str(data.get("id"))

    if id in cart:  # sp da co trong gio
        cart[id]['quantity'] += 1
    else:  # san pham chua co trong gio
        cart[id] = {
            "id": id,
            "name": data.get("name"),
            "price": data.get("price"),
            "quantity": 1,
            # "max_quantity": dao.get_book_inventory(id).quantity
        }

    request.session[settings.SALE_CART_KEY] = cart

    return redirect('sale')
