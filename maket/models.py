from django.db import models
from django.core.files.storage import FileSystemStorage

fs_orders = FileSystemStorage(location='files/orders')
fs_makety = FileSystemStorage(location='files/makety')
fs_films = FileSystemStorage(location='files/films')
fs_patterns = FileSystemStorage(location='files/patterns')
fs_additional = FileSystemStorage(location='files/additional')

class Color_scheme(models.Model):
    """ color scheme IV, Grant, Eco """
    scheme_name = models.CharField(max_length=13)

    def __repr__(self):
        return self.scheme_name

    def __str__(self):
        return str(self.scheme_name)


class Print_group(models.Model):
    """code for similar shapes of items"""
    code = models.CharField(max_length=7, default=0)
    name = models.CharField(max_length=255)
    options = models.SmallIntegerField(default=1)
    layout = models.CharField(max_length=120, blank=True, default='')
    pattern_file = models.FileField(storage=fs_patterns, null=True, blank=True)
    item_width = models.DecimalField(default=39, max_digits=7, decimal_places=3)
    item_height = models.DecimalField(default=39, max_digits=7, decimal_places=3)

    def __repr__(self):
        return self.code

    def __str__(self):
        return str(self.code)


class Detail_set(models.Model):
    """details of item detail# if exist
        name - name of goods
        item_name - item code
        detail_name - name of detail
        detail_place - if prinring possible"""
    name = models.CharField(max_length=200, null=True, blank=True)
    item_name = models.CharField(max_length=20, null=True, blank=True)
    color_scheme = models.ForeignKey(Color_scheme, models.SET_NULL, null=True)
    print_group = models.ForeignKey(Print_group, models.SET_NULL, null=True)
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
    detail6_name = models.CharField(max_length=60, default='', null=True, blank=True)
    detail6_place = models.BooleanField(default=False)

    def __repr__(self):
        return self.name

    def __str__(self):
        return str(self.name)


class Print_type(models.Model):
    """ Pad, screen, UW, soft_touch etc."""
    type_name = models.CharField(max_length=20)

    def __str__(self):
        return str(self.type_name)


class Print_place(models.Model):
    """ detail_name name of part of item
        print_name name of printing place as in import"""
    detail_name = models.CharField(max_length=20)
    place_name = models.CharField(max_length=30)

    def __str__(self):
        return str(self.detail_name + ' ' + self.place_name)


class Print_position(models.Model):
    """ option - open/close pen, plain round
        orientation - left, right, opposite, back"""
    position_place = models.ForeignKey(Print_place, models.SET_NULL, null=True)
    print_group = models.ForeignKey(Print_group, on_delete=models.CASCADE, null=True)
    orientation_id = models.SmallIntegerField(default=1)
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

    def __str__(self):
        return str(self.color_id + ', ' + self.color_scheme.scheme_name)


class Customer(models.Model):
    """type - agency, dealer, etc.
        number of Region"""
    name = models.CharField(max_length=255)
    address = models.CharField(max_length=255)
    inn = models.CharField(max_length=12, null=True)
    type = models.CharField(max_length=30)
    region = models.CharField(max_length=2, default='77')
    group = models.CharField(max_length=255)

    def __repr__(self):
        return self.name

    def __str__(self):
        return str(self.name)


class Manger(models.Model):
    """Customer managers """
    manager = models.CharField(max_length=100, blank=True, null=True, default='')
    manager_phone = models.CharField(max_length=50, blank=True, null=True, default='')
    manager_mail = models.CharField(max_length=50, blank=True, null=True, default='')

    def __repr__(self):
        return self.manager

    def __str__(self):
        return str(self.manager)


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


class Makety(models.Model):
    date_create = models.DateField(blank=True)
    date_modified = models.DateField(blank=True, null=True)
    maket_id = models.SmallIntegerField(default=0)
    uploaded = models.BooleanField(default=False)
    maket_file = models.FileField(storage=fs_makety, null=True, blank=True)
    comment = models.CharField(max_length=255, default='')
    order = models.ForeignKey(Order_imports, on_delete=models.CASCADE, null=True)
    order_num = models.CharField(max_length=18, blank=True, null=True)
    order_date = models.DateField(default='1000-01-01')

    def __repr__(self):
        return self.order.order_id

    def __str__(self):
        return str(self.order.order_id + ' ' + self.order.customer.name)


class Films(models.Model):
    film_id = models.IntegerField(default=0)
    date = models.DateField(default='')
    format = models.CharField(max_length=3, default='A5')
    status = models.BooleanField(default=False)
    date_sent = models.DateField(default=None, null=True)
    film_upload = models.BooleanField(default=False)
    film_file = models.FileField(storage=fs_films, null=True, blank=True)

    def __repr__(self):
        return str(self.film_id) + ' от ' + str(self.date)

    def __str__(self):
        return str(self.film_id + ' от ' + self.date)


class Itemgroup_in_Maket(models.Model):
    """If item from order exists in Maket"""
    item = models.ForeignKey(Item_imports, on_delete=models.CASCADE, null=True, blank=True)
    maket = models.ForeignKey(Makety, on_delete=models.CASCADE, null=True, blank=True)
    checked = models.BooleanField(default=True)
    print_name = models.CharField(max_length=50,  null=True, blank=True)
    film = models.ForeignKey(Films, models.SET_NULL, blank=True, null=True)
    film_error = models.BooleanField(default=True)

    def __str__(self):
        return str(self.maket.order_num + ' ' + self.item.item.print_group.name)


class Print_in_Maket(models.Model):
    """If print item shows big in Maket"""
    print_item = models.ForeignKey(Print_imports, models.SET_NULL, null=True, blank=True)
    maket = models.ForeignKey(Makety, on_delete=models.CASCADE, null=True, blank=True)
    checked = models.BooleanField(default=True)
    option = models.SmallIntegerField(default=1)


class Item_in_Film(models.Model):
    """If item correctly outputed in film"""
    item = models.ForeignKey(Item_imports, models.SET_NULL, null=True, blank=True)
    film = models.ForeignKey(Films, models.SET_NULL, null=True, blank=True)
    status = models.BooleanField(default=True)


class Additional_Files(models.Model):
    """Additional files"""
    additional_file = models.FileField(storage=fs_additional, null=True, blank=True)
    additional_file_name = models.FilePathField(max_length=120)
    file_type = models.CharField(max_length=3, null=True, blank=True, default='pdf')
    comment = models.CharField(max_length=255, null=True, blank=True)
    order_id = models.ForeignKey(Order_imports, on_delete=models.CASCADE)

    def __str__(self):
        return str(self.additional_file.name)


class Print_color(models.Model):
    """Colors of printing"""
    color_pantone = models.CharField(max_length=40, default='')
    color_hex = models.CharField(max_length=7, default='')
    color_number_in_item = models.SmallIntegerField(default=1)
    print_item = models.ForeignKey(Print_imports, on_delete=models.CASCADE)

    def __str__(self):
        return str(self.color_number_in_item + self.color_pantone)
