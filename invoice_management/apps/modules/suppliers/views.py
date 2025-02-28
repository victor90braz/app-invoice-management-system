from django.core.paginator import Paginator
from django.http import JsonResponse
from .models import Supplier

def supplier_list(request):
    page_number = request.GET.get('page', 1)
    limit = request.GET.get('limit', 10)
    suppliers = Supplier.objects.all()
    paginator = Paginator(suppliers, limit)
    page_obj = paginator.get_page(page_number)
    data = {
        "page": page_obj.number,
        "total": paginator.count,
        "suppliers": [
            {
                "id": supplier.id,
                "name": supplier.name,
                "tax_id": supplier.tax_id,
                "country": supplier.country,
            } for supplier in page_obj
        ],
    }
    return JsonResponse(data)
