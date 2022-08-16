# Generated by Django 4.0.4 on 2022-07-10 05:26

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('maket', '0004_alter_print_place_place_name'),
    ]

    operations = [
        migrations.CreateModel(
            name='Item_imports',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('code', models.CharField(blank=True, max_length=20, null=True)),
                ('name', models.CharField(blank=True, max_length=80, null=True)),
                ('print_name', models.CharField(blank=True, max_length=50, null=True)),
            ],
        ),
        migrations.CreateModel(
            name='Order_imports',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('order_id', models.CharField(blank=True, max_length=18, null=True)),
                ('supplier', models.CharField(blank=True, max_length=50, null=True)),
                ('customer', models.CharField(blank=True, max_length=50, null=True)),
                ('customer_INN', models.CharField(blank=True, max_length=12, null=True)),
                ('customer_address', models.CharField(blank=True, max_length=120, null=True)),
            ],
        ),
        migrations.CreateModel(
            name='Print_imports',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('place', models.CharField(blank=True, max_length=20, null=True)),
                ('type', models.CharField(blank=True, max_length=20, null=True)),
                ('second_pass', models.BooleanField(default=False)),
                ('item', models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, to='maket.item_imports')),
            ],
        ),
        migrations.AddField(
            model_name='item_imports',
            name='order',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, to='maket.order_imports'),
        ),
    ]