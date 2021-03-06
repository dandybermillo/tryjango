# Generated by Django 3.1.3 on 2021-02-20 20:56

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('fx', '0018_productsold_description'),
    ]

    operations = [
        migrations.CreateModel(
            name='ProductModel1',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('title', models.CharField(blank=True, max_length=200)),
                ('category', models.PositiveIntegerField(choices=[(0, 'PERSONAL_HYGIENE'), (1, 'CANNED GOODS'), (2, 'DRY GOODS'), (3, 'PRODUCE'), (4, 'OTHER')], default=4)),
                ('qty', models.PositiveIntegerField()),
                ('price', models.FloatField()),
                ('reg_price', models.FloatField()),
                ('product_id', models.CharField(blank=True, max_length=13)),
                ('img', models.ImageField(blank=True, null=True, upload_to='')),
                ('sku', models.CharField(blank=True, max_length=20)),
            ],
        ),
    ]
