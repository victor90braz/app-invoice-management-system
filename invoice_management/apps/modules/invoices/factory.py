import factory
from apps.modules.invoices.models import Invoice
from apps.modules.suppliers.factories import SupplierFactory

class InvoiceFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = Invoice

    supplier = factory.SubFactory(SupplierFactory)
    total_amount = factory.Faker("pydecimal", left_digits=4, right_digits=2, positive=True)
    due_date = factory.Faker("date_object")
