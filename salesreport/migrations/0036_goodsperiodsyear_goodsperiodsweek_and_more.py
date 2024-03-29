# Generated by Django 4.0.4 on 2023-03-20 21:53

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('maket', '0102_alter_customer_all_frigat_id'),
        ('salesreport', '0035_rename_sales_eco_with_vat_customerperiodsmonth_sales_with_vat_eco_and_more'),
    ]

    operations = [
        migrations.CreateModel(
            name='GoodsPeriodsYear',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('quantity', models.IntegerField(default=0)),
                ('cost_without_vat', models.FloatField(default=0)),
                ('profit', models.FloatField(default=0)),
                ('price_with_vat', models.FloatField(default=0)),
                ('price_without_vat', models.FloatField(default=0)),
                ('sale_with_vat', models.FloatField(default=0)),
                ('sale_without_vat', models.FloatField(default=0)),
                ('good', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='maket.detail_set')),
                ('main_color', models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, to='maket.item_color')),
                ('period', models.ForeignKey(limit_choices_to={'period': 'YR'}, on_delete=django.db.models.deletion.CASCADE, to='salesreport.reportperiod')),
            ],
            options={
                'verbose_name': 'еженедельные данные',
                'abstract': False,
            },
        ),
        migrations.CreateModel(
            name='GoodsPeriodsWeek',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('quantity', models.IntegerField(default=0)),
                ('cost_without_vat', models.FloatField(default=0)),
                ('profit', models.FloatField(default=0)),
                ('price_with_vat', models.FloatField(default=0)),
                ('price_without_vat', models.FloatField(default=0)),
                ('sale_with_vat', models.FloatField(default=0)),
                ('sale_without_vat', models.FloatField(default=0)),
                ('good', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='maket.detail_set')),
                ('main_color', models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, to='maket.item_color')),
                ('period', models.ForeignKey(limit_choices_to={'period': 'WK'}, on_delete=django.db.models.deletion.CASCADE, to='salesreport.reportperiod')),
            ],
            options={
                'verbose_name': 'еженедельные данные',
                'abstract': False,
            },
        ),
        migrations.CreateModel(
            name='GoodsPeriodsQuarter',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('quantity', models.IntegerField(default=0)),
                ('cost_without_vat', models.FloatField(default=0)),
                ('profit', models.FloatField(default=0)),
                ('price_with_vat', models.FloatField(default=0)),
                ('price_without_vat', models.FloatField(default=0)),
                ('sale_with_vat', models.FloatField(default=0)),
                ('sale_without_vat', models.FloatField(default=0)),
                ('good', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='maket.detail_set')),
                ('main_color', models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, to='maket.item_color')),
                ('period', models.ForeignKey(limit_choices_to={'period': 'QT'}, on_delete=django.db.models.deletion.CASCADE, to='salesreport.reportperiod')),
            ],
            options={
                'verbose_name': 'еженедельные данные',
                'abstract': False,
            },
        ),
        migrations.CreateModel(
            name='GoodsPeriodsMonth',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('quantity', models.IntegerField(default=0)),
                ('cost_without_vat', models.FloatField(default=0)),
                ('profit', models.FloatField(default=0)),
                ('price_with_vat', models.FloatField(default=0)),
                ('price_without_vat', models.FloatField(default=0)),
                ('sale_with_vat', models.FloatField(default=0)),
                ('sale_without_vat', models.FloatField(default=0)),
                ('good', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='maket.detail_set')),
                ('main_color', models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, to='maket.item_color')),
                ('period', models.ForeignKey(limit_choices_to={'period': 'MT'}, on_delete=django.db.models.deletion.CASCADE, to='salesreport.reportperiod')),
            ],
            options={
                'verbose_name': 'еженедельные данные',
                'abstract': False,
            },
        ),
    ]
