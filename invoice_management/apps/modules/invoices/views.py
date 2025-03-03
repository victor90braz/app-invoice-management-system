from django.http import JsonResponse
from django.shortcuts import get_object_or_404
from rest_framework.request import Request
from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import IsAuthenticated
from datetime import datetime
from .models import Invoice
from apps.modules.suppliers.models import Supplier
from .serializers import InvoiceSerializer
from .pagination import StandardPagination


@api_view(["GET"])
@permission_classes([IsAuthenticated])
def invoice_list(request: Request):
    try:
        paginator = StandardPagination()
        invoices = Invoice.objects.select_related("supplier").order_by("id")

        if not invoices.exists():
            return JsonResponse({"message": "No invoices found", "invoices": []}, status=200)

        paginated_invoices = paginator.paginate_queryset(invoices, request)
        serialized_invoices = InvoiceSerializer(paginated_invoices, many=True).data
        return paginator.get_paginated_response(serialized_invoices)

    except Exception as error:
        return JsonResponse({"error": str(error)}, status=500)


@api_view(["POST"])
@permission_classes([IsAuthenticated])
def create_invoice(request: Request):
    serializer = InvoiceSerializer(data=request.data)

    if serializer.is_valid():
        serializer.save()
        return JsonResponse(
            {"message": "Invoice created successfully", "invoice": serializer.data}, status=201
        )

    return JsonResponse({"error": serializer.errors}, status=400)
