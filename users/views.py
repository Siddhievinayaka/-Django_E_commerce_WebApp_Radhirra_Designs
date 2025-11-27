from django.shortcuts import render, redirect
from django.contrib import messages
from django.contrib.auth import login, logout
from django.contrib.auth.decorators import login_required
from .forms import UserRegisterForm, UserLoginForm, UserProfileUpdateForm
from .models import UserProfile


def register_view(request):
    if request.method == "POST":
        form = UserRegisterForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user)
            messages.success(request, "Registration successful.")
            return redirect("profile")
        messages.error(request, "Unsuccessful registration. Invalid information.")
    else:
        form = UserRegisterForm()
    return render(request, "users/register.html", {"form": form})


def login_view(request):
    if request.method == "POST":
        form = UserLoginForm(request, data=request.POST)
        if form.is_valid():
            user = form.get_user()
            login(request, user)
            messages.info(request, f"You are now logged in as {user.email}.")
            return redirect("profile")
        else:
            messages.error(request, "Invalid email or password.")
    else:
        form = UserLoginForm()
    return render(request, "users/login.html", {"form": form})


@login_required
def logout_view(request):
    logout(request)
    messages.info(request, "You have successfully logged out.")
    return redirect("index")


@login_required
def profile_view(request):
    profile, created = UserProfile.objects.get_or_create(user=request.user)
    context = {"profile": profile}
    return render(request, "users/profile.html", context)


@login_required
def profile_update_view(request):
    profile, created = UserProfile.objects.get_or_create(user=request.user)
    if request.method == "POST":
        form = UserProfileUpdateForm(request.POST, request.FILES, instance=profile)
        if form.is_valid():
            form.save()
            messages.success(request, "Your profile has been updated successfully!")
            return redirect("profile")
        else:
            messages.error(request, "Please correct the error below.")
    else:
        form = UserProfileUpdateForm(instance=profile)

    context = {"form": form}
    return render(request, "users/profile_update.html", context)
