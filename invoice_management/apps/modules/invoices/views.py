from rest_framework.request import Request
from django.http import JsonResponse
from .models import Invoice
from django.core.paginator import Paginator

def invoice_list(request: Request):
    page_number = request.GET.get('page', 1)
    limit = request.GET.get('limit', 10)
    invoices = Invoice.objects.all()
    paginator = Paginator(invoices, limit)
    page_obj = paginator.get_page(page_number)
    data = {
        "page": page_obj.number,
        "total": paginator.count,
        "invoices": [
            {
                "id": invoice.id,
                "supplier": invoice.supplier_id,
                "total_amount": invoice.total_amount,
                "due_date": invoice.due_date.isoformat() if invoice.due_date else None,
            } for invoice in page_obj
        ],
    }
    return JsonResponse(data)
