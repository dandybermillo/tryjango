# Generated by Django 3.1.3 on 2020-12-27 10:11

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('fx', '0046_auto_20201227_1809'),
    ]

    operations = [
        migrations.AddField(
            model_name='constructionmodel',
            name='email',
            field=models.EmailField(blank=True, max_length=254, null=True),
        ),
    ]
