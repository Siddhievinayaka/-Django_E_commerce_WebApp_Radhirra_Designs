from django import forms
from .models import Customer
from django.contrib.auth.models import User


class CustomerForm(forms.ModelForm):
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

    class Meta:
        model = Customer
        fields = ["name", "email", "contact_number", "profile_pic"]
        widgets = {
            "name": forms.TextInput(
                attrs={
                    "class": "w-full px-4 py-2 border rounded-lg text-gray-700 focus:outline-none focus:border-blue-500",
                    "placeholder": "Enter your name",
                }
            ),
            "email": forms.EmailInput(
                attrs={
                    "class": "w-full px-4 py-2 border rounded-lg text-gray-700 focus:outline-none focus:border-blue-500",
                    "placeholder": "Enter your email",
                }
            ),
            "contact_number": forms.TextInput(
                attrs={
                    "class": "w-full px-4 py-2 border rounded-lg text-gray-700 focus:outline-none focus:border-blue-500",
                    "placeholder": "Enter your contact number",
                }
            ),
            "profile_pic": forms.FileInput(
                attrs={"class": "w-full text-gray-700 focus:outline-none"}
            ),
        }

    def clean(self):
        cleaned_data = super().clean()
        password = cleaned_data.get("password")
        password_confirm = cleaned_data.get("password_confirm")

        if password and password_confirm and password != password_confirm:
            raise forms.ValidationError("Passwords do not match.")
        return cleaned_data
