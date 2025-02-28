from django.db import models

class Supplier(models.Model):
    name = models.CharField(max_length=255)
    tax_id = models.CharField(max_length=50, unique=True)
    country = models.CharField(max_length=100)

    def __str__(self):
        return self.name
