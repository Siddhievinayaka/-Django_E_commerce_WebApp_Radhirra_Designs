from django.db import migrations
from django.utils.text import slugify

CATEGORIES = [
    "Cotton hand bags",
    "Painted Bead bags",
    "Gopi Dress",
    "Cotton 3 piece suit fabric",
    "Cotton mul mul sarees",
    "Cotton kota doriya sarees",
    "Cotton linen sarees",
    "Chanderi silk sarees",
    "Cotton khadi sarees",
    "MUGA cotton sarees",
    "Cotton silk sarees",
    "Maheshwari silk sarees",
    "Dhakai Jamdani saree",
    "Pure cotton sarees",
    "South cotton sarees",
]


def preload_categories(apps, schema_editor):
    Category = apps.get_model("Radhirra", "Category")
    for name in CATEGORIES:
        Category.objects.get_or_create(name=name, defaults={"slug": slugify(name)})


def remove_categories(apps, schema_editor):
    Category = apps.get_model("Radhirra", "Category")
    Category.objects.filter(name__in=CATEGORIES).delete()


class Migration(migrations.Migration):

    dependencies = [
        (
            "Radhirra",
            "0003_cart_cartitem",
        ),  # Make sure this matches your last migration file
    ]

    operations = [
        migrations.RunPython(preload_categories, remove_categories),
    ]
