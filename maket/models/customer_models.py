from django.db import models
import datetime
from maket.models.customer_group_models import Customer_types, Customer_groups

class Customer_all(models.Model):
    """type - agency, dealer, etc.
        number of Region"""
    form = models.CharField(max_length=255, blank=True)
    name = models.CharField(max_length=255)
    address = models.CharField(max_length=255, blank=True)
    inn = models.CharField(max_length=20, null=True)
    region = models.CharField(max_length=2)
    customer_group = models.ForeignKey(Customer_groups, models.SET_NULL, null=True, default=None)
    customer_type = models.ForeignKey(Customer_types, models.SET_NULL, null=True, default=None)
    frigat_id = models.CharField(max_length=30, default='', db_index=True)
    phone = models.CharField(max_length=255, blank=True)
    all_phones = models.CharField(max_length=600, null=True, blank=True)
    mail = models.CharField(max_length=255, null=True, blank=True)
    all_mails = models.CharField(max_length=600, null=True, blank=True)
    comment = models.CharField(max_length=255, null=True, blank=True)
    our_manager = models.CharField(max_length=255, blank=True)
    date_import = models.DateField(default=datetime.date(2000, 1, 1))
    date_first = models.DateField(default=datetime.date(2000, 1, 1))
    date_last = models.DateField(default=datetime.date(2000, 1, 1))
    active = models.BooleanField(default=True)
    internal = models.BooleanField(default=False)


    def __repr__(self):
        return self.name

    def __str__(self):
        return str(self.name)


class Customer(models.Model):
    """type - agency, dealer, etc.
        number of Region"""
    name = models.CharField(max_length=255)
    address = models.CharField(max_length=255)
    inn = models.CharField(max_length=12, null=True)
    region = models.CharField(max_length=2, default='77')
    customer_group = models.ForeignKey(Customer_groups, models.SET_NULL, null=True, default=None)
    customer_type = models.ForeignKey(Customer_types, models.SET_NULL, null=True, default=None)
    customer_all = models.ForeignKey(Customer_all, models.SET_NULL, null=True, default=None)

    def __repr__(self):
        return self.name

    def __str__(self):
        return str(self.name)
