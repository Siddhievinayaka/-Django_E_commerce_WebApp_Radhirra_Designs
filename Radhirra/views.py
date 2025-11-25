from django.shortcuts import render, redirect
from .models import Customer, Order, OrderItem, Product, ShippingAddress
from .form import CustomerForm
from django.contrib.auth.models import User
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.http import JsonResponse
from django.db.models import Q, Case, When, Value, IntegerField, F
import json
import datetime
from Radhirra.utils import cookieCart, cartData, guestOrder


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


def register_customer(request):
    form = CustomerForm()
    if request.method == "POST":
        form = CustomerForm(request.POST, request.FILES)
        if form.is_valid():
            # Create a new User instance
            user = User.objects.create_user(
                username=form.cleaned_data["email"],
                email=form.cleaned_data["email"],
                password=form.cleaned_data["password"],
            )
            user.save()

            # Save the Customer instance and link it to the User
            customer = form.save(commit=False)
            customer.user = user
            customer.save()

            return redirect("login_user")

    context = {"form": form}
    return render(request, "forms/register_customer.html", context)


def login_user(request):
    if request.method == "POST":
        email = request.POST.get("email")
        password = request.POST.get("password")

        user = authenticate(request, username=email, password=password)

        if user is not None:
            login(request, user)
            return redirect("index")
        else:
            # Authentication failed
            return render(
                request, "forms/login.html", {"error_message": "Invalid credentials"}
            )
    return render(request, "forms/login.html")


@login_required
def profile(request):
    customer = Customer.objects.get(user=request.user)
    context = {"customer": customer}
    return render(request, "profile.html", context)


def logout_user(request):
    logout(request)
    return redirect("index")


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
        )
        qs = qs.filter(q_obj)

        relevance = (
            Case(When(name__icontains=q, then=Value(3)), default=Value(0), output_field=IntegerField())
            + Case(When(sku__icontains=q, then=Value(3)), default=Value(0), output_field=IntegerField())
            + Case(When(description__icontains=q, then=Value(2)), default=Value(0), output_field=IntegerField())
            + Case(When(material__icontains=q, then=Value(1)), default=Value(0), output_field=IntegerField())
            + Case(When(specifications__icontains=q, then=Value(1)), default=Value(0), output_field=IntegerField())
            + Case(When(seller_information__icontains=q, then=Value(1)), default=Value(0), output_field=IntegerField())
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

    context = {"products": qs, "query": q, "results_count": qs.count(), "sort": sort}
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

    customer = request.user.customer
    product = Product.objects.get(id=productId)
    order, created = Order.objects.get_or_create(customer=customer, complete=False)
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
        customer = request.user.customer
        order, created = Order.objects.get_or_create(customer=customer, complete=False)
    else:
        customer, order = guestOrder(request, data)

    total = float(data["form"]["total"])
    order.transaction_id = transaction_id

    if total == order.get_cart_total:
        order.complete = True
    order.save()

    if order.shipping == True:
        ShippingAddress.objects.create(
            customer=customer,
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
    qs = (
        Product.objects.filter(Q(name__icontains=q) | Q(sku__icontains=q))
        .order_by("name")[:5]
    )
    data = [
        {"id": p.id, "name": p.name, "sku": p.sku, "image": p.imageURL}
        for p in qs
    ]
    return JsonResponse({"suggestions": data})
