# Generated by Django 3.1.3 on 2020-12-24 05:30

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('fx', '0037_mechanicmodel_repairmodel'),
    ]

    operations = [
        migrations.CreateModel(
            name='ConstructionModel',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=124)),
                ('phone', models.CharField(max_length=124)),
                ('description', models.CharField(max_length=300)),
                ('category', models.PositiveIntegerField(choices=[(0, 'Worker'), (1, 'Materials')], default=0)),
                ('message', models.CharField(max_length=300)),
            ],
        ),
    ]
