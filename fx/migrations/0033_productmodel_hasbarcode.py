# Generated by Django 3.1.3 on 2021-03-14 15:17

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('fx', '0032_creditlinemodel_transaction_type'),
    ]

    operations = [
        migrations.AddField(
            model_name='productmodel',
            name='hasbarcode',
            field=models.BooleanField(default=True),
        ),
    ]