# Generated by Django 4.0.4 on 2022-07-31 09:51

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('maket', '0035_remove_print_imports_position_and_more'),
    ]

    operations = [
        migrations.AlterField(
            model_name='detail_set',
            name='item_name',
            field=models.CharField(blank=True, max_length=20, null=True),
        ),
        migrations.AlterField(
            model_name='item_imports',
            name='item_group',
            field=models.CharField(blank=True, default='', max_length=20, null=True),
        ),
    ]
