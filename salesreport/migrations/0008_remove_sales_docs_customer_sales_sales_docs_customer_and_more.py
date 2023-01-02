# Generated by Django 4.0.4 on 2022-12-30 12:35

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('maket', '0085_customer_date_first'),
        ('salesreport', '0007_customer_all_customer'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='sales_docs',
            name='customer_sales',
        ),
        migrations.AddField(
            model_name='sales_docs',
            name='customer',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, to='maket.customer'),
        ),
        migrations.DeleteModel(
            name='Customers_sales',
        ),
    ]