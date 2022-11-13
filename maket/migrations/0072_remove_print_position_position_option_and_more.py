# Generated by Django 4.0.4 on 2022-11-02 18:31

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('maket', '0071_additional_files_file_type'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='print_position',
            name='position_option',
        ),
        migrations.AddField(
            model_name='print_position',
            name='orientation_id',
            field=models.SmallIntegerField(default=1),
        ),
        migrations.AddField(
            model_name='print_position',
            name='position_place',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, to='maket.print_place'),
        ),
        migrations.AddField(
            model_name='print_position',
            name='print_group',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, to='maket.print_group'),
        ),
    ]
