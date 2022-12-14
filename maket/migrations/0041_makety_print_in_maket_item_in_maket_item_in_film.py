# Generated by Django 4.0.4 on 2022-09-03 07:12

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('maket', '0040_alter_item_imports_name'),
    ]

    operations = [
        migrations.CreateModel(
            name='Makety',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('date_create', models.DateField(blank=True)),
                ('date_modified', models.DateField(blank=True, null=True)),
                ('maket_id', models.SmallIntegerField(default=0)),
                ('uploaded', models.BooleanField(default=False)),
                ('maket_file', models.FilePathField(blank=True, null=True)),
                ('comment', models.CharField(default='', max_length=255)),
                ('order_num', models.CharField(blank=True, max_length=6, null=True)),
                ('order_date', models.DateField(default='1000-01-01')),
                ('order', models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, to='maket.order_imports')),
            ],
        ),
        migrations.CreateModel(
            name='Print_in_Maket',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('maket', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, to='maket.makety')),
                ('print_item', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, to='maket.print_imports')),
            ],
        ),
        migrations.CreateModel(
            name='Item_in_Maket',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('item', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, to='maket.item_imports')),
                ('maket', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, to='maket.makety')),
            ],
        ),
        migrations.CreateModel(
            name='Item_in_Film',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('status', models.BooleanField(default=True)),
                ('film', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, to='maket.films')),
                ('item', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, to='maket.item_imports')),
            ],
        ),
    ]
