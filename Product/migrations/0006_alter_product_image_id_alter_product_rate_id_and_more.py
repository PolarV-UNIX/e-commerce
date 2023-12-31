# Generated by Django 4.2.4 on 2023-09-15 19:31

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('Product', '0005_remove_product_name_product_title_and_more'),
    ]

    operations = [
        migrations.AlterField(
            model_name='product',
            name='image_id',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, to='Product.imageproduct', verbose_name='image'),
        ),
        migrations.AlterField(
            model_name='product',
            name='rate_id',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, to='Product.rating'),
        ),
        migrations.AlterField(
            model_name='rating',
            name='user_id',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, to=settings.AUTH_USER_MODEL),
        ),
    ]
