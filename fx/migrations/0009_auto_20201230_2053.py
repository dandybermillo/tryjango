# Generated by Django 3.1.3 on 2020-12-30 12:53

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('fx', '0008_auto_20201230_2053'),
    ]

    operations = [
        migrations.AlterField(
            model_name='daytransactionmodel',
            name='source_type',
            field=models.IntegerField(choices=[(0, 'CASH'), (1, 'WALLET ACCOUNT'), (2, 'SAVING ACCOUNT')], default=0),
        ),
    ]