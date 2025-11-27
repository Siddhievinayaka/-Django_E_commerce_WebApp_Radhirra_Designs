from django import forms
from Radhirra.models import Product, Category, ProductImage


class ProductForm(forms.ModelForm):
    class Meta:
        model = Product
        fields = [
            "name",
            "description",
            "regular_price",
            "sale_price",
            "category",
            "material",
            "specifications",
            "seller_information",
        ]
        widgets = {
            "name": forms.TextInput(attrs={"class": "form-control"}),
            "description": forms.Textarea(attrs={"class": "form-control", "rows": 3}),
            "regular_price": forms.NumberInput(attrs={"class": "form-control"}),
            "sale_price": forms.NumberInput(attrs={"class": "form-control"}),
            "category": forms.Select(attrs={"class": "form-control"}),
            "material": forms.TextInput(attrs={"class": "form-control"}),
            "specifications": forms.Textarea(
                attrs={"class": "form-control", "rows": 3}
            ),
            "seller_information": forms.Textarea(
                attrs={"class": "form-control", "rows": 3}
            ),
        }


class ProductImageForm(forms.ModelForm):
    class Meta:
        model = ProductImage
        fields = ["image", "is_main"]
        widgets = {
            "image": forms.ClearableFileInput(attrs={"class": "form-control"}),
            "is_main": forms.CheckboxInput(attrs={"class": "form-check-input"}),
        }


ProductImageFormSet = forms.inlineformset_factory(
    Product,
    ProductImage,
    form=ProductImageForm,
    extra=3,  # Number of extra forms to display
    can_delete=True,
)


class CategoryForm(forms.ModelForm):
    class Meta:
        model = Category
        fields = ["name", "slug"]
        widgets = {
            "name": forms.TextInput(attrs={"class": "form-control"}),
            "slug": forms.TextInput(attrs={"class": "form-control"}),
        }
