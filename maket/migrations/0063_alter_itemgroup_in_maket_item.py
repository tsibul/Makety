# Generated by Django 4.0.4 on 2022-10-08 17:59

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('maket', '0062_alter_itemgroup_in_maket_maket_and_more'),
    ]

    operations = [
        migrations.AlterField(
            model_name='itemgroup_in_maket',
            name='item',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='maket.item_imports'),
        ),
    ]
