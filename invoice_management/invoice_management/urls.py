from django.contrib import admin
from django.urls import include, path

urlpatterns = [
    path('admin/', admin.site.urls),
    path('suppliers/', include('apps.modules.suppliers.urls')),
    path('invoices/', include('apps.modules.invoices.urls')),
    path('bank-reconciliation/', include('apps.modules.bank_reconciliation.urls')),
]
