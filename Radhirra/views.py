from django.shortcuts import get_object_or_404, render, redirect
from .models import Order, OrderItem, Product, ShippingAddress, Category, Review
from .forms import ReviewForm

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
    try:
        data = cartData(request)
        cartItems = data["cartItems"]

        featured_products = Product.objects.filter(is_featured=True).prefetch_related('images', 'reviews')[:8]
        five_star_reviews = Review.objects.filter(rating=5).select_related('user', 'product').order_by('-created_at')[:10]
        context = {
            "featured_products": featured_products,
            "cartItems": cartItems,
            "five_star_reviews": five_star_reviews,
        }
    except Exception:
        context = {
            "featured_products": [],
            "cartItems": 0,
            "five_star_reviews": [],
        }
    return render(request, "index.html", context)


# Removed register_customer view - now handled by users app
# Removed login_user view - now handled by users app
# Removed profile view - now handled by users app
# Removed logout_user view - now handled by users app


def all_products(request):
    q = request.GET.get("q", "").strip()
    sort = request.GET.get("sort", "relevance")
    qs = Product.objects.select_related('category').prefetch_related('images')

    if q:
        import re
        price_match = re.search(r'\d+', q)
        
        q_obj = Q(name__icontains=q) | Q(category__name__icontains=q) | Q(sku__icontains=q)
        
        if price_match:
            price_value = float(price_match.group())
            price_range = price_value * 0.2
            q_obj |= Q(regular_price__range=(price_value - price_range, price_value + price_range)) | Q(sale_price__range=(price_value - price_range, price_value + price_range))
        
        qs = qs.filter(q_obj).annotate(
            relevance=Case(
                When(name__iexact=q, then=Value(5)),
                When(sku__iexact=q, then=Value(5)),
                When(category__name__iexact=q, then=Value(4)),
                When(name__istartswith=q, then=Value(3)),
                When(category__name__istartswith=q, then=Value(3)),
                default=Value(1),
                output_field=IntegerField(),
            )
        )

    qs = qs.annotate(
        effective_price=Case(
            When(sale_price__isnull=False, then=F("sale_price")),
            default=F("regular_price"),
        )
    )

    if sort == "price_asc":
        qs = qs.order_by("effective_price")
    elif sort == "price_desc":
        qs = qs.order_by("-effective_price")
    elif q:
        qs = qs.order_by("-relevance", "name")
    else:
        qs = qs.order_by("name")

    context = {
        "products": qs,
        "query": q,
        "results_count": qs.count(),
        "sort": sort,
        "categories": Category.objects.all(),
    }
    return render(request, "all_products.html", context)


def product_detail(request, pk):
    product = Product.objects.get(id=pk)
    reviews = product.reviews.all().order_by('-created_at')
    user_review = None
    
    if request.user.is_authenticated:
        user_review = reviews.filter(user=request.user).first()
    
    if request.method == 'POST' and request.user.is_authenticated:
        if user_review:
            form = ReviewForm(request.POST, instance=user_review)
        else:
            form = ReviewForm(request.POST)
        
        if form.is_valid():
            review = form.save(commit=False)
            review.product = product
            review.user = request.user
            review.save()
            return redirect('product_detail', pk=pk)
    else:
        form = ReviewForm(instance=user_review) if user_review else ReviewForm()
    
    recommended_products = Product.objects.exclude(id=pk)[:4]
    
    context = {
        'product': product,
        'reviews': reviews,
        'user_review': user_review,
        'form': form,
        'recommended_products': recommended_products
    }
    return render(request, 'product_detail.html', context)


def cart(request):
    cart = get_cart(request)
    items = cart.items.select_related("product").prefetch_related("product__images")
    
    # Calculate totals
    cart_total = sum(item.get_total for item in items)
    cart_items_count = sum(item.quantity for item in items)
    
    context = {
        "items": items,
        "cart_total": cart_total,
        "cart_items_count": cart_items_count,
        "cartItems": cart_items_count
    }
    return render(request, "cart_new.html", context)


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
    if not q or len(q) < 2:
        return JsonResponse({"suggestions": []})
    
    qs = Product.objects.filter(
        Q(name__istartswith=q) | Q(category__name__istartswith=q)
    ).select_related('category')[:5]
    
    data = [{
        "id": p.id, 
        "name": p.name, 
        "category": p.category.name if p.category else "",
        "price": str(p.sale_price if p.sale_price else p.regular_price)
    } for p in qs]
    
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
    items = cart.items.select_related("product").prefetch_related("product__images")
    
    # Calculate totals
    cart_total = sum(item.get_total for item in items)
    cart_items_count = sum(item.quantity for item in items)
    
    context = {
        "items": items,
        "cart_total": cart_total,
        "cart_items_count": cart_items_count,
        "cartItems": cart_items_count
    }
    return render(request, "cart_new.html", context)


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


def contact(request):
    data = cartData(request)
    cartItems = data["cartItems"]
    
    context = {"cartItems": cartItems}
    return render(request, "contacts.html", context)

def update_cart_item(request):
    if request.method == 'POST':
        import json
        data = json.loads(request.body)
        item_id = data.get('item_id')
        action = data.get('action')
        
        try:
            cart_item = CartItem.objects.get(id=item_id)
            
            if action == 'increase':
                cart_item.quantity += 1
                cart_item.save()
            elif action == 'decrease':
                if cart_item.quantity > 1:
                    cart_item.quantity -= 1
                    cart_item.save()
                else:
                    cart_item.delete()
                    return JsonResponse({'success': True, 'removed': True})
            elif action == 'remove':
                cart_item.delete()
                return JsonResponse({'success': True, 'removed': True})
            
            # Calculate new totals
            cart = cart_item.cart
            cart_total = sum(item.get_total for item in cart.items.all())
            cart_items_count = sum(item.quantity for item in cart.items.all())
            
            return JsonResponse({
                'success': True,
                'quantity': cart_item.quantity,
                'item_total': float(cart_item.get_total),
                'cart_total': float(cart_total),
                'cart_items_count': cart_items_count
            })
            
        except CartItem.DoesNotExist:
            return JsonResponse({'success': False, 'error': 'Item not found'})
    
    return JsonResponse({'success': False})
    if request.method == 'POST':
        import json
        data = json.loads(request.body)
        product_id = data.get('product_id')
        size = data.get('size')
        sleeve = data.get('sleeve')
        
        product = get_object_or_404(Product, id=product_id)
        cart = get_cart(request)
        
        # Check if item with same product, size, and sleeve exists
        cart_item, created = CartItem.objects.get_or_create(
            cart=cart,
            product=product,
            size=size,
            sleeve=sleeve,
            defaults={'quantity': 1}
        )
        
        if not created:
            cart_item.quantity += 1
            cart_item.save()
        
        cart_items = sum(item.quantity for item in cart.items.all())
        
        return JsonResponse({
            'success': True,
            'cart_items': cart_items,
            'message': 'Item added to cart'
        })
    
    return JsonResponse({'success': False})

def get_cart_items(request):
    cart = get_cart(request)
    items = cart.items.select_related("product").prefetch_related("product__images")
    
    cart_data = {
        'items': [],
        'cart_total': 0,
        'cart_items_count': 0
    }
    
    for item in items:
        image_url = item.product.main_image.image.url if item.product.main_image else '/static/images/no-image.png'
        cart_data['items'].append({
            'id': item.id,
            'name': item.product.name,
            'size': item.size or 'N/A',
            'sleeve': item.get_sleeve_display() if item.sleeve else 'N/A',
            'price': float(item.product.sale_price if item.product.sale_price else item.product.regular_price),
            'quantity': item.quantity,
            'total': float(item.get_total),
            'image': image_url
        })
    
    cart_data['cart_total'] = float(sum(item.get_total for item in items))
    cart_data['cart_items_count'] = sum(item.quantity for item in items)
    
    return JsonResponse(cart_data)

def add_to_cart_ajax(request):
    if request.method == 'POST':
        import json
        data = json.loads(request.body)
        product_id = data.get('product_id')
        size = data.get('size')
        sleeve = data.get('sleeve')
        
        product = get_object_or_404(Product, id=product_id)
        cart = get_cart(request)
        
        cart_item, created = CartItem.objects.get_or_create(
            cart=cart,
            product=product,
            size=size,
            sleeve=sleeve,
            defaults={'quantity': 1}
        )
        
        if not created:
            cart_item.quantity += 1
            cart_item.save()
        
        cart_items = sum(item.quantity for item in cart.items.all())
        
        return JsonResponse({
            'success': True,
            'cart_items': cart_items,
            'message': 'Item added to cart'
        })
    
    return JsonResponse({'success': False})