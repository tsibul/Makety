# Generated by Django 4.0.4 on 2022-12-30 10:29

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('salesreport', '0005_alter_customer_all_all_mails_and_more'),
    ]

    operations = [
        migrations.AlterField(
            model_name='customer_all',
            name='inn',
            field=models.CharField(max_length=20, null=True),
        ),
    ]
