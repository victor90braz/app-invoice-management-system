from django.db import models
from apps.modules.suppliers.models import Supplier
from django.core.exceptions import ValidationError
from django.utils.translation import gettext_lazy as _
from datetime import date


class Invoice(models.Model):
    supplier = models.ForeignKey(Supplier, on_delete=models.CASCADE)
    due_date = models.DateField()
    total_amount = models.DecimalField(max_digits=10, decimal_places=2)

    def __str__(self):
        return f"Invoice {self.id} - {self.supplier.name}"

    def clean(self):
        if self.total_amount < 0:
            raise ValidationError(_("Total amount cannot be negative."), code="negative_total_amount")

        if self.due_date < date.today():
            raise ValidationError(_("Due date cannot be in the past."), code="invalid_due_date")

    def save(self, *args, **kwargs):
        self.full_clean()  
        super().save(*args, **kwargs)
