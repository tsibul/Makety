# Generated by Django 4.0.4 on 2023-03-05 12:25

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('maket', '0098_alter_customer_all_date_last'),
        ('salesreport', '0030_customerperiodsweek'),
    ]

    operations = [
        migrations.CreateModel(
            name='CustomerPeriodsYear',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('sales_with_vat', models.FloatField(default=0, null=True, verbose_name='продажи с НДС')),
                ('sales_eco_with_vat', models.FloatField(default=0, null=True, verbose_name='продажи эко с НДС')),
                ('sales_no_eco_with_vat', models.FloatField(default=0, null=True, verbose_name='продажи неэко с НДС')),
                ('profit', models.FloatField(default=0, null=True, verbose_name='прибыль')),
                ('profit_eco', models.FloatField(default=0, null=True, verbose_name='прибыль эко')),
                ('profit_no_eco', models.FloatField(default=0, null=True, verbose_name='прибыль неэко')),
                ('no_sales', models.SmallIntegerField(default=0, null=True, verbose_name='количество продаж')),
                ('no_sales_eco', models.SmallIntegerField(default=0, null=True, verbose_name='количество продаж эко')),
                ('no_sales_no_eco', models.SmallIntegerField(default=0, null=True, verbose_name='количество продаж неэко')),
                ('average_check', models.FloatField(default=0, null=True, verbose_name='редний чек')),
                ('average_check_eco', models.FloatField(default=0, null=True, verbose_name='средний чек эко')),
                ('average_check_no_eco', models.FloatField(default=0, null=True, verbose_name='средний чек неэко')),
                ('customer', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='maket.customer_all')),
                ('period', models.ForeignKey(limit_choices_to={'period': 'YR'}, on_delete=django.db.models.deletion.CASCADE, to='salesreport.reportperiod')),
            ],
            options={
                'verbose_name': 'ежегодные данные',
                'abstract': False,
            },
        ),
        migrations.CreateModel(
            name='CustomerPeriodsQuarter',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('sales_with_vat', models.FloatField(default=0, null=True, verbose_name='продажи с НДС')),
                ('sales_eco_with_vat', models.FloatField(default=0, null=True, verbose_name='продажи эко с НДС')),
                ('sales_no_eco_with_vat', models.FloatField(default=0, null=True, verbose_name='продажи неэко с НДС')),
                ('profit', models.FloatField(default=0, null=True, verbose_name='прибыль')),
                ('profit_eco', models.FloatField(default=0, null=True, verbose_name='прибыль эко')),
                ('profit_no_eco', models.FloatField(default=0, null=True, verbose_name='прибыль неэко')),
                ('no_sales', models.SmallIntegerField(default=0, null=True, verbose_name='количество продаж')),
                ('no_sales_eco', models.SmallIntegerField(default=0, null=True, verbose_name='количество продаж эко')),
                ('no_sales_no_eco', models.SmallIntegerField(default=0, null=True, verbose_name='количество продаж неэко')),
                ('average_check', models.FloatField(default=0, null=True, verbose_name='редний чек')),
                ('average_check_eco', models.FloatField(default=0, null=True, verbose_name='средний чек эко')),
                ('average_check_no_eco', models.FloatField(default=0, null=True, verbose_name='средний чек неэко')),
                ('customer', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='maket.customer_all')),
                ('period', models.ForeignKey(limit_choices_to={'period': 'QT'}, on_delete=django.db.models.deletion.CASCADE, to='salesreport.reportperiod')),
            ],
            options={
                'verbose_name': 'ежевартальные данные',
                'abstract': False,
            },
        ),
        migrations.CreateModel(
            name='CustomerPeriodsMonth',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('sales_with_vat', models.FloatField(default=0, null=True, verbose_name='продажи с НДС')),
                ('sales_eco_with_vat', models.FloatField(default=0, null=True, verbose_name='продажи эко с НДС')),
                ('sales_no_eco_with_vat', models.FloatField(default=0, null=True, verbose_name='продажи неэко с НДС')),
                ('profit', models.FloatField(default=0, null=True, verbose_name='прибыль')),
                ('profit_eco', models.FloatField(default=0, null=True, verbose_name='прибыль эко')),
                ('profit_no_eco', models.FloatField(default=0, null=True, verbose_name='прибыль неэко')),
                ('no_sales', models.SmallIntegerField(default=0, null=True, verbose_name='количество продаж')),
                ('no_sales_eco', models.SmallIntegerField(default=0, null=True, verbose_name='количество продаж эко')),
                ('no_sales_no_eco', models.SmallIntegerField(default=0, null=True, verbose_name='количество продаж неэко')),
                ('average_check', models.FloatField(default=0, null=True, verbose_name='редний чек')),
                ('average_check_eco', models.FloatField(default=0, null=True, verbose_name='средний чек эко')),
                ('average_check_no_eco', models.FloatField(default=0, null=True, verbose_name='средний чек неэко')),
                ('customer', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='maket.customer_all')),
                ('period', models.ForeignKey(limit_choices_to={'period': 'MT'}, on_delete=django.db.models.deletion.CASCADE, to='salesreport.reportperiod')),
            ],
            options={
                'verbose_name': 'ежеесячные данные',
                'abstract': False,
            },
        ),
    ]
