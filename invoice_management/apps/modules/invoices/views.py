import json
from django.http import JsonResponse
from rest_framework.request import Request
from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import IsAuthenticated
from django.core.paginator import Paginator
from django.shortcuts import get_object_or_404
from apps.modules.suppliers.models import Supplier
from .models import Invoice

@api_view(["GET"])
@permission_classes([IsAuthenticated])  
def invoice_list(request: Request):
    try:
        page_number = request.GET.get("page", 1)
        limit = request.GET.get("limit", 10)

        invoices = Invoice.objects.select_related("supplier").order_by("id")

        paginator = Paginator(invoices, limit)
        page_obj = paginator.get_page(page_number)

        data = {
            "page": page_obj.number,
            "total": paginator.count,
            "invoices": [
                {
                    "id": invoice.id,
                    "supplier": {
                        "id": invoice.supplier.id,
                        "name": invoice.supplier.name
                    },
                    "total_amount": str(invoice.total_amount),
                    "due_date": invoice.due_date.isoformat() if invoice.due_date else None,
                } for invoice in page_obj
            ],
        }
        return JsonResponse(data)

    except Exception as e:
        return JsonResponse({"error": str(e)}, status=500)


@api_view(["POST"])
@permission_classes([IsAuthenticated])  
def create_invoice(request: Request):
    try:
        data = request.data  

        supplier_id = data.get("supplier")
        due_date = data.get("due_date")
        items = data.get("items")

        if not supplier_id:
            return JsonResponse({"error": "Supplier is required"}, status=400)

        supplier = get_object_or_404(Supplier, id=supplier_id)

        if not due_date:
            return JsonResponse({"error": "due_date is required"}, status=400)

        if not isinstance(items, list) or not items:
            return JsonResponse({"error": "Items must be a non-empty array"}, status=400)

        invoice = Invoice.objects.create(
            supplier=supplier,
            due_date=due_date,
            total_amount=0  
        )

        return JsonResponse(
            {"message": "Invoice created successfully", "invoice_id": invoice.id},
            status=201
        )

    except json.JSONDecodeError:
        return JsonResponse({"error": "Invalid JSON format"}, status=400)

    except Exception as e:
        print("Error in create_invoice:", str(e))  
        return JsonResponse({"error": str(e)}, status=500)
