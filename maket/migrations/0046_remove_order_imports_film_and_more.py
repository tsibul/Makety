# Generated by Django 4.0.4 on 2022-09-04 05:31

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('maket', '0045_order_imports_maket_status_delete_order_to_maket'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='order_imports',
            name='film',
        ),
        migrations.RemoveField(
            model_name='order_imports',
            name='film_status',
        ),
        migrations.AddField(
            model_name='films',
            name='item_group',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, to='maket.itemgroup_in_maket'),
        ),
        migrations.AddField(
            model_name='itemgroup_in_maket',
            name='print_name',
            field=models.CharField(blank=True, max_length=50, null=True),
        ),
    ]