from . import views
from django.urls import path

urlpatterns = [
    path("", views.index, name="index"),
    path("products/", views.all_products, name="all_products"),
    path("product/<int:pk>/", views.product_detail, name="product_detail"),
    path("cart/", views.cart, name="cart"),
    path("checkout/", views.checkout, name="checkout"),
    path("contact/", views.contact, name="contact"),
    path("add_to_cart/", views.add_to_cart_ajax, name="add_to_cart_ajax"),
    path("get_cart_items/", views.get_cart_items, name="get_cart_items"),
    path("update_cart_item/", views.update_cart_item, name="update_cart_item"),
    path("update_item/", views.updateItem, name="update_item"),
    path("process_order/", views.processOrder, name="process_order"),
    path("search_suggest/", views.search_suggest, name="search_suggest"),
]

urlpatterns += [
    path("cart/", views.cart_detail, name="cart_detail"),
    path("cart/add/<int:product_id>/", views.add_to_cart, name="add_to_cart"),
    path("cart/remove/<int:item_id>/", views.remove_from_cart, name="remove_from_cart"),
    path("cart/update/<int:item_id>/", views.update_quantity, name="update_quantity"),
]
