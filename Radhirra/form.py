from django import forms
from django.contrib.auth import get_user_model
from users.models import UserProfile  # Import UserProfile from the users app

User = get_user_model()  # Get the currently active user model


class CustomerRegistrationForm(forms.ModelForm):
    username = forms.CharField(
        max_length=150,
        widget=forms.TextInput(
            attrs={
                "class": "w-full px-4 py-2 border rounded-lg text-gray-700 focus:outline-none focus:border-blue-500",
                "placeholder": "Enter your username",
            }
        ),
    )
    email = forms.EmailField(
        widget=forms.EmailInput(
            attrs={
                "class": "w-full px-4 py-2 border rounded-lg text-gray-700 focus:outline-none focus:border-blue-500",
                "placeholder": "Enter your email",
            }
        ),
    )
    password = forms.CharField(
        widget=forms.PasswordInput(
            attrs={
                "class": "w-full px-4 py-2 border rounded-lg text-gray-700 focus:outline-none focus:border-blue-500",
                "placeholder": "Enter your password",
            }
        )
    )
    password_confirm = forms.CharField(
        widget=forms.PasswordInput(
            attrs={
                "class": "w-full px-4 py-2 border rounded-lg text-gray-700 focus:outline-none focus:border-blue-500",
                "placeholder": "Confirm your password",
            }
        )
    )
    contact_number = forms.CharField(
        max_length=20,
        required=False,
        widget=forms.TextInput(
            attrs={
                "class": "w-full px-4 py-2 border rounded-lg text-gray-700 focus:outline-none focus:border-blue-500",
                "placeholder": "Enter your contact number (optional)",
            }
        ),
    )
    profile_pic = forms.ImageField(
        required=False,
        widget=forms.FileInput(
            attrs={"class": "w-full text-gray-700 focus:outline-none"}
        ),
    )

    class Meta:
        model = User
        fields = ["username", "email", "password"]  # These are for the CustomUser model

    def clean(self):
        cleaned_data = super().clean()
        password = cleaned_data.get("password")
        password_confirm = cleaned_data.get("password_confirm")

        if password and password_confirm and password != password_confirm:
            raise forms.ValidationError("Passwords do not match.")
        return cleaned_data

    def save(self, commit=True):
        user = super().save(commit=False)
        user.set_password(self.cleaned_data["password"])
        if commit:
            user.save()
            UserProfile.objects.create(
                user=user,
                phone=self.cleaned_data.get("contact_number"),
                profile_pic=self.cleaned_data.get("profile_pic"),
            )
        return user
