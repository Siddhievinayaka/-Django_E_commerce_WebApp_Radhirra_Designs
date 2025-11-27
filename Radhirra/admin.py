from django.contrib import admin
from .models import (
    Product,
    ProductImage,
    Order,
    OrderItem,
    ShippingAddress,
    Category,
)  # Removed Customer, Added Category


class ProductImageInline(admin.TabularInline):
    model = ProductImage
    extra = 1  # Number of extra forms to display


class ProductAdmin(admin.ModelAdmin):
    inlines = [ProductImageInline]


# Register your models here.
# admin.site.register(Customer) # Removed Customer registration
admin.site.register(Category)  # Register the new Category model
admin.site.register(Product, ProductAdmin)
admin.site.register(ProductImage)
admin.site.register(Order)
admin.site.register(OrderItem)
admin.site.register(ShippingAddress)
