# Generated by Django 4.0.4 on 2022-05-21 20:09

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('maket', '0002_rename_company_customer_group_customer_region_and_more'),
    ]

    operations = [
        migrations.AlterField(
            model_name='color_scheme',
            name='scheme_name',
            field=models.CharField(max_length=13),
        ),
    ]
