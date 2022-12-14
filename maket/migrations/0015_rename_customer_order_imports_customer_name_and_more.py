# Generated by Django 4.0.4 on 2022-07-13 06:09

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('maket', '0014_alter_order_imports_customer'),
    ]

    operations = [
        migrations.RenameField(
            model_name='order_imports',
            old_name='customer',
            new_name='customer_name',
        ),
        migrations.AddField(
            model_name='item_imports',
            name='detail1_color',
            field=models.CharField(default='', max_length=10),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='item_imports',
            name='detail2_color',
            field=models.CharField(default='', max_length=10),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='item_imports',
            name='detail3_color',
            field=models.CharField(default='', max_length=10),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='item_imports',
            name='detail4_color',
            field=models.CharField(default='', max_length=10),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='item_imports',
            name='detail5_color',
            field=models.CharField(default='', max_length=10),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='item_imports',
            name='item_color',
            field=models.CharField(default='', max_length=40),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='print_imports',
            name='position',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, to='maket.print_position'),
        ),
    ]
