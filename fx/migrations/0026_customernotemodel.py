# Generated by Django 3.1.3 on 2021-03-06 13:24

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('fx', '0025_pricelistmodel_product'),
    ]

    operations = [
        migrations.CreateModel(
            name='CustomerNoteModel',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('source_id', models.IntegerField(default=0)),
                ('note', models.TextField(blank=True, help_text='Enter note when necessary. Thank you', max_length=300, null=True)),
                ('date_entered', models.DateField(blank=True, null=True, verbose_name='Date')),
            ],
        ),
    ]
