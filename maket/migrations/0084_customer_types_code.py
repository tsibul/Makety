# Generated by Django 4.0.4 on 2022-12-13 23:08

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('maket', '0083_alter_customer_types_group_discount'),
    ]

    operations = [
        migrations.AddField(
            model_name='customer_types',
            name='code',
            field=models.CharField(default='', max_length=2),
        ),
    ]
