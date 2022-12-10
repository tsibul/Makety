# Generated by Django 4.0.4 on 2022-12-10 23:08

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('maket', '0080_customer_types_good_crm_type_good_matrix_type_and_more'),
    ]

    operations = [
        migrations.CreateModel(
            name='Customers_sales',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('customer_name', models.CharField(max_length=255)),
                ('customer_type', models.CharField(max_length=20)),
                ('customer', models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, to='maket.customer')),
                ('customer_group', models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, to='maket.customer_groups')),
            ],
        ),
        migrations.CreateModel(
            name='Sales_docs',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('sales_document', models.CharField(max_length=255)),
                ('customer_sales', models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, to='salesreport.customers_sales')),
                ('order', models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, to='maket.order_imports')),
            ],
        ),
        migrations.CreateModel(
            name='Sales_doc_imports',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('code', models.CharField(max_length=20)),
                ('color_code', models.CharField(max_length=20)),
                ('series_id', models.IntegerField(null=True)),
                ('detail_set', models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, to='maket.detail_set')),
                ('item_color', models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, to='maket.item_color')),
            ],
        ),
    ]
