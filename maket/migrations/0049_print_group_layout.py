# Generated by Django 4.0.4 on 2022-09-07 18:19

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('maket', '0048_print_group_detail_set_print_group'),
    ]

    operations = [
        migrations.AddField(
            model_name='print_group',
            name='layout',
            field=models.CharField(blank=True, default='', max_length=120),
        ),
    ]
