from django.db import models
import datetime

from maket.models.order_models import Order_imports
from maket.models.customer_models import Customer_all, Customer
from maket.models.print_color_models import Item_color
from maket.models.goods_models import Detail_set

class Sales_docs(models.Model):
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

    def __repr__(self):
        return str(self.sales_doc_number) + ' от ' + str(self.sales_doc_date) + ' заказ ' + str(self.order.order_id)

    def __str__(self):
        return str(self.sales_doc_number) + ' от ' + str(self.sales_doc_date) + ' заказ ' + str(self.order.order_id)


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

