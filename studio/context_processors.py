def cart(request):
    """Context processor для корзины (доступно во всех шаблонах)"""
    cart_items = []
    total_cart_price = 0
    cart_count = 0
    
    if request.user.is_authenticated:
        cart_items = request.user.cart_items.all()
        total_cart_price = sum(item.get_total_price() for item in cart_items)
        cart_count = cart_items.count()
    
    return {
        'cart_items': cart_items,
        'total_cart_price': total_cart_price,
        'cart_count': cart_count,
    }

