# Generated by Django 4.0.4 on 2022-07-17 13:27

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('maket', '0028_remove_detail_set_detail1_remove_detail_set_detail2_and_more'),
    ]

    operations = [
        migrations.AlterField(
            model_name='order_imports',
            name='customer_name',
            field=models.CharField(blank=True, max_length=255, null=True),
        ),
    ]
