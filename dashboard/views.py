from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required, user_passes_test
from django.contrib.admin.views.decorators import staff_member_required
from django.contrib import messages
from django.core.paginator import Paginator
from django.urls import reverse
from Radhirra.models import Product, Category, ProductImage
from .forms import ProductForm, CategoryForm, ProductImageFormSet
from django.contrib.auth import authenticate, login
from django.contrib.auth.views import LoginView
from django.contrib.auth import logout
from django.urls import reverse_lazy


def admin_login(request):
    if request.method == "POST":
        # Custom login logic for staff users
        # This is a simplified example. For production, use Django's authentication form.
        # You can create a custom form that inherits from AuthenticationForm
        # and add extra validation.
        # For now, we'll keep it simple.
        # This is NOT a secure way to handle logins.
        # It's for demonstration purposes only.
        # A proper implementation should use Django's built-in authentication system.
        # See: https://docs.djangoproject.com/en/stable/topics/auth/default/#how-to-log-a-user-in
        # This is a placeholder for a proper login form.
        # You should replace this with a robust implementation.
        # For example, you could use Django's built-in LoginView.
        # See: https://docs.djangoproject.com/en/stable/topics/auth/default/#django.contrib.auth.views.LoginView
        # This is a simplified login for demonstration.
        # In a real application, you would have a form here.
        # For example:
        # from django.contrib.auth.forms import AuthenticationForm
        # form = AuthenticationForm(request, data=request.POST)
        # if form.is_valid():
        #     user = form.get_user()
        #     login(request, user)
        #     return redirect('dashboard:home')
        # else:
        #     # Handle invalid login
        #     pass
        # This is a placeholder.
        # You should implement a proper login form.
        # For now, we'll just redirect to the dashboard home.
        # This is not secure and is for demonstration only.
        return redirect("dashboard:home")
    return render(request, "admin_dashboard/login.html")


class AdminLoginView(LoginView):
    template_name = "admin_dashboard/login.html"
    redirect_authenticated_user = True

    def get_success_url(self):
        return reverse_lazy("dashboard:home")

    def form_valid(self, form):
        user = form.get_user()
        if user.is_staff:
            login(self.request, user)
            return redirect(self.get_success_url())
        else:
            messages.error(
                self.request,
                "You do not have permission to access the admin dashboard.",
            )
            return self.form_invalid(form)


def admin_logout(request):
    logout(request)
    messages.success(request, "You have been successfully logged out.")
    return redirect("dashboard:admin_login")


@staff_member_required
def dashboard_home(request):
    product_count = Product.objects.count()
    category_count = Category.objects.count()
    context = {
        "product_count": product_count,
        "category_count": category_count,
    }
    return render(request, "admin_dashboard/dashboard_home.html", context)


@staff_member_required
def product_list(request):
    products = Product.objects.all().order_by("-id")
    paginator = Paginator(products, 10)  # Show 10 products per page.
    page_number = request.GET.get("page")
    page_obj = paginator.get_page(page_number)
    return render(request, "admin_dashboard/products_list.html", {"page_obj": page_obj})


@staff_member_required
def product_add(request):
    if request.method == "POST":
        form = ProductForm(request.POST, request.FILES)
        if form.is_valid():
            product = form.save()
            messages.success(request, "Product added successfully!")
            return redirect("dashboard:product_edit", pk=product.pk)
    else:
        form = ProductForm()
    return render(request, "admin_dashboard/product_add.html", {"form": form})


@staff_member_required
def product_edit(request, pk):
    product = get_object_or_404(Product, pk=pk)
    if request.method == "POST":
        form = ProductForm(request.POST, request.FILES, instance=product)
        formset = ProductImageFormSet(request.POST, request.FILES, instance=product)
        if form.is_valid() and formset.is_valid():
            form.save()
            formset.save()
            messages.success(request, "Product updated successfully!")
            return redirect("dashboard:product_list")
    else:
        form = ProductForm(instance=product)
        formset = ProductImageFormSet(instance=product)
    return render(
        request,
        "admin_dashboard/product_edit.html",
        {"form": form, "formset": formset, "product": product},
    )


@staff_member_required
def product_delete(request, pk):
    product = get_object_or_404(Product, pk=pk)
    if request.method == "POST":
        product.delete()
        messages.success(request, "Product deleted successfully!")
        return redirect("dashboard:product_list")
    return render(request, "admin_dashboard/product_delete.html", {"product": product})


@staff_member_required
def category_list(request):
    query = request.GET.get("q")
    if query:
        categories = Category.objects.filter(name__icontains=query).order_by("name")
    else:
        categories = Category.objects.all().order_by("name")

    paginator = Paginator(categories, 10)  # Show 10 categories per page.
    page_number = request.GET.get("page")
    page_obj = paginator.get_page(page_number)

    return render(
        request,
        "admin_dashboard/categories_list.html",
        {"page_obj": page_obj, "query": query},
    )


@staff_member_required
def category_add(request):
    if request.method == "POST":
        form = CategoryForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, "Category added successfully!")
            return redirect("dashboard:category_list")
    else:
        form = CategoryForm()
    return render(request, "admin_dashboard/category_add.html", {"form": form})


@staff_member_required
def category_edit(request, pk):
    category = get_object_or_404(Category, pk=pk)
    if request.method == "POST":
        form = CategoryForm(request.POST, instance=category)
        if form.is_valid():
            form.save()
            messages.success(request, "Category updated successfully!")
            return redirect("dashboard:category_list")
    else:
        form = CategoryForm(instance=category)
    return render(
        request,
        "admin_dashboard/category_edit.html",
        {"form": form, "category": category},
    )


@staff_member_required
def category_delete(request, pk):
    category = get_object_or_404(Category, pk=pk)
    if request.method == "POST":
        category.delete()
        messages.success(request, "Category deleted successfully!")
        return redirect("dashboard:category_list")
    return render(
        request, "admin_dashboard/category_delete.html", {"category": category}
    )
