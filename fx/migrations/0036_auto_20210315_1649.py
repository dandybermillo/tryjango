# Generated by Django 3.1.3 on 2021-03-15 08:49

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('fx', '0035_auto_20210315_0801'),
    ]

    operations = [
        migrations.AlterField(
            model_name='productmodel',
            name='category',
            field=models.PositiveIntegerField(choices=[(0, 'PERSONAL_HYGIENE'), (1, 'CANNED GOODS'), (2, 'DRY GOODS'), (3, 'PRODUCE'), (5, 'DRINKS'), (4, 'OTHER'), (6, 'CONDIMENTS'), (7, 'SNACKS'), (8, 'SEASONING')], default=4),
        ),
    ]
