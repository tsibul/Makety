from django.db import models
from django.core.files.storage import FileSystemStorage

from maket.models.order_models import Order_imports, Item_imports, Print_imports
from maket.models.films_addfiles_models import Films

fs_makety = FileSystemStorage(location='files/makety')


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


class Itemgroup_in_Maket(models.Model):
    """If item from order exists in Maket"""
    item = models.ForeignKey(Item_imports, on_delete=models.CASCADE, null=True, blank=True)
    maket = models.ForeignKey(Makety, on_delete=models.CASCADE, null=True, blank=True)
    checked = models.BooleanField(default=True)
    print_name = models.CharField(max_length=50,  null=True, blank=True)
    film = models.ForeignKey(Films, models.SET_NULL, blank=True, null=True)
    film_error = models.BooleanField(default=True)

    def __repr__(self):
        return str(self.maket.order_num + ' ' + self.item.item.print_group.name)

    def __str__(self):
        return str(self.maket.order_num + ' ' + self.item.item.print_group.name)


class Print_in_Maket(models.Model):
    """If print item shows big in Maket"""
    print_item = models.ForeignKey(Print_imports, models.SET_NULL, null=True, blank=True)
    maket = models.ForeignKey(Makety, on_delete=models.CASCADE, null=True, blank=True)
    checked = models.BooleanField(default=True)
    option = models.SmallIntegerField(default=1)



