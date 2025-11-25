from . import views
from django.urls import path

urlpatterns = [
    path("", views.index, name="index"),
    path("register/", views.register_customer, name="register_customer"),
    path("login/", views.login_user, name="login_user"),
    path("profile/", views.profile, name="profile"),
    path("logout/", views.logout_user, name="logout_user"),
    path("products/", views.all_products, name="all_products"),
    path("product/<int:pk>/", views.product_detail, name="product_detail"),
    path("cart/", views.cart, name="cart"),
    path("checkout/", views.checkout, name="checkout"),
    path("update_item/", views.updateItem, name="update_item"),
    path("process_order/", views.processOrder, name="process_order"),
    path("search_suggest/", views.search_suggest, name="search_suggest"),
]
