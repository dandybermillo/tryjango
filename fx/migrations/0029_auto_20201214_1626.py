# Generated by Django 3.1.3 on 2020-12-14 08:26

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('fx', '0028_daytransactionmodel'),
    ]

    operations = [
        migrations.AlterField(
            model_name='daytransactionmodel',
            name='source_type',
            field=models.CharField(choices=[(2, 'CASH'), (0, 'WALLET ACCOUNT'), (1, 'SAVING ACCOUNT')], default=0, max_length=1),
        ),
    ]
