from django.urls import path
from .views import bank_transaction_list

urlpatterns = [
    path('', bank_transaction_list, name='bank_transaction_list'),
]
