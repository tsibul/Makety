# Generated by Django 4.0.4 on 2022-07-10 06:04

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('maket', '0008_remove_item_imports_print_id_and_more'),
    ]

    operations = [
        migrations.AddField(
            model_name='item_imports',
            name='print_id',
            field=models.CharField(blank=True, max_length=3, null=True),
        ),
        migrations.AddField(
            model_name='print_imports',
            name='print_id',
            field=models.CharField(blank=True, max_length=3, null=True),
        ),
    ]
