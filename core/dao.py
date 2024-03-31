from core.models import Book, Comment, Order, OrderDetails, Receipt, ReceiptDetails, User, Transaction
from bookstore import settings


def get_books(kw=None, cate_id=None, page=None, desc=True, limit=None):
    books = Book.objects

    if desc:
        books = books.order_by('-id')
    if limit:
        return books.all()[:limit]
    if kw:
        books = books.filter(name__icontains=kw)
    if cate_id:
        books = books.filter(categories__id=cate_id)
    if page:
        page = int(page)
        page_size = settings.PAGE_SIZE
        start = (page - 1) * page_size
        return books[start:start+page_size]

    return books.all()


def books_count(cate_id=None, kw=None):
    books = Book.objects

    if cate_id:
        books = books.filter(categories__id=cate_id)
    if kw:
        books = books.filter(name__icontains=kw)

    return books.count()


def get_book_by_id(book_id):
    return Book.objects.get(pk=book_id)


def get_comments(book_id):
    return Comment.objects.filter(book_id=book_id)


def save_comment(book_id, user_id, content):
    comment = Comment.objects.create(book_id=book_id, user_id=user_id, content=content)
    return comment


def get_orders_by_user_id(user_id):
    orders = []
    summary = {
        'subtotal': 0,
        'discount': 0,
        'shipping': 0,
        'tax': 0,
        'total': 0
    }
    for i, o in enumerate(Order.objects.filter(customer_user_id=user_id).all()):
        details = OrderDetails.objects.filter(order_id=o.id).all()

        orders.append({
            'id': o.id,
            'created_date': o.created_date,
            'tax': o.tax_fee,
            'shipping': o.shipping_fee,
            'status': o.status,
            'customer': o.customer_user,
            'transaction': o.transaction,
            'detail0': details[0],
            'total_quantity': 0,
            'total_price': 0,
            'subtotal_price': 0
        })

        other_fee = o.tax_fee + o.shipping_fee
        for d in OrderDetails.objects.filter(order_id=o.id).all():
            orders[i]['total_quantity'] += d.quantity
            orders[i]['total_price'] += d.quantity * d.price + other_fee
            orders[i]['subtotal_price'] += d.quantity * d.book.price + other_fee

        summary['shipping'] += o.shipping_fee
        summary['tax'] += o.tax_fee
        summary['total'] += orders[i]['total_price']
        summary['subtotal'] += orders[i]['subtotal_price'] - other_fee
        summary['discount'] = +orders[i]['total_price'] - orders[i]['subtotal_price']

    return orders, summary


def get_order_by_order_id(order_id):
    o = Order.objects.get(pk=order_id)

    order = {
        'id': o.id,
        'created_date': o.created_date,
        'tax': o.tax_fee,
        'shipping': o.shipping_fee,
        'status': o.status,
        'customer': o.customer_user,
        'transaction': o.transaction,
        'details': OrderDetails.objects.filter(order_id=order_id).all(),
        'total_quantity': 0,
        'total_price':  o.tax_fee + o.shipping_fee,
        'subtotal_price': 0,
        'discount': 0
    }

    other_fee = order['tax'] + order['shipping']
    for d in OrderDetails.objects.filter(order_id=order_id).all():
        order['total_quantity'] += d.quantity
        order['total_price'] += d.quantity * d.price
        order['subtotal_price'] += d.quantity * d.book.price
    order['discount'] = order['total_price'] - order['subtotal_price'] - other_fee

    return order


def save_order_from_request(request, cart, is_paid=False):
    if cart:
        o = Order.objects.create(customer_user=request.user)
        if is_paid:
            staff = User.objects.filter(is_staff=True).all()[1]
            r = Receipt.objects.create(customer_user=request.user, staff_user=staff)

        for i, c in cart.items():
            OrderDetails.objects.create(order=o, quantity=c['quantity'], price=c['price'], book_id=c['id'])
            if is_paid:
                ReceiptDetails.objects.create(receipt=r, quantity=c['quantity'], price=c['price'], book_id=c['id'])

        return o


def get_order_details(order_id):
    return OrderDetails.objects.filter(order_id=order_id).all()


def save_transaction(transaction_id, bank_code, description):
    return Transaction.objects.create(transaction_id=transaction_id, bank_code=bank_code, description=description)


def update_order(order_id, status=None, transaction_id=None):
    order = Order.objects.get(id=order_id)

    if status:
        order.status = status
    if transaction_id:
        order.transaction_id = transaction_id

    order.save()
