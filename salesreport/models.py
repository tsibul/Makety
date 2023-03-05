from django.db import models
import datetime

from maket.models.order_models import Order_imports
from maket.models.customer_models import Customer_all, Customer
from maket.models.print_color_models import Item_color
from maket.models.goods_models import Detail_set
from salesreport.report_period import ReportPeriod


class Sales_docs(models.Model):

    class Meta:
        verbose_name = 'отгрузочные документы'

    sales_document = models.CharField(max_length=255)
    sales_doc_number = models.CharField(max_length=20, null=True)
    sales_doc_date = models.DateField(default=datetime.date(2000, 1, 1))
    customer = models.ForeignKey(Customer_all, models.SET_NULL, null=True)
    quantity = models.FloatField(default=0)
    total_sale_with_vat = models.FloatField(default=0)
    total_sale_without_vat = models.FloatField(default=0)
    total_buy_with_vat = models.FloatField(default=0)
    total_buy_without_vat = models.FloatField(default=0)
    order = models.ForeignKey(Order_imports, models.SET_NULL, null=True)
    good_no_error = models.BooleanField(default=True)
    eco = models.BooleanField(default=True)
    week = models.ForeignKey(ReportPeriod, models.SET_NULL, null=True, default='', related_name='week')
    month = models.ForeignKey(ReportPeriod, models.SET_NULL, null=True, default='', related_name='month')
    quarter = models.ForeignKey(ReportPeriod, models.SET_NULL, null=True, default='', related_name='quarter')
    year = models.ForeignKey(ReportPeriod, models.SET_NULL, null=True, default='', related_name='year')

    def __repr__(self):
        return str(self.sales_doc_number) + ' от ' + str(self.sales_doc_date)

    def __str__(self):
        return str(self.sales_doc_number) + ' от ' + str(self.sales_doc_date)

    def set_periods(self):
        week = ReportPeriod.objects.get(period='WK', date_begin__lte=self.sales_doc_date,
                                        date_end__gte=self.sales_doc_date)
        month = ReportPeriod.objects.get(period='MT', date_begin__lte=self.sales_doc_date,
                                         date_end__gte=self.sales_doc_date)
        quarter = ReportPeriod.objects.get(period='QT', date_begin__lte=self.sales_doc_date,
                                           date_end__gte=self.sales_doc_date)
        year = ReportPeriod.objects.get(period='YR', date_begin__lte=self.sales_doc_date,
                                        date_end__gte=self.sales_doc_date)
        self.week = week
        self.month = month
        self.quarter = quarter
        self.year = year


class Sales_doc_imports(models.Model):
    """ Frigat fields from report:
    series_id
    good_id
    good_group_id
    good_group
    good_title
    good_name
    code_1
    """

    import_date = models.DateField(default=datetime.date(2000, 1, 1))
    code = models.CharField(max_length=30)
    detail_set = models.ForeignKey(Detail_set, models.SET_NULL, null=True)
    color_code = models.CharField(max_length=40, null=True)
    main_color = models.CharField(max_length=12, null=True)
    item_color = models.ForeignKey(Item_color, models.SET_NULL, null=True)
    series_id = models.IntegerField(null=True)
    good_id = models.IntegerField(null=True)
    good_group_id = models.IntegerField(null=True)
    good_group = models.CharField(max_length=255, null=True)
    good_title = models.CharField(max_length=255, null=True)
    good_name = models.CharField(max_length=255, null=True)
    code_1 = models.CharField(max_length=100, null=True)
    quantity = models.FloatField(default=0)
    sales_doc_name = models.CharField(max_length=255, default='Расходная накладная')
    sales_doc_no = models.CharField(max_length=20, null=True)
    sales_doc_date = models.DateField(default=datetime.date(2000, 1, 1))
    buy_without_vat = models.FloatField(default=0)
    buy_with_vat = models.FloatField(default=0)
    sales_quantity = models.FloatField(default=0)
    sale_without_vat = models.FloatField(default=0)
    sale_with_vat = models.FloatField(default=0)
    sale_price_vat = models.FloatField(default=0)
    customer_name = models.CharField(max_length=255, null=True)
    customer_frigat_id = models.IntegerField(null=True)
    customer_all = models.ForeignKey(Customer_all, models.SET_NULL, null=True)
    sales_doc = models.ForeignKey(Sales_docs, models.SET_NULL, null=True)

    def __repr__(self):
        return self.code

    def __str__(self):
        return str(self.code)


class CustomerPeriods(models.Model):
    class Meta:
        abstract = True
        verbose_name = 'periods where was transactions with Client'

    customer = models.ForeignKey(Customer_all, on_delete=models.CASCADE)
    sales_with_vat = models.FloatField(default=0, null=True, verbose_name='продажи с НДС')
    sales_eco_with_vat = models.FloatField(default=0, null=True, verbose_name='продажи эко с НДС')
    sales_no_eco_with_vat = models.FloatField(default=0, null=True, verbose_name='продажи неэко с НДС')
    profit = models.FloatField(default=0, null=True, verbose_name='прибыль')
    profit_eco = models.FloatField(default=0, null=True, verbose_name='прибыль эко')
    profit_no_eco = models.FloatField(default=0, null=True, verbose_name='прибыль неэко')
    no_sales = models.SmallIntegerField(default=0, null=True, verbose_name='количество продаж')
    no_sales_eco = models.SmallIntegerField(default=0, null=True, verbose_name='количество продаж эко')
    no_sales_no_eco = models.SmallIntegerField(default=0, null=True, verbose_name='количество продаж неэко')
    average_check = models.FloatField(default=0, null=True, verbose_name='редний чек')
    average_check_eco = models.FloatField(default=0, null=True, verbose_name='средний чек эко')
    average_check_no_eco = models.FloatField(default=0, null=True, verbose_name='средний чек неэко')


class CustomerPeriodsWeek(CustomerPeriods):

    class Meta(CustomerPeriods.Meta):
        verbose_name = 'еженедельные данные'

    period = models.ForeignKey(ReportPeriod, on_delete=models.CASCADE, limit_choices_to={'period': 'WK'})

    def __repr__(self):
        return self.customer.name + ' ' + self.period.name

    def __str__(self):
        return self.customer.name + ' ' + self.period.name


class CustomerPeriodsMonth(CustomerPeriods):

    class Meta(CustomerPeriods.Meta):
        verbose_name = 'ежеесячные данные'

    period = models.ForeignKey(ReportPeriod, on_delete=models.CASCADE, limit_choices_to={'period': 'MT'})

    def __repr__(self):
        return self.customer.name + ' ' + self.period.name

    def __str__(self):
        return self.customer.name + ' ' + self.period.name


class CustomerPeriodsQuarter(CustomerPeriods):

    class Meta(CustomerPeriods.Meta):
        verbose_name = 'ежевартальные данные'

    period = models.ForeignKey(ReportPeriod, on_delete=models.CASCADE, limit_choices_to={'period': 'QT'})

    def __repr__(self):
        return self.customer.name + ' ' + self.period.name

    def __str__(self):
        return self.customer.name + ' ' + self.period.name


class CustomerPeriodsYear(CustomerPeriods):

    class Meta(CustomerPeriods.Meta):
        verbose_name = 'ежегодные данные'

    period = models.ForeignKey(ReportPeriod, on_delete=models.CASCADE, limit_choices_to={'period': 'YR'})

    def __repr__(self):
        return self.customer.name + ' ' + self.period.name

    def __str__(self):
        return self.customer.name + ' ' + self.period.name

