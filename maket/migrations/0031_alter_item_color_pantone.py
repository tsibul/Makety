# Generated by Django 4.0.4 on 2022-07-19 20:51

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('maket', '0030_item_color_pantone'),
    ]

    operations = [
        migrations.AlterField(
            model_name='item_color',
            name='pantone',
            field=models.CharField(default='', max_length=20),
        ),
    ]
