# Generated by Django 3.1.3 on 2021-02-23 06:33

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('fx', '0019_productmodel1'),
    ]

    operations = [
        migrations.AddField(
            model_name='productmodel',
            name='srp',
            field=models.FloatField(default=0),
        ),
    ]
