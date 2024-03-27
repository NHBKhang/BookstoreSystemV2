from core.models import Category


def categories(request):
    categories = Category.objects.all()

    return {'categories': categories}


def count_cart(request):
    total_amount, total_quantity = 0, 0

    cart = request.session.get('cart')

    if cart:
        for i, c in cart.items():
            print(i, c)
            total_quantity += int(c['quantity'])
            total_amount += int(c['quantity']) * int(c['price'])

    return {
        "total_amount": total_amount,
        "total_quantity": total_quantity
    }

