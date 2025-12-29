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
    path("get_cart_drawer/", views.get_cart_drawer, name="get_cart_drawer"),
    path("get_cart_items/", views.get_cart_items, name="get_cart_items"),
    path("update_cart_item/", views.update_cart_item, name="update_cart_item"),
    path("update_item/", views.updateItem, name="update_item"),
    path("process_order/", views.processOrder, name="process_order"),
    path("search_suggest/", views.search_suggest, name="search_suggest"),
    # New WhatsApp/Email order endpoints
    path("create_whatsapp_order/", views.create_whatsapp_order, name="create_whatsapp_order"),
    path("create_email_order/", views.create_email_order, name="create_email_order"),
    path("my_orders/", views.my_orders, name="my_orders"),
    path("get_user_orders/", views.get_user_orders, name="get_user_orders"),
    path("get_order_details/<int:order_id>/", views.get_order_details, name="get_order_details"),
    path("cancel_order/<int:order_id>/", views.cancel_order, name="cancel_order"),
    path("reorder_items/<int:order_id>/", views.reorder_items, name="reorder_items"),
]

urlpatterns += [
    path("cart/", views.cart_detail, name="cart_detail"),
    path("cart/add/<int:product_id>/", views.add_to_cart, name="add_to_cart"),
    path("cart/remove/<int:item_id>/", views.remove_from_cart, name="remove_from_cart"),
    path("cart/update/<int:item_id>/", views.update_quantity, name="update_quantity"),
]
