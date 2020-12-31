# Generated by Django 3.1.3 on 2020-12-30 12:53

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('fx', '0007_auto_20201230_2051'),
    ]

    operations = [
        migrations.AlterField(
            model_name='daytransactionmodel',
            name='source_type',
            field=models.IntegerField(choices=[(0, 'CASH'), (1, 'WALLET ACCOUNT'), (2, 'SAVING ACCOUNT')], default=0, max_length=1),
        ),
    ]
