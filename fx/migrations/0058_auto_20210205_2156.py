# Generated by Django 3.1.3 on 2021-02-05 13:56

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('fx', '0057_auto_20210205_2053'),
    ]

    operations = [
        migrations.AlterField(
            model_name='itemmodel',
            name='img',
            field=models.ImageField(blank=True, null=True, upload_to=''),
        ),
    ]