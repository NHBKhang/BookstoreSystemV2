from datetime import datetime
from rest_framework import viewsets, generics, status, parsers
from rest_framework.decorators import action
from rest_framework.response import Response
from core import serializers, paginators, dao
from core.models import Category, User, Author, Inventory, Book, Book_Inventories, Gender, OrderStatus
from django.shortcuts import render, redirect, get_object_or_404
from django.http import JsonResponse
import math
import json
from bookstore import settings
from core.utils import context_processors as cp
from django.contrib.auth import login
from core.utils import utils
from django.contrib import messages
from core.mail import Mail
from urllib.parse import parse_qs


class CategoryViewSet(viewsets.ModelViewSet):
    queryset = Category.objects.all()
    serializer_class = serializers.CategorySerializer


class AuthorViewSet(viewsets.ViewSet, generics.ListCreateAPIView):
    queryset = Author.objects.all()
    serializer_class = serializers.AuthorSerializer


class InventoryViewSet(viewsets.ViewSet, generics.RetrieveUpdateAPIView, generics.ListAPIView):
    queryset = Inventory.objects.all()
    serializer_class = serializers.InventorySerializer


class BookInventoriesViewSet(viewsets.ViewSet, generics.ListAPIView):
    queryset = Book_Inventories.objects.all()
    serializer_class = serializers.BookInventoriesSerializer


class BookViewSet(viewsets.ViewSet, generics.ListAPIView):
    queryset = Book.objects.filter(active=True)
    serializer_class = serializers.BookSerializer
    pagination_class = paginators.BookPaginator

    def get_queryset(self):
        queryset = self.queryset

        if self.action.__eq__('list'):
            q = self.request.query_params.get('q')
            if q:
                queryset = queryset.filter(name__icontains=q)

            cate_id = self.request.query_params.get('category_id')
            if cate_id:
                queryset = queryset.filter(category_id=cate_id)

        return queryset


class UserViewSet(viewsets.ViewSet, generics.CreateAPIView):
    queryset = User.objects.filter(is_active=True)
    serializer_class = serializers.UserSerializer
    parser_classes = [parsers.MultiPartParser, ]


# template
def index(request):
    books = dao.get_books(limit=4)

    return render(request, 'index.html', {'books': books})


def pages(request):
    cate_id = request.GET.get('cate_id')
    page = request.GET.get('page')
    kw = request.GET.get('kw')

    books = dao.get_books(cate_id=cate_id, kw=kw, page=page)

    return render(request, 'pages.html', {
        'books': books,
        'pages': range(1, math.ceil(dao.books_count(cate_id=cate_id, kw=kw)
                                    / settings.PAGE_SIZE) + 1)
    })


def details(request, book_id):
    book = dao.get_book_by_id(book_id)

    return render(request, 'details.html', {
        'book': book,
        'auths': [{'id': item[0], 'name': item[1]} for item in book.authors.values_list('id', 'name')],
        'cates': [{'id': item[0], 'name': item[1]} for item in book.categories.values_list('id', 'name')]
    })


def register(request):
    if request.method == 'POST':
        username = request.POST['username']
        password = request.POST['password']
        confirm_password = request.POST['confirm_password']
        first_name = request.POST['first_name']
        last_name = request.POST['last_name']
        birthday = request.POST['birthday']
        gender_val = request.POST['gender']
        phone = request.POST['phone']
        email = request.POST['email']
        address = request.POST['address']

        try:
            if password != confirm_password:
                raise Exception('Passwords do not match.')

            if int(gender_val) == 1:
                gender = Gender.MALE
                avatar = 'https://res.cloudinary.com/dd0qzygo7/image/upload/v1711539545/gyaplslq1shp2exulcia.png'
            elif int(gender_val) == 2:
                gender = Gender.FEMALE
                avatar = 'https://res.cloudinary.com/dd0qzygo7/image/upload/v1711551474/t0cra9qee3xq04yywsns.png'
            else:
                gender = Gender.OTHER
                avatar = 'https://res.cloudinary.com/dd0qzygo7/image/upload/v1711539545/gyaplslq1shp2exulcia.png'

            user = (User.objects
                    .create_user(username=username, password=password, first_name=first_name,
                                 last_name=last_name, birthday=birthday, gender=gender,
                                 phone=phone, email=email, avatar=avatar,
                                 address=address, last_login=datetime.now(), date_joined=datetime.now()))
            user.save()

            login(request, user)

            return redirect('home')
        except Exception as e:
            return render(request, 'register.html', {
                'error_msg': e.__str__()})

    return render(request, 'register.html')


def cart(request):
    c = request.session.get('cart', {})

    return render(request, 'cart.html', {'cart': c})


def add_to_cart(request):
    if request.method == 'POST':
        cart = request.session.get(settings.CART_KEY, {})

        data = json.loads(request.body.decode('utf-8'))
        id = data.get("id")

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

        request.session[settings.CART_KEY] = cart

        return JsonResponse(cp.count_cart(request))


def alter_cart(request, book_id):
    cart = request.session.get(settings.CART_KEY, {})

    if cart and book_id in cart:
        if request.method == 'PUT':
            cart[book_id]['quantity'] = (
                int(json.loads(request.body.decode('utf-8')).get('quantity')))

        if request.method == 'DELETE':
            del cart[book_id]

    request.session[settings.CART_KEY] = cart

    return JsonResponse(cp.count_cart(request))


def payment(request):
    return render(request, 'payment.html')


def comments(request, book_id):
    if request.method == 'POST':
        try:
            comment = json.loads(request.body.decode('utf-8'))
            if comment['content'] == '':
                return JsonResponse({'status': 501})
            c = dao.save_comment(book_id=book_id, content=comment['content'], user_id=request.user.id)
        except Exception as e:
            print(e)
            return JsonResponse({'status': 500})

        return JsonResponse({
            'status': 204,
            'comment': {
                'id': c.id,
                'content': c.content,
                'created_date': str(c.created_date),
                'user': {
                    'username': c.user.username,
                    'name': c.user.first_name + ' ' + c.user.last_name,
                    'avatar': c.user.avatar.url
                }
            }
        }, safe=False)
    else:
        data = []
        for c in dao.get_comments(book_id=book_id):
            data.append({
                'id': c.id,
                'content': c.content,
                'created_date': c.created_date,
                'user': {
                    'username': c.user.username,
                    'name': c.user.first_name + ' ' + c.user.last_name,
                    'avatar': c.user.avatar.url
                }
            })

        return JsonResponse(data, safe=False)


def pay(request):
    cart = request.session.get(settings.CART_KEY, {})
    method = request.POST.get('payment')
    subscribe = request.POST.get('subscribe')

    if cart:
        order = None
        try:
            if subscribe:
                Mail('subscribe', {
                    'name': request.user.first_name
                }).send_email([request.user.email])

            if int(method) == 3:
                order = dao.save_order_from_request(request, cart=cart, is_paid=True)
            elif int(method) == 4:
                print(method)
                order = dao.save_order_from_request(request, cart=cart)
        except Exception as ex:
            print(str(ex))
            return JsonResponse({"status": 500})
        else:
            del request.session[settings.CART_KEY]

            if int(method) == 3:
                return redirect(utils.pay_with_vnpay(request, order), kwargs=JsonResponse({"status": 200}))

            elif int(method) == 4:
                return redirect('/my_orders/' + str(order.id), kwargs=JsonResponse({"status": 200}))


def vnpay_return(request):
    vnp_TransactionNo = request.GET.get('vnp_TransactionNo')
    vnp_TxnRef = request.GET.get('vnp_TxnRef')
    vnp_Amount = request.GET.get('vnp_Amount')
    vnp_ResponseCode = request.GET.get('vnp_ResponseCode')
    vnp_BankCode = request.GET.get('vnp_BankCode')
    vnp_OrderInfo = request.GET.get('vnp_OrderInfo')
    order_id = int(vnp_TxnRef.split('-')[0])

    if vnp_ResponseCode == '00':
        try:
            transaction = dao.save_transaction(vnp_TransactionNo, vnp_BankCode, vnp_OrderInfo)
            dao.update_order(order_id, status=OrderStatus.PROCESSING, transaction_id=transaction.id)

            Mail('order', {
                'id': order_id,
                'name': request.user.first_name
            }).send_email([request.user.email])

            messages.info(request, 'Cập nhật trạng thái thanh toán thành công.')
        except Exception as e:
            print(f"Error updating database: {str(e)}")
            messages.error(request, 'Lỗi cập nhật trạng thái thanh toán.')

    else:
        messages.error(request, 'Lỗi thanh toán. Vui lòng thử lại hoặc liên hệ với hỗ trợ.')

    return render(request, 'vnpay_return.html', {
        'transaction_no': vnp_TransactionNo,
        'txn_ref': vnp_TxnRef,
        'amount': int(float(vnp_Amount) / 100),
        'bank_code': vnp_BankCode,
        'description': vnp_OrderInfo,
        'order_id': order_id
    })


def my_orders(request):
    orders, summary = dao.get_orders_by_user_id(request.user.id)

    return render(request, 'my_orders.html', {
        'orders': orders,
        'summary': summary
    })


def my_order_details(request, order_id):
    order = dao.get_order_by_order_id(order_id)

    return render(request, 'my_order_details.html', {
        'order': order
    })


def profile(request):
    if request.method == 'POST':
        first_name = request.POST.get('first_name')
        last_name = request.POST.get('last_name')
        birthday = request.POST.get('birthday')
        gender = request.POST.get('gender')
        phone = request.POST.get('phone')
        email = request.POST.get('email')
        address = request.POST.get('address')
        avatar = request.POST.get('avatar')

        if dao.update_user(request.user.id, first_name, last_name, birthday, Gender(int(gender)), phone, email,
                           address, avatar):
            return redirect('profile')

    return render(request, 'profile.html', {
        'stat': dao.profile_stats(request.user)
    })
