from django.db import models


class Manger(models.Model):
    """Customer managers """
    manager = models.CharField(max_length=100, blank=True, null=True, default='')
    manager_phone = models.CharField(max_length=50, blank=True, null=True, default='')
    manager_mail = models.CharField(max_length=50, blank=True, null=True, default='')

    def __repr__(self):
        return self.manager

    def __str__(self):
        return str(self.manager)


