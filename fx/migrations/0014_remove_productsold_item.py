# Generated by Django 3.1.3 on 2021-02-15 07:25

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('fx', '0013_productsold'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='productsold',
            name='item',
        ),
    ]
