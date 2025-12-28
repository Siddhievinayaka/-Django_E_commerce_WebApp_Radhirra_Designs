from django.db import models
from django.conf import settings  # Import settings to get AUTH_USER_MODEL
from cloudinary.models import CloudinaryField
from django.utils.text import slugify

# Create your models here.


# Removed the Customer model as it's replaced by UserProfile in the 'users' app


class Category(models.Model):  # New Category Model
    name = models.CharField(max_length=120, unique=True)
    slug = models.SlugField(max_length=120, unique=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        verbose_name_plural = "Categories"  # Correct pluralization

    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(self.name)
        super().save(*args, **kwargs)

    def __str__(self):
        return self.name


class Product(models.Model):
    SIZE_CHOICES = [
        ("XS", "XS"),
        ("S", "S"),
        ("M", "M"),
        ("L", "L"),
        ("XL", "XL"),
        ("XXL", "XXL"),
    ]
    
    SLEEVE_CHOICES = [
        ("sleeveless", "Sleeveless"),
        ("short", "Short"),
        ("3/4", "3/4"),
    ]

    category = models.ForeignKey(
        Category,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name="products",
    )  # Added category
    name = models.CharField(max_length=200)
    sku = models.CharField(max_length=50, unique=True, null=True, blank=True)
    regular_price = models.DecimalField(max_digits=10, decimal_places=2)
    sale_price = models.DecimalField(
        max_digits=10, decimal_places=2, null=True, blank=True
    )
    description = models.TextField(blank=True, null=True)
    size = models.CharField(max_length=3, choices=SIZE_CHOICES, null=True, blank=True)
    sleeve = models.CharField(max_length=20, choices=SLEEVE_CHOICES, null=True, blank=True)
    material = models.CharField(max_length=100, null=True, blank=True)
    specifications = models.TextField(blank=True, null=True)
    seller_information = models.TextField(blank=True, null=True)
    is_featured = models.BooleanField(default=False)
    is_new_arrival = models.BooleanField(default=False)
    is_best_seller = models.BooleanField(default=False)

    def __str__(self):
        return self.name

    @property
    def main_image(self):
        return self.images.filter(is_main=True).first()

    @property
    def discount_percentage(self):
        if self.sale_price and self.regular_price:
            return round(
                ((self.regular_price - self.sale_price) / self.regular_price) * 100
            )
        return 0


class ProductImage(models.Model):
    product = models.ForeignKey(
        Product, related_name="images", on_delete=models.CASCADE
    )
    image = CloudinaryField("image")
    is_main = models.BooleanField(default=False)

    def __str__(self):
        return f"Image for {self.product.name}"

    @property
    def thumbnail_url(self):
        return self.image.build_url(width=200, height=200, crop="thumb")


class Order(models.Model):
    ORDER_TYPE_CHOICES = [
        ('whatsapp', 'WhatsApp'),
        ('email', 'Email'),
    ]
    
    ORDER_STATUS_CHOICES = [
        ('pending', 'Pending'),
        ('confirmed', 'Confirmed'),
        ('completed', 'Completed'),
        ('cancelled', 'Cancelled'),
    ]
    
    user = models.ForeignKey(
        settings.AUTH_USER_MODEL, on_delete=models.SET_NULL, null=True, blank=True
    )
    date_ordered = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    complete = models.BooleanField(default=False)  # Keep for backward compatibility
    transaction_id = models.CharField(max_length=100, null=True)
    
    # New fields for WhatsApp/Email checkout
    order_type = models.CharField(max_length=10, choices=ORDER_TYPE_CHOICES, default='whatsapp')
    order_status = models.CharField(max_length=10, choices=ORDER_STATUS_CHOICES, default='pending')
    total_amount = models.DecimalField(max_digits=10, decimal_places=2, default=0)
    contact_value = models.CharField(max_length=255, null=True, blank=True)  # phone or email

    def __str__(self):
        return f"Order #{self.id} - {self.get_order_status_display()}"
    
    def save(self, *args, **kwargs):
        # Auto-calculate total_amount if not set
        if not self.total_amount and self.pk:
            self.total_amount = self.get_cart_total
        super().save(*args, **kwargs)

    @property
    def shipping(self):
        shipping = False
        orderitems = self.orderitem_set.all()
        for i in orderitems:
            if i.product.digital == False:
                shipping = True
        return shipping

    @property
    def get_cart_total(self):
        orderitems = self.orderitem_set.all()
        total = sum([item.get_total for item in orderitems])
        return total

    @property
    def get_cart_items(self):
        orderitems = self.orderitem_set.all()
        total = sum([item.quantity for item in orderitems])
        return total


class OrderItem(models.Model):
    product = models.ForeignKey(Product, on_delete=models.SET_NULL, null=True)
    order = models.ForeignKey(Order, on_delete=models.SET_NULL, null=True)
    quantity = models.IntegerField(default=0, null=True, blank=True)
    date_added = models.DateTimeField(auto_now_add=True)
    
    # New fields for order snapshot
    price_at_order = models.DecimalField(max_digits=10, decimal_places=2, default=0)
    variant_info = models.CharField(max_length=255, null=True, blank=True)  # size/color/customization
    user_note = models.TextField(null=True, blank=True)  # User's order note

    @property
    def get_total(self):
        # Use price_at_order if available, otherwise current product price
        if self.price_at_order:
            return self.price_at_order * self.quantity
        price = (
            self.product.sale_price
            if self.product.sale_price
            else self.product.regular_price
        )
        return price * self.quantity


class ShippingAddress(models.Model):
    user = models.ForeignKey(
        settings.AUTH_USER_MODEL, on_delete=models.SET_NULL, null=True, blank=True
    )
    order = models.ForeignKey(Order, on_delete=models.SET_NULL, null=True)
    address = models.CharField(max_length=200, null=True, blank=True)  # Allow empty initially
    city = models.CharField(max_length=200, null=True, blank=True)
    state = models.CharField(max_length=200, null=True, blank=True)
    zipcode = models.CharField(max_length=200, null=True, blank=True)
    phone_number = models.CharField(max_length=20, null=True, blank=True)
    date_added = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.address or f"Address for Order #{self.order.id if self.order else 'Unknown'}"


class Cart(models.Model):
    user = models.ForeignKey(
        settings.AUTH_USER_MODEL, null=True, blank=True, on_delete=models.CASCADE
    )
    session_key = models.CharField(max_length=40, null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Cart ({self.user or self.session_key})"


class CartItem(models.Model):
    cart = models.ForeignKey(Cart, related_name="items", on_delete=models.CASCADE)
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    quantity = models.PositiveIntegerField(default=1)
    size = models.CharField(max_length=3, choices=Product.SIZE_CHOICES, null=True, blank=True)
    sleeve = models.CharField(max_length=20, choices=Product.SLEEVE_CHOICES, null=True, blank=True)

    def __str__(self):
        return f"{self.quantity} x {self.product.name}"
    
    @property
    def get_total(self):
        price = self.product.sale_price if self.product.sale_price else self.product.regular_price
        return price * self.quantity

class Review(models.Model):
    RATING_CHOICES = [
        (1, '1 Star'),
        (2, '2 Stars'),
        (3, '3 Stars'),
        (4, '4 Stars'),
        (5, '5 Stars'),
    ]
    
    product = models.ForeignKey(Product, related_name='reviews', on_delete=models.CASCADE)
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    rating = models.IntegerField(choices=RATING_CHOICES)
    comment = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)
    
    class Meta:
        unique_together = ('product', 'user')
    
    def __str__(self):
        return f'{self.user.username} - {self.product.name} ({self.rating} stars)'