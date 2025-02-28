from django.db import models
from apps.modules.invoices.models import Invoice

class Withholding(models.Model):
    invoice = models.ForeignKey(Invoice, on_delete=models.CASCADE)
    amount = models.DecimalField(max_digits=10, decimal_places=2)
    withholding_type = models.CharField(max_length=50)
    date_applied = models.DateField()

    def __str__(self):
        return f"Withholding {self.withholding_type} - Invoice {self.invoice.id}"
