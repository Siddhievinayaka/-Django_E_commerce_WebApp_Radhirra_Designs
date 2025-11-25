from django.db import models
from django.contrib.auth.models import User

# Create your models here.


class Customer(models.Model):
    user = models.OneToOneField(User, null=True, blank=True, on_delete=models.CASCADE)
    name = models.CharField(max_length=200, null=True)
    email = models.CharField(max_length=200, null=True)
    contact_number = models.CharField(max_length=20, null=True, blank=True)
    profile_pic = models.ImageField(
        upload_to="profile_pics/",
        default="profile_pics/default.png",
        null=True,
        blank=True,
    )

    def __str__(self):
        return self.name

    @property
    def imageURL(self):
        try:
            url = self.profile_pic.url
        except:
            url = ""
        return url


class Product(models.Model):
    SIZE_CHOICES = [
        ("S", "S"),
        ("M", "M"),
        ("L", "L"),
        ("XL", "XL"),
        ("XXL", "XXL"),
    ]

    name = models.CharField(max_length=200)
    sku = models.CharField(max_length=50, unique=True, null=True, blank=True)
    regular_price = models.DecimalField(max_digits=10, decimal_places=2)
    sale_price = models.DecimalField(
        max_digits=10, decimal_places=2, null=True, blank=True
    )
    description = models.TextField(blank=True, null=True)
    size = models.CharField(max_length=3, choices=SIZE_CHOICES, null=True, blank=True)
    material = models.CharField(max_length=100, null=True, blank=True)
    specifications = models.TextField(blank=True, null=True)
    seller_information = models.TextField(blank=True, null=True)
    image = models.ImageField(upload_to="products/", null=True, blank=True)
    digital = models.BooleanField(default=False, null=True, blank=True)

    def __str__(self):
        return self.name

    @property
    def imageURL(self):
        try:
            url = self.image.url
        except:
            url = ""
        return url

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
    image = models.ImageField(upload_to="products/")

    def __str__(self):
        return f"Image for {self.product.name}"


class Order(models.Model):
    customer = models.ForeignKey(
        Customer, on_delete=models.SET_NULL, null=True, blank=True
    )
    date_ordered = models.DateTimeField(auto_now_add=True)
    complete = models.BooleanField(default=False)
    transaction_id = models.CharField(max_length=100, null=True)

    def __str__(self):
        return str(self.id)

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

    @property
    def get_total(self):
        price = (
            self.product.sale_price
            if self.product.sale_price
            else self.product.regular_price
        )
        total = price * self.quantity
        return total


class ShippingAddress(models.Model):
    customer = models.ForeignKey(Customer, on_delete=models.SET_NULL, null=True)
    order = models.ForeignKey(Order, on_delete=models.SET_NULL, null=True)
    address = models.CharField(max_length=200, null=False)
    city = models.CharField(max_length=200, null=False)
    state = models.CharField(max_length=200, null=False)
    zipcode = models.CharField(max_length=200, null=False)
    date_added = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.address
