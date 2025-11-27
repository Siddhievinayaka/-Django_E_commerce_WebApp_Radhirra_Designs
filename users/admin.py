from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from .models import CustomUser, UserProfile


class CustomUserAdmin(UserAdmin):
    model = CustomUser
    list_display = ["email", "username", "is_staff", "is_active"]
    fieldsets = UserAdmin.fieldsets  # Removed the duplicate email field
    add_fieldsets = UserAdmin.add_fieldsets + ((None, {"fields": ("email",)}),)


admin.site.register(CustomUser, CustomUserAdmin)
admin.site.register(UserProfile)

# Register your models here.
