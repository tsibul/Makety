# Generated by Django 4.0.4 on 2022-09-03 16:09

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('maket', '0043_alter_makety_order_num'),
    ]

    operations = [
        migrations.CreateModel(
            name='Order_to_Maket',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('status', models.CharField(choices=[('R', 'R'), ('P', 'P'), ('N', 'N')], default='N', max_length=1)),
                ('maket', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='maket.makety')),
                ('order', models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, to='maket.order_imports')),
            ],
        ),
    ]
