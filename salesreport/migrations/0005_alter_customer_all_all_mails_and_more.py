# Generated by Django 4.0.4 on 2022-12-30 10:26

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('salesreport', '0004_alter_customer_all_region'),
    ]

    operations = [
        migrations.AlterField(
            model_name='customer_all',
            name='all_mails',
            field=models.CharField(max_length=600, null=True),
        ),
        migrations.AlterField(
            model_name='customer_all',
            name='all_phones',
            field=models.CharField(max_length=600, null=True),
        ),
    ]