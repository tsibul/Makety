# Generated by Django 4.0.4 on 2022-07-22 19:41

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('maket', '0032_films_order_imports_film'),
    ]

    operations = [
        migrations.AddField(
            model_name='order_imports',
            name='film_status',
            field=models.BooleanField(default=True),
        ),
        migrations.AlterField(
            model_name='films',
            name='film_id',
            field=models.IntegerField(default=0),
        ),
    ]
