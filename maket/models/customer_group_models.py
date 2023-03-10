from django.db import models
import datetime


class Customer_types(models.Model):
    type_name = models.CharField(max_length=30)
    group_discount = models.FloatField(default=0)
    code = models.CharField(max_length=2, default='')

    def __repr__(self):
        return self.type_name

    def __str__(self):
        return str(self.type_name)


class Customer_groups(models.Model):
    group_name = models.CharField(max_length=255, unique=True)
    group_type = models.ForeignKey(Customer_types, models.SET_NULL, null=True)
    phone = models.CharField(max_length=255, default='')
    mail = models.CharField(max_length=255, default='')
    date_first = models.DateField(default=datetime.date(2000, 1, 1))
    date_last = models.DateField(default=datetime.date(2000, 1, 1))
    active = models.BooleanField(default=True)


    def __repr__(self):
        return self.group_name

    def __str__(self):
        return str(self.group_name)
