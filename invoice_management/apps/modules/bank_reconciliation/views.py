from django.http import JsonResponse
from rest_framework.request import Request
from django.core.paginator import Paginator
from .models import BankTransaction

def bank_transaction_list(request: Request):
    page_number = request.GET.get('page', 1)
    limit = request.GET.get('limit', 10)
    transactions = BankTransaction.objects.all()
    paginator = Paginator(transactions, limit)
    page_obj = paginator.get_page(page_number)

    data = {
        "page": page_obj.number,
        "total": paginator.count,
        "transactions": [
            {
                "id": txn.id,
                "invoice": txn.invoice_id,
                "transaction_id": txn.transaction_id,
                "amount": str(txn.amount),
                "transaction_date": txn.transaction_date.isoformat() if txn.transaction_date else None,
            } for txn in page_obj
        ],
    }
    return JsonResponse(data)
