# Generated by Django 4.0.4 on 2023-03-10 12:30

import datetime
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('maket', '0099_alter_customer_groups_group_name'),
    ]

    operations = [
        migrations.AlterField(
            model_name='customer_groups',
            name='date_first',
            field=models.DateField(default=datetime.date(2000, 1, 1)),
        ),
        migrations.AlterField(
            model_name='customer_groups',
            name='date_last',
            field=models.DateField(default=datetime.date(2000, 1, 1)),
        ),
    ]