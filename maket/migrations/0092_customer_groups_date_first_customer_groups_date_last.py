# Generated by Django 4.0.4 on 2023-01-09 06:31

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('maket', '0091_customer_active_customer_internal'),
    ]

    operations = [
        migrations.AddField(
            model_name='customer_groups',
            name='date_first',
            field=models.DateField(default='2100-01-01'),
        ),
        migrations.AddField(
            model_name='customer_groups',
            name='date_last',
            field=models.DateField(default='2000-01-01'),
        ),
    ]