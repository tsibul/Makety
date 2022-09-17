# Generated by Django 4.0.4 on 2022-09-10 22:41

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('maket', '0051_print_in_maket_option'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='films',
            name='item_group',
        ),
        migrations.AddField(
            model_name='itemgroup_in_maket',
            name='film',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, to='maket.films'),
        ),
        migrations.AddField(
            model_name='itemgroup_in_maket',
            name='film_error',
            field=models.BooleanField(default=True),
        ),
    ]