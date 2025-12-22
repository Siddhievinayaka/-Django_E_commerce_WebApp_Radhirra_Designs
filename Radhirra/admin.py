from django.contrib import admin
from .models import (
    Product,
    ProductImage,
    Order,
    OrderItem,
    ShippingAddress,
    Category,
    Review,
)


class ProductImageInline(admin.TabularInline):
    model = ProductImage
    extra = 1  # Number of extra forms to display


class ProductAdmin(admin.ModelAdmin):
    inlines = [ProductImageInline]


# Register your models here.
admin.site.register(Category)
admin.site.register(Product, ProductAdmin)
admin.site.register(ProductImage)
admin.site.register(Order)
admin.site.register(OrderItem)
admin.site.register(ShippingAddress)
admin.site.register(Review)
