# Generated by Django 4.0.4 on 2023-02-25 14:51

import datetime
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('maket', '0098_alter_customer_all_date_last'),
        ('salesreport', '0025_alter_sales_doc_imports_main_color'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='sales_doc_imports',
            name='customer',
        ),
        migrations.AlterField(
            model_name='sales_doc_imports',
            name='import_date',
            field=models.DateField(default=datetime.date(2000, 1, 1)),
        ),
        migrations.AlterField(
            model_name='sales_doc_imports',
            name='sales_doc_date',
            field=models.DateField(default=datetime.date(2000, 1, 1)),
        ),
        migrations.AlterField(
            model_name='sales_docs',
            name='customer',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, to='maket.customer_all'),
        ),
        migrations.AlterField(
            model_name='sales_docs',
            name='sales_doc_date',
            field=models.DateField(default=datetime.date(2000, 1, 1)),
        ),
    ]
