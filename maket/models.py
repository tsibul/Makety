from django.db import models


class Films(models.Model):
    film_id = models.IntegerField(default=0)
    date = models.DateField(default='')
    format = models.CharField(max_length=3, default='A5')


class Color_scheme(models.Model):
    """ color scheme IV, Grant, Eco """
    scheme_name = models.CharField(max_length=13)


class Print_place(models.Model):
    """ detail_name name of part of item
        print_name name of printing place clip/top/cap"""
    detail_name = models.CharField(max_length=20)
    place_name = models.CharField(max_length=30)


class Detail_set(models.Model):
    """details of item detail# if exist
        name - name of goods
        item_name - item code
        detail_name - name of detail
        detail_place - if prinring possible"""
    name = models.CharField(max_length=200, null=True, blank=True)
    item_name = models.CharField(max_length=20, null=True, blank=True)
    color_scheme = models.ForeignKey(Color_scheme, models.SET_NULL, null=True)
    detail1_name = models.CharField(max_length=60)
    detail1_place = models.BooleanField(default=False)
    detail2_name = models.CharField(max_length=60, default='', null=True, blank=True)
    detail2_place = models.BooleanField(default=False)
    detail3_name = models.CharField(max_length=60, default='', null=True, blank=True)
    detail3_place = models.BooleanField(default=False)
    detail4_name = models.CharField(max_length=60, default='', null=True, blank=True)
    detail4_place = models.BooleanField(default=False)
    detail5_name = models.CharField(max_length=60, default='', null=True, blank=True)
    detail5_place = models.BooleanField(default=False)


class Print_type(models.Model):
    """ Pad, screen, UW, soft_touch etc."""
    type_name = models.CharField(max_length=20)


class Print_position(models.Model):
    """ option - open/close pen, plain round
        orientation - left, right, opposite, back"""
    position_option = models.CharField(max_length=20)
    position_orientation = models.CharField(max_length=20)


class Item_color(models.Model):
    """ id - (07)
        name - name
        pantone - pantone color
        code - HEX"""
    color_id = models.CharField(max_length=10)
    pantone = models.CharField(max_length=20, default='')
    color_name = models.CharField(max_length=60)
    color_code = models.CharField(max_length=7)
    color_scheme = models.ForeignKey(Color_scheme, models.SET_NULL, null=True)


class Customer(models.Model):
    """type - agency, dealer, etc.
        number of Region"""
    name = models.CharField(max_length=255)
    address = models.CharField(max_length=255)
    inn = models.CharField(max_length=12, null=True)
    type = models.CharField(max_length=30)
    region = models.CharField(max_length=2, default='77')
    group = models.CharField(max_length=255)

class Manger(models.Model):
    """Customer managers """
    manager = models.CharField(max_length=100, blank=True, null=True, default='')
    manager_phone= models.CharField(max_length=50, blank=True, null=True, default='')
    manager_mail = models.CharField(max_length=50, blank=True, null=True, default='')


class Order_imports(models.Model):
    """ date_num - 'date' part of order no (dmy)
    order_quantity — total items
    order_sum — total amount
    print_quantity — number of prints
    print_sum — amount for prints only
    """
    order_id = models.CharField(max_length=18, blank=True, null=True)
    order_date = models.DateField(default='1000-01-01')
    date_num = models.CharField(max_length=6 , blank=True, null=True)
    supplier = models.CharField(max_length=50, blank=True, null=True)
    customer_name = models.CharField(max_length=255, blank=True, null=True)
    customer_INN = models.CharField(max_length=12, blank=True, null=True)
    customer_address = models.CharField(max_length=120, blank=True, null=True)
    customer = models.ForeignKey(Customer, models.SET_NULL, null=True)
    film = models.ForeignKey(Films, models.SET_NULL, null=True, default=None)
    film_status = models.BooleanField(default=True)
    order_quantity = models.IntegerField(default=0)
    order_sum = models.FloatField(default=0)
    print_quantity = models.IntegerField(default=0)
    print_sum = models.FloatField(default=0)
    our_manager = models.CharField(max_length=50, blank=True, null=True, default='')
    manager = models.ForeignKey(Manger, models.SET_NULL, blank=True, null=True, default='')

class Item_imports(models.Model):
    """item_color - total color code back part of item code(after Item series)
        detail_color - should be extracted from item_color
        print_name - name of print"""
    print_id = models.IntegerField(default=0)
    item = models.ForeignKey(Detail_set, models.SET_NULL, null=True)
    code = models.CharField(max_length=20, blank=True, null=True)
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
    item_price = models.FloatField(default=0)
    print_price = models.FloatField(default=0)
    num_prints = models.IntegerField(default=0)


class Print_imports(models.Model):
    """quantity - number of colors
        shots - number of shots 1 or 2"""
    place = models.CharField(max_length=30, blank=True, null=True)
    type = models.CharField(max_length=20, blank=True, null=True)
    colors = models.SmallIntegerField(default=1)
    second_pass = models.BooleanField(default=False)
    item = models.ForeignKey(Item_imports, on_delete=models.CASCADE, null=True)
    print_id = models.IntegerField(default=0)
    print_price = models.FloatField(default=0)


class Order_item_print(models.Model):
    """quantity - number of colors
        shots - number of shots 1 or 2"""
    order_item = models.ForeignKey(Item_imports, on_delete=models.CASCADE)
    place = models.ForeignKey(Print_place, models.SET_NULL, null=True)
    position = models.ForeignKey(Print_position, models.SET_NULL, null=True)
    quantity = models.SmallIntegerField(default=1)
    shots = models.SmallIntegerField(default=1)


class Makety(models.Model):
    date_create = models.DateField(blank=True)
    date_modified = models.DateField(blank=True, null=True)
    maket_id = models.SmallIntegerField(default=0)
    uploaded = models.BooleanField(default=False)
    maket_file = models.FilePathField(null=True, blank=True)
    comment = models.CharField(max_length=255, default='')
    order = models.ForeignKey(Order_imports, models.SET_NULL, null=True)
    order_num = models.CharField(max_length=18, blank=True, null=True)
    order_date = models.DateField(default='1000-01-01')


class Itemgroup_in_Maket(models.Model):
    """If item from order exists in Maket"""
    item = models.ForeignKey(Detail_set, models.SET_NULL, null=True, blank=True)
    maket = models.ForeignKey(Makety, models.SET_NULL, null=True, blank=True)
    checked = models.BooleanField(default=True)


class Print_in_Maket(models.Model):
    """If print item shows big in Maket"""
    print_item = models.ForeignKey(Print_imports, models.SET_NULL, null=True, blank=True)
    maket = models.ForeignKey(Makety, models.SET_NULL, null=True, blank=True)
    checked = models.BooleanField(default=True)


class Item_in_Film(models.Model):
    """If item correctly outputed in film"""
    item = models.ForeignKey(Item_imports, models.SET_NULL, null=True, blank=True)
    film = models.ForeignKey(Films, models.SET_NULL, null=True, blank=True)
    status = models.BooleanField(default=True)


