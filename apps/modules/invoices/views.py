import logging
import json
from django.http import HttpResponse
from rest_framework import status
from rest_framework.request import Request
from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import IsAuthenticated
from rest_framework.exceptions import NotFound, ValidationError
from .models import Invoice
from .serializers import InvoiceSerializer
from .pagination import StandardPagination

logger = logging.getLogger(__name__)

@api_view(["GET"])
def invoice_list(request: Request):
    try:
        paginator = StandardPagination()
        invoices = Invoice.objects.select_related("supplier").order_by("id")

        if not invoices.exists():
            return HttpResponse(
                json.dumps({"message": "No invoices found", "invoices": []}),
                content_type="application/json",
            )

        paginated_invoices = paginator.paginate_queryset(invoices, request)
        if paginated_invoices is None:
            raise NotFound("Invalid pagination parameters.")

        serialized_invoices = InvoiceSerializer(paginated_invoices, many=True).data
        return paginator.get_paginated_response(serialized_invoices)

    except Exception as error:
        logger.error(f"Error in invoice_list: {error}", exc_info=True)
        raise ValidationError(f"Unexpected error: {error}")

@api_view(["POST"])
@permission_classes([IsAuthenticated])
def create_invoice(request: Request):
    try:
        serializer = InvoiceSerializer(data=request.data)

        if serializer.is_valid():
            serializer.save()
            return HttpResponse(
                json.dumps({"message": "Invoice created successfully", "invoice": serializer.data}),
                status=status.HTTP_201_CREATED,
                content_type="application/json",
            )

        logger.warning(f"Validation errors in create_invoice: {serializer.errors}")
        raise ValidationError(serializer.errors)

    except ValidationError as error:
        logger.error(f"Validation error in create_invoice: {error}", exc_info=True)
        raise error

    except Exception as error:
        logger.error(f"Unexpected error in create_invoice: {error}", exc_info=True)
        raise ValidationError(f"Unexpected error: {error}")
