from rest_framework import serializers
from apps.modules.invoices.models import Invoice
from datetime import date

class InvoiceSerializer(serializers.ModelSerializer):
    supplier_name = serializers.CharField(source="supplier.name", read_only=True)

    class Meta:
        model = Invoice
        fields = ["id", "supplier", "supplier_name", "due_date", "total_amount"]

    def validate_total_amount(self, value):
        if value < 0:
            raise serializers.ValidationError("Total amount cannot be negative.")
        return value

    def validate_due_date(self, value):
        if value < date.today():
            raise serializers.ValidationError("Due date cannot be in the past.")
        return value