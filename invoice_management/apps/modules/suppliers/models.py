from django.db import models
from django.core.exceptions import ValidationError
from django.utils.translation import gettext_lazy as _
import re


class Supplier(models.Model):
    name = models.CharField(max_length=255, unique=True)  
    tax_id = models.CharField(max_length=50, unique=True)
    country = models.CharField(max_length=2) 

    def __str__(self):
        return self.name

    def clean(self):
        if not re.match(r"^[A-Za-z0-9-]+$", self.tax_id):
            raise ValidationError(_("Invalid tax ID format."), code="invalid_tax_id")

        if len(self.country) != 2:
            raise ValidationError(_("Country must be a 2-letter ISO code."), code="invalid_country")

    def save(self, *args, **kwargs):
        self.full_clean()  
        super().save(*args, **kwargs)
