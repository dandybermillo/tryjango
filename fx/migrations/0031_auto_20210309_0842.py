# Generated by Django 3.1.3 on 2021-03-09 00:42

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('fx', '0030_auto_20210309_0834'),
    ]

    operations = [
        migrations.RenameField(
            model_name='productmodel',
            old_name='whole_sale',
            new_name='whole_sale_price',
        ),
    ]
