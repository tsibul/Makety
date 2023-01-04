# Generated by Django 4.0.4 on 2023-01-04 12:45

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('salesreport', '0014_alter_sales_doc_imports_color_code'),
    ]

    operations = [
        migrations.AddField(
            model_name='sales_docs',
            name='quantity',
            field=models.IntegerField(default=0),
        ),
        migrations.AddField(
            model_name='sales_docs',
            name='total_buy_with_vat',
            field=models.FloatField(default=0),
        ),
        migrations.AddField(
            model_name='sales_docs',
            name='total_buy_without_vat',
            field=models.FloatField(default=0),
        ),
        migrations.AddField(
            model_name='sales_docs',
            name='total_sale_with_vat',
            field=models.FloatField(default=0),
        ),
        migrations.AddField(
            model_name='sales_docs',
            name='total_sale_without_vat',
            field=models.FloatField(default=0),
        ),
    ]
