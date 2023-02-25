from django.db import models
from django.core.files.storage import FileSystemStorage
from maket.models.customer_models import Customer
from maket.models.persons_models import Manger
from maket.models.print_color_models import Print_position, Print_place
from maket.models.goods_models import Detail_set


fs_orders = FileSystemStorage(location='files/orders')


class Order_imports(models.Model):
    """ date_num - 'date' part of order no (dmy)
    order_quantity — total items
    order_sum — total amount
    print_quantity — number of prints
    print_sum — amount for prints only
    to_check — possible import errors
    """
    order_id = models.CharField(max_length=18, blank=True, null=True)
    order_date = models.DateField(default='1000-01-01')
    supplier = models.CharField(max_length=50, blank=True, null=True)
    customer_name = models.CharField(max_length=255, blank=True, null=True)
    customer_INN = models.CharField(max_length=12, blank=True, null=True)
    customer_address = models.CharField(max_length=255, blank=True, null=True)
    customer = models.ForeignKey(Customer, models.SET_NULL, null=True)
    order_quantity = models.IntegerField(default=0)
    order_sum = models.FloatField(default=0)
    print_quantity = models.IntegerField(default=0)
    print_sum = models.FloatField(default=0)
    our_manager = models.CharField(max_length=50, blank=True, null=True, default='')
    manager = models.ForeignKey(Manger, models.SET_NULL, blank=True, null=True, default='')
    Ready = 'R'
    Partial = 'P'
    NotReady = 'N'
    status_choices = [(Ready, 'R'), (Partial, 'P'), (NotReady, 'N')]
    maket_status = models.CharField(max_length=1, choices=status_choices, default=NotReady)
    order_upload = models.BooleanField(default=False)
    order_file = models.FileField(storage=fs_orders, null=True, blank=True)
    to_check = models.BooleanField(default=False)
    number_orders = models.SmallIntegerField(default=0)
    number_makets = models.SmallIntegerField(default=0)
    number_additional = models.SmallIntegerField(default=0)

    def __repr__(self):
        return self.order_id

    def __str__(self):
        return str(self.order_id + ' ' + self.customer.name)


class Item_imports(models.Model):
    """item_color - total color code back part of item code(after Item series)
        detail_color - should be extracted from item_color
        print_name - name of print"""
    print_id = models.IntegerField(default=0)
    item = models.ForeignKey(Detail_set, models.SET_NULL, null=True)
    code = models.CharField(max_length=40, blank=True, null=True)
    name = models.CharField(max_length=100, blank=True, null=True)
    quantity = models.IntegerField(default=0)
    print_name = models.CharField(max_length=50, blank=True, null=True)
    order = models.ForeignKey(Order_imports, on_delete=models.CASCADE, null=True)
    item_group = models.CharField(max_length=20, default='', blank=True, null=True)
    item_color = models.CharField(max_length=40, default='', blank=True, null=True)
    detail1_color = models.CharField(max_length=10, default='', blank=True, null=True)
    detail2_color = models.CharField(max_length=10, default='', blank=True, null=True)
    detail3_color = models.CharField(max_length=10, default='', blank=True, null=True)
    detail4_color = models.CharField(max_length=10, default='', blank=True, null=True)
    detail5_color = models.CharField(max_length=10, default='', blank=True, null=True)
    detail6_color = models.CharField(max_length=10, default='', blank=True, null=True)
    detail1_hex = models.CharField(max_length=7, default='', blank=True, null=True)
    detail2_hex = models.CharField(max_length=7, default='', blank=True, null=True)
    detail3_hex = models.CharField(max_length=7, default='', blank=True, null=True)
    detail4_hex = models.CharField(max_length=7, default='', blank=True, null=True)
    detail5_hex = models.CharField(max_length=7, default='', blank=True, null=True)
    detail6_hex = models.CharField(max_length=7, default='', blank=True, null=True)
    item_price = models.FloatField(default=0)
    print_price = models.FloatField(default=0)
    num_prints = models.IntegerField(default=0)

    def __repr__(self):
        return self.code + ' ' + self.print_name

    def __str__(self):
        return str(self.code + ' ' + self.print_name)


class Print_imports(models.Model):
    """quantity - number of colors
        shots - number of shots 1 or 2"""
    place = models.CharField(max_length=30, blank=True, null=True)
    print_place = models.ForeignKey(Print_place, models.SET_NULL, null=True)
    type = models.CharField(max_length=30, blank=True, null=True)
    colors = models.SmallIntegerField(default=1)
    second_pass = models.BooleanField(default=False)
    item = models.ForeignKey(Item_imports, on_delete=models.CASCADE, null=True)
    print_id = models.IntegerField(default=0)
    print_price = models.FloatField(default=0)
    print_position = models.ForeignKey(Print_position, models.SET_NULL, null=True, default='')


class Print_color(models.Model):
    """Colors of printing"""
    color_pantone = models.CharField(max_length=40, default='')
    color_hex = models.CharField(max_length=7, default='')
    color_number_in_item = models.SmallIntegerField(default=1)
    print_item = models.ForeignKey(Print_imports, on_delete=models.CASCADE)

    def __repr__(self):
        return str(self.color_number_in_item + self.color_pantone)

    def __str__(self):
        return str(self.color_number_in_item + self.color_pantone)
