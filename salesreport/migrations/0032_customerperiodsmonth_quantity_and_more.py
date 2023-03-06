# Generated by Django 4.0.4 on 2023-03-05 14:18

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('salesreport', '0031_customerperiodsyear_customerperiodsquarter_and_more'),
    ]

    operations = [
        migrations.AddField(
            model_name='customerperiodsmonth',
            name='quantity',
            field=models.IntegerField(default=0, verbose_name='количество'),
        ),
        migrations.AddField(
            model_name='customerperiodsmonth',
            name='quantity_eco',
            field=models.IntegerField(default=0, verbose_name='количество эко'),
        ),
        migrations.AddField(
            model_name='customerperiodsmonth',
            name='quantity_no_eco',
            field=models.IntegerField(default=0, verbose_name='количество неэко'),
        ),
        migrations.AddField(
            model_name='customerperiodsquarter',
            name='quantity',
            field=models.IntegerField(default=0, verbose_name='количество'),
        ),
        migrations.AddField(
            model_name='customerperiodsquarter',
            name='quantity_eco',
            field=models.IntegerField(default=0, verbose_name='количество эко'),
        ),
        migrations.AddField(
            model_name='customerperiodsquarter',
            name='quantity_no_eco',
            field=models.IntegerField(default=0, verbose_name='количество неэко'),
        ),
        migrations.AddField(
            model_name='customerperiodsweek',
            name='quantity',
            field=models.IntegerField(default=0, verbose_name='количество'),
        ),
        migrations.AddField(
            model_name='customerperiodsweek',
            name='quantity_eco',
            field=models.IntegerField(default=0, verbose_name='количество эко'),
        ),
        migrations.AddField(
            model_name='customerperiodsweek',
            name='quantity_no_eco',
            field=models.IntegerField(default=0, verbose_name='количество неэко'),
        ),
        migrations.AddField(
            model_name='customerperiodsyear',
            name='quantity',
            field=models.IntegerField(default=0, verbose_name='количество'),
        ),
        migrations.AddField(
            model_name='customerperiodsyear',
            name='quantity_eco',
            field=models.IntegerField(default=0, verbose_name='количество эко'),
        ),
        migrations.AddField(
            model_name='customerperiodsyear',
            name='quantity_no_eco',
            field=models.IntegerField(default=0, verbose_name='количество неэко'),
        ),
        migrations.AlterField(
            model_name='customerperiodsmonth',
            name='average_check',
            field=models.FloatField(default=0, null=True, verbose_name='средний чек'),
        ),
        migrations.AlterField(
            model_name='customerperiodsquarter',
            name='average_check',
            field=models.FloatField(default=0, null=True, verbose_name='средний чек'),
        ),
        migrations.AlterField(
            model_name='customerperiodsweek',
            name='average_check',
            field=models.FloatField(default=0, null=True, verbose_name='средний чек'),
        ),
        migrations.AlterField(
            model_name='customerperiodsyear',
            name='average_check',
            field=models.FloatField(default=0, null=True, verbose_name='средний чек'),
        ),
    ]
