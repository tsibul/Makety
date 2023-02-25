from django.db import models


class Good_matrix_type(models.Model):
    matrix_name = models.CharField(max_length=140)

    def __repr__(self):
        return self.matrix_name

    def __str__(self):
        return str(self.matrix_name)


class Good_crm_type(models.Model):
    crm_name = models.CharField(max_length=140)

    def __repr__(self):
        return self.crm_name

    def __str__(self):
        return str(self.crm_name)
