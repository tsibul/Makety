# Generated by Django 4.0.4 on 2022-07-13 19:40

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('maket', '0017_customer_inn_order_imports_customer_and_more'),
    ]

    operations = [
        migrations.AddField(
            model_name='detail_set',
            name='item_name',
            field=models.CharField(blank=True, max_length=6, null=True),
        ),
    ]
