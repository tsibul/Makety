from django.db import models
from django.core.files.storage import FileSystemStorage

from maket.models.order_models import Order_imports, Item_imports


fs_films = FileSystemStorage(location='files/films')
fs_additional = FileSystemStorage(location='files/additional')


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


    def __repr__(self):
        return self.additional_file.name

    def __str__(self):
        return str(self.additional_file.name)

