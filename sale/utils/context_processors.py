from bookstore import settings


def count_cart(request):
    total_amount, total_quantity = 0, 0

    cart = request.session.get(settings.SALE_CART_KEY)

    if cart:
        for i, c in cart.items():
            total_quantity += int(c['quantity'])
            total_amount += int(c['quantity']) * int(c['price'])
    return {
        "sale_total_amount": total_amount,
        "sale_total_quantity": total_quantity
    }
