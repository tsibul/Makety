# Generated by Django 4.0.4 on 2022-10-08 18:00

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('maket', '0063_alter_itemgroup_in_maket_item'),
    ]

    operations = [
        migrations.AlterField(
            model_name='makety',
            name='order',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, to='maket.order_imports'),
        ),
    ]
