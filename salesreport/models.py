from django.db import models
from maket.models import Customer, Detail_set, Item_color, Order_imports, Customer_groups


class Customers_sales(models.Model):
    customer_id = models.IntegerField
    customer_name = models.CharField(max_length=255)
    customer_type = models.CharField(max_length=20)
    customer = models.ForeignKey(Customer, models.SET_NULL, null=True)
    customer_group = models.ForeignKey(Customer_groups, models.SET_NULL, null=True)
    date_first = models.DateField


class Sales_docs(models.Model):
    sales_document = models.CharField(max_length=255)
    sales_doc_number = models.IntegerField
    sales_doc_date = models.DateField
    customer_sales = models.ForeignKey(Customers_sales, models.SET_NULL, null=True)
    total_sale_with_vat = models.IntegerField
    total_sale_without_vat = models.IntegerField
    total_buy_with_vat = models.IntegerField
    total_buy_without_vat = models.IntegerField
    order = models.ForeignKey(Order_imports, models.SET_NULL, null=True)


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


