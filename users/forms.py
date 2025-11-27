from django import forms
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from .models import CustomUser, UserProfile


class UserRegisterForm(UserCreationForm):
    class Meta(UserCreationForm.Meta):
        model = CustomUser
        fields = ("username", "email")


class UserLoginForm(AuthenticationForm):
    username = forms.EmailField(widget=forms.EmailInput(attrs={"autofocus": True}))


class UserProfileUpdateForm(forms.ModelForm):
    class Meta:
        model = UserProfile
        fields = [
            "phone",
            "gender",
            "profile_pic",
            "address",
            "city",
            "state",
            "zipcode",
        ]
        widgets = {
            "profile_pic": forms.FileInput(),
        }
