# Generated by Django 4.0.4 on 2022-09-16 20:37

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('maket', '0055_alter_print_group_code'),
    ]

    operations = [
        migrations.AddField(
            model_name='films',
            name='date_sent',
            field=models.DateField(default=None, null=True),
        ),
    ]
