from django.test import TestCase, Client, RequestFactory
from django.urls import reverse
from django.core.files.uploadedfile import SimpleUploadedFile
from django.contrib.auth.models import User
import json
from .models import Customer, Product, Order, OrderItem
from .utils import guestOrder

class ModelTests(TestCase):
    def setUp(self):
        self.customer = Customer.objects.create(name="C", email="c@example.com")
        self.product = Product.objects.create(name="P", regular_price=100, sale_price=80, digital=False)
        self.order = Order.objects.create(customer=self.customer, complete=False)
        self.item = OrderItem.objects.create(order=self.order, product=self.product, quantity=2)

    def test_order_item_total(self):
        self.assertEqual(self.item.get_total, 160)

    def test_order_totals_and_shipping(self):
        self.assertEqual(self.order.get_cart_total, 160)
        self.assertTrue(self.order.shipping)

    def test_product_discount_percentage(self):
        self.assertEqual(self.product.discount_percentage, 20)

class GuestCheckoutTests(TestCase):
    def setUp(self):
        self.product = Product.objects.create(name="PG", regular_price=50, digital=False)
        self.factory = RequestFactory()

    def test_guest_order_creates_customer_order_items(self):
        request = self.factory.post(reverse("process_order"))
        cart_cookie = json.dumps({str(self.product.id): {"quantity": 3}})
        request.COOKIES["cart"] = cart_cookie
        data = {"form": {"name": "Guest", "email": "guest@example.com"}}
        customer, order = guestOrder(request, data)
        self.assertIsNotNone(customer.id)
        self.assertEqual(customer.name, "Guest")
        self.assertEqual(order.orderitem_set.count(), 1)
        item = order.orderitem_set.first()
        self.assertEqual(item.quantity, 3)

class AuthFlowTests(TestCase):
    def test_register_and_login(self):
        client = Client()
        resp = client.post(reverse("register_customer"), data={
            "name": "User",
            "email": "user@example.com",
            "contact_number": "123",
            "password": "pass1234",
            "password_confirm": "pass1234",
        })
        self.assertEqual(resp.status_code, 302)
        self.assertTrue(User.objects.filter(username="user@example.com").exists())
        user = User.objects.get(username="user@example.com")
        self.assertTrue(Customer.objects.filter(user=user).exists())
        resp2 = client.post(reverse("login_user"), data={"email": "user@example.com", "password": "pass1234"})
        self.assertEqual(resp2.status_code, 302)
        resp3 = client.get(reverse("profile"))
        self.assertEqual(resp3.status_code, 200)

# Create your tests here.
