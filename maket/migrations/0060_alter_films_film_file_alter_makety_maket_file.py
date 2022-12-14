# Generated by Django 4.0.4 on 2022-09-18 23:52

import django.core.files.storage
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('maket', '0059_alter_order_imports_order_file'),
    ]

    operations = [
        migrations.AlterField(
            model_name='films',
            name='film_file',
            field=models.FileField(blank=True, null=True, storage=django.core.files.storage.FileSystemStorage(location='files/films'), upload_to=''),
        ),
        migrations.AlterField(
            model_name='makety',
            name='maket_file',
            field=models.FileField(blank=True, null=True, storage=django.core.files.storage.FileSystemStorage(location='files/makety'), upload_to=''),
        ),
    ]
