from django.http import JsonResponse
from rest_framework.request import Request
from django.core.paginator import Paginator
from .models import Withholding

def withholding_list(request: Request):
    page_number = request.GET.get('page', 1)
    limit = request.GET.get('limit', 10)
    withholdings = Withholding.objects.order_by('id')  
    paginator = Paginator(withholdings, limit)
    page_obj = paginator.get_page(page_number)

    data = {
        "page": page_obj.number,
        "total": paginator.count,
        "withholdings": [
            {
                "id": w.id,
                "invoice": w.invoice_id,
                "amount": str(w.amount),
                "withholding_type": w.withholding_type,
                "date_applied": w.date_applied.isoformat(),
            } for w in page_obj
        ],
    }
    return JsonResponse(data)
