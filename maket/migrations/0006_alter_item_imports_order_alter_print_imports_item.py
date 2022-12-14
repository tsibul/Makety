# Generated by Django 4.0.4 on 2022-07-10 05:58

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('maket', '0005_item_imports_order_imports_print_imports_and_more'),
    ]

    operations = [
        migrations.AlterField(
            model_name='item_imports',
            name='order',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, to='maket.order_imports'),
        ),
        migrations.AlterField(
            model_name='print_imports',
            name='item',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, to='maket.item_imports'),
        ),
    ]
