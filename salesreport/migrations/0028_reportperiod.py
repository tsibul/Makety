# Generated by Django 4.0.4 on 2023-03-04 11:28

import datetime
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('salesreport', '0027_alter_sales_doc_imports_color_code'),
    ]

    operations = [
        migrations.CreateModel(
            name='ReportPeriod',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('period', models.CharField(choices=[('WK', 'неделя'), ('MT', 'месяц'), ('QT', 'квартал'), ('YR', 'год'), ('DY', 'день'), ('UD', 'произвольный')], default='MT', max_length=2)),
                ('date_begin', models.DateField(default=datetime.date(2000, 1, 1))),
                ('date_end', models.DateField(default=datetime.date(2000, 1, 31))),
                ('name', models.CharField(max_length=100)),
            ],
        ),
    ]
