# Generated by Django 4.0.4 on 2022-09-08 20:39

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('maket', '0049_print_group_layout'),
    ]

    operations = [
        migrations.AddField(
            model_name='print_group',
            name='options',
            field=models.SmallIntegerField(default=1),
        ),
    ]
