import logging
from django.http import JsonResponse
from rest_framework.request import Request
from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import IsAuthenticated
from rest_framework.exceptions import NotFound
from .models import Invoice
from .serializers import InvoiceSerializer
from .pagination import StandardPagination

logger = logging.getLogger(__name__)

@api_view(["GET"])
@permission_classes([IsAuthenticated])
def invoice_list(request: Request):
    try:
        paginator = StandardPagination()
        invoices = Invoice.objects.select_related("supplier").order_by("id")

        if not invoices.exists():
            return JsonResponse({"message": "No invoices found", "invoices": []}, status=200)

        paginated_invoices = paginator.paginate_queryset(invoices, request)
        if paginated_invoices is None:
            raise NotFound("Invalid pagination parameters.")

        serialized_invoices = InvoiceSerializer(paginated_invoices, many=True).data
        return paginator.get_paginated_response(serialized_invoices)

    except Exception as error:
        logger.error(f"Error in invoice_list: {str(error)}")
        return JsonResponse({"error": "An internal server error occurred."}, status=500)


@api_view(["POST"])
@permission_classes([IsAuthenticated])
def create_invoice(request: Request):
    serializer = InvoiceSerializer(data=request.data)

    if serializer.is_valid():
        serializer.save()
        return JsonResponse(
            {"message": "Invoice created successfully", "invoice": serializer.data}, status=201
        )

    logger.warning(f"Validation errors in create_invoice: {serializer.errors}")
    return JsonResponse({"errors": serializer.errors}, status=400)
