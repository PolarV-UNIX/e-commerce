# Generated by Django 4.2.4 on 2023-09-16 19:29

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('Product', '0015_alter_rating_rate'),
    ]

    operations = [
        migrations.AlterField(
            model_name='product',
            name='rate',
            field=models.DecimalField(decimal_places=1, max_digits=6, null=True),
        ),
    ]