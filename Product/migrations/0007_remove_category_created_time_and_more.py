# Generated by Django 4.2.4 on 2023-09-15 19:45

from django.db import migrations, models
import django.utils.timezone


class Migration(migrations.Migration):

    dependencies = [
        ('Product', '0006_alter_product_image_id_alter_product_rate_id_and_more'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='category',
            name='created_time',
        ),
        migrations.RemoveField(
            model_name='category',
            name='modify_date',
        ),
        migrations.RemoveField(
            model_name='imageproduct',
            name='created_time',
        ),
        migrations.RemoveField(
            model_name='imageproduct',
            name='modify_date',
        ),
        migrations.RemoveField(
            model_name='product',
            name='created_time',
        ),
        migrations.RemoveField(
            model_name='product',
            name='modify_date',
        ),
        migrations.AddField(
            model_name='category',
            name='created_at',
            field=models.DateTimeField(auto_now_add=True, default=django.utils.timezone.now, verbose_name='created_at'),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='category',
            name='modify_at',
            field=models.DateTimeField(auto_now=True, verbose_name='modify_at'),
        ),
        migrations.AddField(
            model_name='imageproduct',
            name='created_at',
            field=models.DateTimeField(auto_now_add=True, default=django.utils.timezone.now, verbose_name='created_at'),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='imageproduct',
            name='modify_at',
            field=models.DateTimeField(auto_now=True, verbose_name='modify_at'),
        ),
        migrations.AddField(
            model_name='product',
            name='created_at',
            field=models.DateTimeField(auto_now_add=True, default=django.utils.timezone.now, verbose_name='created_at'),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='product',
            name='modify_at',
            field=models.DateTimeField(auto_now=True, verbose_name='modify_at'),
        ),
    ]
