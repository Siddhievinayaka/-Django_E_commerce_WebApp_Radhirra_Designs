import json
from .models import *


def cookieCart(request):
    try:
        cart = json.loads(request.COOKIES["cart"])
    except:
        cart = {}

    items = []
    order = {"get_cart_total": 0, "get_cart_items": 0, "shipping": False}
    cartItems = order["get_cart_items"]

    for i in cart:
        try:
            cartItems += cart[i]["quantity"]

            product = Product.objects.get(id=i)
            price = product.sale_price if product.sale_price else product.regular_price
            total = price * cart[i]["quantity"]

            order["get_cart_total"] += total
            order["get_cart_items"] += cart[i]["quantity"]

            item = {
                "product": {
                    "id": product.id,
                    "name": product.name,
                    "price": price,
                    "imageURL": product.imageURL,
                },
                "quantity": cart[i]["quantity"],
                "get_total": total,
            }
            items.append(item)

            if product.digital == False:
                order["shipping"] = True
        except:
            pass
    return {"cartItems": cartItems, "order": order, "items": items}


def cartData(request):
    if request.user.is_authenticated:
        # Changed from customer = request.user.customer to user = request.user
        user = request.user
        # Fix: Handle multiple incomplete orders by getting the first one or creating new
        order = Order.objects.filter(user=user, complete=False).first()
        if not order:
            order = Order.objects.create(user=user, complete=False)
        items = order.orderitem_set.all()
        cartItems = order.get_cart_items
    else:
        cookieData = cookieCart(request)
        cartItems = cookieData["cartItems"]
        order = cookieData["order"]
        items = cookieData["items"]
    return {"cartItems": cartItems, "order": order, "items": items}


def guestOrder(request, data):
    name = data["form"]["name"]
    email = data["form"]["email"]

    cookieData = cookieCart(request)
    items = cookieData["items"]

    # Since Customer model is removed, we'll use CustomUser or handle as anonymous
    # For now, let's assume we create a user if not exists or use an anonymous user
    # This part might need further refinement based on how you want to handle guest users
    # For simplicity, I'm creating a placeholder user or associating with an existing one
    # You might want to create a proper CustomUser if you want to store guest info
    from users.models import CustomUser  # Import CustomUser model

    user, created = CustomUser.objects.get_or_create(email=email)
    if created:
        user.username = email  # Or generate a unique username
        user.set_unusable_password()  # Guest users don't need a password
        user.save()

    order = Order.objects.create(
        user=user,  # Changed customer=customer to user=user
        complete=False,
    )

    for item in items:
        product = Product.objects.get(id=item["product"]["id"])

        orderItem = OrderItem.objects.create(
            product=product, order=order, quantity=item["quantity"]
        )
    return user, order


def get_sections():
    """
    Returns a list of static sections for the homepage.
    """
    return [
        "New Arrival",
        "Only skirts",
        "Lehenga Sets–Gopidresses",
    ]
