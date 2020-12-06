# Generated by Django 3.1.3 on 2020-11-30 08:02

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('fx', '0024_auto_20201129_1840'),
    ]

    operations = [
        migrations.CreateModel(
            name='LoanSummaryModel',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('date_entered', models.DateField(blank=True, null=True, verbose_name='Date')),
                ('max_loan', models.FloatField(default=300, verbose_name='Max Loan')),
                ('percent', models.PositiveIntegerField(default=35)),
                ('member', models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, to='fx.membermodel')),
            ],
        ),
    ]