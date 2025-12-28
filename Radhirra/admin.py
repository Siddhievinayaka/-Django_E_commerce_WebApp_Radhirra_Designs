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
    extra = 1


class OrderItemInline(admin.TabularInline):
    model = OrderItem
    extra = 0
    readonly_fields = ('price_at_order', 'variant_info', 'user_note')


class ShippingAddressInline(admin.StackedInline):
    model = ShippingAddress
    extra = 0


class ProductAdmin(admin.ModelAdmin):
    inlines = [ProductImageInline]
    list_display = ('name', 'category', 'regular_price', 'sale_price', 'is_featured')
    list_filter = ('category', 'is_featured', 'is_new_arrival', 'is_best_seller')
    search_fields = ('name', 'sku')


class OrderAdmin(admin.ModelAdmin):
    inlines = [OrderItemInline, ShippingAddressInline]
    list_display = ('id', 'user', 'order_type', 'order_status', 'total_amount', 'date_ordered')
    list_filter = ('order_type', 'order_status', 'date_ordered')
    search_fields = ('id', 'user__username', 'contact_value')
    readonly_fields = ('date_ordered', 'updated_at', 'transaction_id')
    
    fieldsets = (
        ('Order Info', {
            'fields': ('user', 'order_type', 'order_status', 'total_amount', 'contact_value')
        }),
        ('Timestamps', {
            'fields': ('date_ordered', 'updated_at', 'transaction_id'),
            'classes': ('collapse',)
        }),
        ('Legacy', {
            'fields': ('complete',),
            'classes': ('collapse',)
        })
    )


# Register your models here.
admin.site.register(Category)
admin.site.register(Product, ProductAdmin)
admin.site.register(ProductImage)
admin.site.register(Order, OrderAdmin)
admin.site.register(OrderItem)
admin.site.register(ShippingAddress)
admin.site.register(Review)
