from django.db import models


class Color_scheme(models.Model):
    """ color scheme IV, Grant, Eco """
    scheme_name = models.CharField(max_length=3)


class Print_place(models.Model):
    """ detail_name name of part of item
        print_name name of printing place clip/top/cap"""
    detail_name = models.CharField(max_length=20)
    place_name = models.CharField(max_length=20)


class Detail_set(models.Model):
    """details of item detail# if exist
                       name - name of detail
                       place - name of prinring place"""
    detail1 = models.BooleanField(default=True)
    detail1_name = models.CharField(max_length=60)
    detail1_place = models.ForeignKey(Print_place, models.SET_NULL, related_name='detail1', null=True, blank=True)
    detail2 = models.BooleanField(default=False)
    detail2_name = models.CharField(max_length=60)
    detail2_place = models.ForeignKey(Print_place, models.SET_NULL, related_name='detail2', null=True, blank=True)
    detail3 = models.BooleanField(default=False)
    detail3_name = models.CharField(max_length=60)
    detail3_place = models.ForeignKey(Print_place, models.SET_NULL, related_name='detail3', null=True, blank=True)
    detail4 = models.BooleanField(default=False)
    detail4_name = models.CharField(max_length=60)
    detail4_place = models.ForeignKey(Print_place, models.SET_NULL, related_name='detail4', null=True, blank=True)
    detail5 = models.BooleanField(default=False)
    detail5_name = models.CharField(max_length=60)
    detail5_place = models.ForeignKey(Print_place, models.SET_NULL, related_name='detail5', null=True, blank=True)


class Items(models.Model):
    """code - series code
       item_details - quantity of parts for total code """
    item_code = models.CharField(max_length=
                                 6)
    color_scheme = models.ForeignKey(Color_scheme, models.SET_NULL, null=True)
    item_details = models.SmallIntegerField
    details = models.ForeignKey(Detail_set, models.SET_NULL, null=True)

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
        code - HEX"""
    color_id = models.CharField(max_length=60)
    color_name = models.CharField(max_length=10)
    color_code = models.CharField(max_length=7)
    color_scheme = models.ForeignKey(Color_scheme, models.SET_NULL, null=True)


class Customer(models.Model):
    """type - agency, dealer, etc.
        number of Region"""
    name = models.CharField(max_length=255)
    address = models.CharField(max_length=255)
    type = models.CharField(max_length=30)
    region = models.CharField(max_length=2, default='77')
    group = models.CharField(max_length=255)


class Order(models.Model):
    """ date_num - 'date' part of order no (dmy)"""
    date = models.DateField('date of order')
    date_num = models.CharField(max_length=6)
    order_number = models.CharField(max_length=10)
    customer = models.ForeignKey(Customer, models.SET_NULL, null=True)


class Order_items(models.Model):
    """item_color - total color code back part of item code(after Item series)
        detail_color - should be extracted from item_color
        print_name - name of print"""
    order = models.ForeignKey(Order, on_delete=models.CASCADE)
    item_series = models.ForeignKey(Items, on_delete=models.CASCADE)
    item_color = models.CharField(max_length=10)
    detail1_color = models.CharField(max_length=10)
    detail2_color = models.CharField(max_length=10)
    detail3_color = models.CharField(max_length=10)
    detail4_color = models.CharField(max_length=10)
    detail5_color = models.CharField(max_length=10)
    item_quant = models.IntegerField(default=1)
    print_name = models.CharField(max_length=40)


class Order_item_print(models.Model):
    """quantity - number of colors
        shots - number of shots 1 or 2"""
    order_item = models.ForeignKey(Order_items, on_delete=models.CASCADE)
    place = models.ForeignKey(Print_place, models.SET_NULL, null=True)
    position = models.ForeignKey(Print_position, models.SET_NULL, null=True)
    quantity = models.SmallIntegerField(default=1)
    shots = models.SmallIntegerField(default=1)


class Item_to_type(models.Model):
    item_name = models.ForeignKey(Items, on_delete=models.CASCADE)
    print_type = models.ForeignKey(Print_type, on_delete=models.CASCADE)


class Item_to_position(models.Model):
    item_name = models.ForeignKey(Items, on_delete=models.CASCADE)
    position_name = models.ForeignKey(Print_position, on_delete=models.CASCADE)


class Item_to_color(models.Model):
    item_name = models.ForeignKey(Items, on_delete=models.CASCADE)
    place_name = models.ForeignKey(Print_place, on_delete=models.CASCADE)
