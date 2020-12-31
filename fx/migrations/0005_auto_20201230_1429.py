# Generated by Django 3.1.3 on 2020-12-30 06:29

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('fx', '0004_auto_20201230_1032'),
    ]

    operations = [
        migrations.AddField(
            model_name='daytransactionmodel',
            name='account_code',
            field=models.PositiveIntegerField(choices=[(0, 'CASH'), (1, 'WALLET ACCOUNT'), (2, 'SAVING ACCOUNT')], default=1),
        ),
        migrations.AlterField(
            model_name='daytransactionmodel',
            name='category',
            field=models.PositiveIntegerField(choices=[(2, 'REGULAR TRANSACTION'), (0, 'PAYMENT'), (1, 'VENTURE'), (3, 'DEPOSIT'), (4, 'WITHRAWAL'), (5, 'GROCERY'), (6, 'SERVICES')], default=1),
        ),
    ]