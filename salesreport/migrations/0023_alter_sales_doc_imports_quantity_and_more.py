# Generated by Django 4.0.4 on 2023-01-06 15:06

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('salesreport', '0022_alter_sales_doc_imports_sales_doc_no_and_more'),
    ]

    operations = [
        migrations.AlterField(
            model_name='sales_doc_imports',
            name='quantity',
            field=models.FloatField(default=0),
        ),
        migrations.AlterField(
            model_name='sales_doc_imports',
            name='sales_quantity',
            field=models.FloatField(default=0),
        ),
        migrations.AlterField(
            model_name='sales_docs',
            name='quantity',
            field=models.FloatField(default=0),
        ),
    ]
