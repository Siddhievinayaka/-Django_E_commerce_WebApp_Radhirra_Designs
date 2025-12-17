from django.shortcuts import get_object_or_404, render, redirect
from .models import Order, OrderItem, Product, ShippingAddress, Category

# from .form import CustomerForm # This form is no longer needed here
from django.contrib.auth.models import (
    User,
)  # This might not be needed if using CustomUser directly
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.http import JsonResponse
from django.db.models import Q, Case, When, Value, IntegerField, F
import json
import datetime
from Radhirra.utils import cookieCart, cartData, guestOrder
from .models import Cart, CartItem, Product


# Create your views here.
def index(request):
    data = cartData(request)
    cartItems = data["cartItems"]

    products = Product.objects.all()
    context = {
        "products": products,
        "cartItems": cartItems,
        "autumn_products": products[:4],
        "summer_products": products[4:6],
        "ajrakh_products": products[6:10],
    }
    return render(request, "index.html", context)


# Removed register_customer view - now handled by users app
# Removed login_user view - now handled by users app
# Removed profile view - now handled by users app
# Removed logout_user view - now handled by users app


def all_products(request):
    q = request.GET.get("q", "").strip()
    sort = request.GET.get("sort", "relevance")
    qs = Product.objects.all()

    if q:
        q_obj = (
            Q(name__icontains=q)
            | Q(description__icontains=q)
            | Q(material__icontains=q)
            | Q(specifications__icontains=q)
            | Q(seller_information__icontains=q)
            | Q(sku__icontains=q)
            | Q(size__icontains=q)
            | Q(category__name__icontains=q)
        )
        qs = qs.filter(q_obj)

        relevance = (
            Case(
                When(name__icontains=q, then=Value(3)),
                default=Value(0),
                output_field=IntegerField(),
            )
            + Case(
                When(sku__icontains=q, then=Value(3)),
                default=Value(0),
                output_field=IntegerField(),
            )
            + Case(
                When(description__icontains=q, then=Value(2)),
                default=Value(0),
                output_field=IntegerField(),
            )
            + Case(
                When(material__icontains=q, then=Value(1)),
                default=Value(0),
                output_field=IntegerField(),
            )
            + Case(
                When(specifications__icontains=q, then=Value(1)),
                default=Value(0),
                output_field=IntegerField(),
            )
            + Case(
                When(seller_information__icontains=q, then=Value(1)),
                default=Value(0),
                output_field=IntegerField(),
            )
        )
        qs = qs.annotate(relevance=relevance)

    effective_price = Case(
        When(sale_price__isnull=False, then=F("sale_price")),
        default=F("regular_price"),
    )
    qs = qs.annotate(effective_price=effective_price)

    if sort == "price_asc":
        qs = qs.order_by("effective_price")
    elif sort == "price_desc":
        qs = qs.order_by("-effective_price")
    else:
        if q:
            qs = qs.order_by("-relevance", "name")
        else:
            qs = qs.order_by("name")

    context = {
        "products": qs,
        "query": q,
        "results_count": qs.count(),
        "sort": sort,
    }
    return render(request, "all_products.html", context)


def product_detail(request, pk):
    product = Product.objects.get(id=pk)
    # Fetch all other products to recommend, excluding the current one
    recommended_products = Product.objects.exclude(id=pk)

    context = {"product": product, "recommended_products": recommended_products}
    return render(request, "product_detail.html", context)


def cart(request):
    data = cartData(request)
    cartItems = data["cartItems"]
    order = data["order"]
    items = data["items"]

    context = {"items": items, "order": order, "cartItems": cartItems}
    return render(request, "cart.html", context)


def checkout(request):
    data = cartData(request)
    cartItems = data["cartItems"]
    order = data["order"]
    items = data["items"]

    context = {"items": items, "order": order, "cartItems": cartItems}
    return render(request, "checkout.html", context)


def updateItem(request):
    data = json.loads(request.body)
    productId = data["productId"]
    action = data["action"]

    # Changed from customer = request.user.customer to user = request.user
    user = request.user
    product = Product.objects.get(id=productId)
    order, created = Order.objects.get_or_create(
        user=user, complete=False
    )  # Changed customer=customer to user=user
    orderItem, created = OrderItem.objects.get_or_create(order=order, product=product)

    if action == "add":
        orderItem.quantity = orderItem.quantity + 1
    elif action == "remove":
        orderItem.quantity = orderItem.quantity - 1
    elif action == "remove_item":
        orderItem.quantity = 0

    orderItem.save()

    if orderItem.quantity <= 0:
        orderItem.delete()
    return JsonResponse("Item was added", safe=False)


def processOrder(request):
    transaction_id = datetime.datetime.now().timestamp()
    data = json.loads(request.body)

    if request.user.is_authenticated:
        # Changed from customer = request.user.customer to user = request.user
        user = request.user
        order, created = Order.objects.get_or_create(
            user=user, complete=False
        )  # Changed customer=customer to user=user
    else:
        # guestOrder function might need to be updated to handle user instead of customer
        user, order = guestOrder(request, data)  # This function might need review

    total = float(data["form"]["total"])
    order.transaction_id = transaction_id

    if total == order.get_cart_total:
        order.complete = True
    order.save()

    if order.shipping == True:
        ShippingAddress.objects.create(
            user=user,  # Changed customer=customer to user=user
            order=order,
            address=data["shipping"]["address"],
            city=data["shipping"]["city"],
            state=data["shipping"]["state"],
            zipcode=data["shipping"]["zipcode"],
        )
    return JsonResponse("Payment complete!", safe=False)


def search_suggest(request):
    q = request.GET.get("q", "").strip()
    if not q:
        return JsonResponse({"suggestions": []})
    qs = Product.objects.filter(Q(name__icontains=q) | Q(sku__icontains=q)).order_by(
        "name"
    )[:5]
    data = [{"id": p.id, "name": p.name, "sku": p.sku, "image": p.imageURL} for p in qs]
    return JsonResponse({"suggestions": data})


def get_cart(request):
    if request.user.is_authenticated:
        cart, created = Cart.objects.get_or_create(user=request.user)
    else:
        if not request.session.session_key:
            request.session.save()
        cart, created = Cart.objects.get_or_create(
            session_key=request.session.session_key
        )
    return cart


def add_to_cart(request, product_id):
    cart = get_cart(request)
    product = get_object_or_404(Product, id=product_id)
    item, created = CartItem.objects.get_or_create(cart=cart, product=product)
    if not created:
        item.quantity += 1
        item.save()
    return redirect("cart_detail")


def remove_from_cart(request, item_id):
    item = get_object_or_404(CartItem, id=item_id)
    item.delete()
    return redirect("cart_detail")


def update_quantity(request, item_id):
    item = get_object_or_404(CartItem, id=item_id)
    if request.method == "POST":
        quantity = int(request.POST.get("quantity", 1))
        item.quantity = quantity
        item.save()
    return redirect("cart_detail")


def cart_detail(request):
    cart = get_cart(request)
    items = cart.items.select_related("product")
    return render(request, "cart.html", {"cart": cart, "items": items})


def move_session_cart_to_user_cart(request, user):
    session_key = request.session.session_key
    if not session_key:
        return
    try:
        session_cart = Cart.objects.get(session_key=session_key, user__isnull=True)
        user_cart, created = Cart.objects.get_or_create(user=user)
        for item in session_cart.items.all():
            user_item, created = CartItem.objects.get_or_create(
                cart=user_cart, product=item.product
            )
            if not created:
                user_item.quantity += item.quantity
                user_item.save()
            else:
                user_item.quantity = item.quantity
                user_item.save()
        session_cart.delete()
    except Cart.DoesNotExist:
        pass
