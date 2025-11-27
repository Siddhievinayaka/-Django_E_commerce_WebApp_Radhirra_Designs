from django.urls import path
from . import views

app_name = "dashboard"

urlpatterns = [
    path("login/", views.AdminLoginView.as_view(), name="admin_login"),
    path("logout/", views.admin_logout, name="admin_logout"),
    path("", views.dashboard_home, name="home"),
    path("products/", views.product_list, name="product_list"),
    path("products/add/", views.product_add, name="product_add"),
    path("products/edit/<int:pk>/", views.product_edit, name="product_edit"),
    path("products/delete/<int:pk>/", views.product_delete, name="product_delete"),
    path("categories/", views.category_list, name="category_list"),
    path("categories/add/", views.category_add, name="category_add"),
    path("categories/edit/<int:pk>/", views.category_edit, name="category_edit"),
    path("categories/delete/<int:pk>/", views.category_delete, name="category_delete"),
]
