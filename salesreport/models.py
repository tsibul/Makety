from django.db import models
from maket.models import Customer, Detail_set, Item_color, Order_imports, Customer_groups, Customer_types


class Sales_docs(models.Model):
    sales_document = models.CharField(max_length=255)
    sales_doc_number = models.IntegerField
    sales_doc_date = models.DateField
    customer = models.ForeignKey(Customer, models.SET_NULL, null=True)
    total_sale_with_vat = models.IntegerField
    total_sale_without_vat = models.IntegerField
    total_buy_with_vat = models.IntegerField
    total_buy_without_vat = models.IntegerField
    order = models.ForeignKey(Order_imports, models.SET_NULL, null=True)

    def __repr__(self):
        return str(self.sales_doc_number) + ' от ' + str(self.sales_doc_date) + ' заказ ' + str(self.order.order_id)

    def __str__(self):
        return str(self.sales_doc_number) + ' от ' + str(self.sales_doc_date) + ' заказ ' + str(self.order.order_id)


class Sales_doc_imports(models.Model):
    import_date = models.DateField
    code = models.CharField(max_length=20)
    detail_set = models.ForeignKey(Detail_set, models.SET_NULL, null=True)
    color_code = models.CharField(max_length=20)
    item_color = models.ForeignKey(Item_color, models.SET_NULL, null=True)
    series_id = models.IntegerField(null=True)
    quantity = models.IntegerField
    buy_without_vat = models.FloatField
    buy_with_vat = models.FloatField
    sales_quantity = models.IntegerField
    sale_without_vat = models.FloatField
    sale_with_vat = models.FloatField
    sale_price_vat = models.FloatField

    def __repr__(self):
        return self.code

    def __str__(self):
        return str(self.code)

class Customer_all(models.Model):
    """type - agency, dealer, etc.
        number of Region"""
    form = models.CharField(max_length=255)
    name = models.CharField(max_length=255)
    address = models.CharField(max_length=255)
    inn = models.CharField(max_length=20, null=True)
    type = models.CharField(max_length=30)
    region = models.CharField(max_length=2)
    group = models.CharField(max_length=255)
    customer_group = models.ForeignKey(Customer_groups, models.SET_NULL, null=True, default=None)
    customer_type = models.ForeignKey(Customer_types, models.SET_NULL, null=True, default=None)
    frigat_id = models.CharField(max_length=30, default='')
    phone = models.CharField(max_length=255)
    all_phones = models.CharField(max_length=600, null=True)
    mail = models.CharField(max_length=255, null=True)
    all_mails = models.CharField(max_length=600, null=True)
    comment = models.CharField(max_length=255, null=True)
    our_manager = models.CharField(max_length=255)
    date_import = models.DateField(default='2010-01-01')
    customer = models.ForeignKey(Customer, models.SET_NULL, default=None, null=True)

    def __repr__(self):
        return self.name

    def __str__(self):
        return str(self.name)
