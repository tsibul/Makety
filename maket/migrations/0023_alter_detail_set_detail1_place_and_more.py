# Generated by Django 4.0.4 on 2022-07-15 04:11

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('maket', '0022_alter_detail_set_detail2_name_and_more'),
    ]

    operations = [
        migrations.AlterField(
            model_name='detail_set',
            name='detail1_place',
            field=models.SmallIntegerField(default=0),
        ),
        migrations.AlterField(
            model_name='detail_set',
            name='detail2_place',
            field=models.SmallIntegerField(default=0),
        ),
        migrations.AlterField(
            model_name='detail_set',
            name='detail3_place',
            field=models.SmallIntegerField(default=0),
        ),
        migrations.AlterField(
            model_name='detail_set',
            name='detail4_place',
            field=models.SmallIntegerField(default=0),
        ),
        migrations.AlterField(
            model_name='detail_set',
            name='detail5_place',
            field=models.SmallIntegerField(default=0),
        ),
    ]
