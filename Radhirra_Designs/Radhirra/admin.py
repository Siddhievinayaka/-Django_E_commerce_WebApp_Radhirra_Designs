from django.contrib import admin
from .models import Customer, Product, ProductImage, Order, OrderItem, ShippingAddress


class ProductImageInline(admin.TabularInline):
    model = ProductImage
    extra = 1  # Number of extra forms to display


class ProductAdmin(admin.ModelAdmin):
    inlines = [ProductImageInline]


# Register your models here.
admin.site.register(Customer)
admin.site.register(Product, ProductAdmin)
admin.site.register(ProductImage)
admin.site.register(Order)
admin.site.register(OrderItem)
admin.site.register(ShippingAddress)
