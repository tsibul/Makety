# Generated by Django 4.0.4 on 2023-03-06 20:04

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('maket', '0098_alter_customer_all_date_last'),
    ]

    operations = [
        migrations.AlterField(
            model_name='customer_groups',
            name='group_name',
            field=models.CharField(max_length=255, unique=True),
        ),
    ]
