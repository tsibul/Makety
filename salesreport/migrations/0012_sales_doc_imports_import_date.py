# Generated by Django 4.0.4 on 2023-01-03 14:50

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('salesreport', '0011_sales_doc_imports_main_color'),
    ]

    operations = [
        migrations.AddField(
            model_name='sales_doc_imports',
            name='import_date',
            field=models.DateField(default='2000-01-01'),
        ),
    ]
