from django.shortcuts import render, redirect
from django.contrib import messages
from django.contrib.auth import login, logout
from django.contrib.auth.decorators import login_required
from .forms import UserRegisterForm, UserLoginForm, UserProfileUpdateForm
from .models import UserProfile


def register_view(request):
    if request.user.is_authenticated:
        return redirect("profile")

    if request.method == "POST":
        form = UserRegisterForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user, backend='django.contrib.auth.backends.ModelBackend')
            messages.success(request, "Registration successful.")
            return redirect("profile")
        else:
            messages.error(request, "Please correct the errors below.")
    else:
        form = UserRegisterForm()

    return render(request, "users/register.html", {"form": form})


def login_view(request):
    if request.method == "POST":
        form = UserLoginForm(request, data=request.POST)
        if form.is_valid():
            login(request, form.get_user())
            return redirect("profile")
        messages.error(request, "Invalid credentials.")
    else:
        form = UserLoginForm()

    return render(request, "users/login.html", {"form": form})


def logout_view(request):
    logout(request)
    messages.success(request, 'You have been successfully logged out.')
    return redirect("login")


@login_required
def profile_view(request):
    profile, _ = UserProfile.objects.get_or_create(user=request.user)
    return render(request, "users/profile.html", {"profile": profile})


@login_required
def profile_update_view(request):
    profile, _ = UserProfile.objects.get_or_create(user=request.user)

    if request.method == "POST":
        form = UserProfileUpdateForm(request.POST, request.FILES, instance=profile)
        if form.is_valid():
            form.save()
            return redirect("profile")
    else:
        form = UserProfileUpdateForm(instance=profile)

    return render(request, "users/profile_update.html", {"form": form})

@login_required
def delete_account(request):
    if request.method == 'POST':
        request.user.delete()
        messages.success(request, 'Your account has been deleted successfully.')
        return redirect('index')
    return render(request, 'users/delete_account.html')