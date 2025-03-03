from rest_framework import serializers
from apps.modules.invoices.models import Invoice

class InvoiceSerializer(serializers.ModelSerializer):
    supplier_name = serializers.CharField(source="supplier.name", read_only=True)

    class Meta:
        model = Invoice
        fields = ["id", "supplier", "supplier_name", "due_date", "total_amount"]  

    def validate(self, data):
        instance = Invoice(**data)
        instance.full_clean()
        return data

