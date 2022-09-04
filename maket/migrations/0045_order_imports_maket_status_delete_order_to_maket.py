# Generated by Django 4.0.4 on 2022-09-04 05:00

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('maket', '0044_order_to_maket'),
    ]

    operations = [
        migrations.AddField(
            model_name='order_imports',
            name='maket_status',
            field=models.CharField(choices=[('R', 'R'), ('P', 'P'), ('N', 'N')], default='N', max_length=1),
        ),
        migrations.DeleteModel(
            name='Order_to_Maket',
        ),
    ]
