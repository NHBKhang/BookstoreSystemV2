import datetime

from core.models import Category
from bookstore import settings


def categories(request):
    categories = Category.objects.all()

    return {'categories': categories}


def count_cart(request):
    total_amount, total_quantity = 0, 0

    cart = request.session.get(settings.CART_KEY)

    if cart:
        for i, c in cart.items():
            total_quantity += int(c['quantity'])
            total_amount += int(c['quantity']) * int(c['price'])

    return {
        "total_amount": total_amount,
        "total_quantity": total_quantity
    }


def today(request):
    return {
        'today': datetime.datetime.now()
    }
