# Generated by Django 3.2 on 2023-01-28 11:09

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('store', '0003_auto_20230128_1638'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='product',
            name='price2',
        ),
    ]
