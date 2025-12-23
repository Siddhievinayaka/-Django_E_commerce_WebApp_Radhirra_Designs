# Generated migration

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('Radhirra', '0012_cartitem_size_cartitem_sleeve_product_sleeve_and_more'),
    ]

    operations = [
        migrations.AddField(
            model_name='product',
            name='is_featured',
            field=models.BooleanField(default=False),
        ),
        migrations.AddField(
            model_name='product',
            name='is_new_arrival',
            field=models.BooleanField(default=False),
        ),
        migrations.AddField(
            model_name='product',
            name='is_best_seller',
            field=models.BooleanField(default=False),
        ),
    ]
