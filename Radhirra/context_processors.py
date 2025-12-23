from .models import Category, Cart


def categories_processor(request):
    """
    Makes the list of all categories available to every template.
    """
    categories = Category.objects.all()
    return {"categories": categories}


def cart_items_processor(request):
    """
    Makes cart items count available to every template.
    """
    if request.user.is_authenticated:
        cart = Cart.objects.filter(user=request.user).first()
    else:
        session_key = request.session.session_key
        cart = Cart.objects.filter(session_key=session_key).first() if session_key else None
    
    cart_items = sum(item.quantity for item in cart.items.all()) if cart else 0
    return {"cartItems": cart_items}
