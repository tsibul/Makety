# Generated by Django 4.0.4 on 2023-01-04 14:32

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('salesreport', '0018_alter_sales_docs_sales_doc_date_and_more'),
    ]

    operations = [
        migrations.AddField(
            model_name='sales_docs',
            name='good_no_error',
            field=models.BooleanField(default=True),
        ),
    ]
