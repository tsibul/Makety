# Generated by Django 4.0.4 on 2022-11-05 12:28

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('maket', '0073_print_imports_print_place'),
    ]

    operations = [
        migrations.AddField(
            model_name='print_imports',
            name='print_position',
            field=models.ForeignKey(default='', null=True, on_delete=django.db.models.deletion.SET_NULL, to='maket.print_position'),
        ),
        migrations.CreateModel(
            name='Print_color',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('color_pantone', models.CharField(default='', max_length=20)),
                ('color_hex', models.CharField(default='', max_length=7)),
                ('color_number_in_item', models.IntegerField(default=1)),
                ('print_item', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='maket.print_imports')),
            ],
        ),
    ]
