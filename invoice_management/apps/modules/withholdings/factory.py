import factory
from apps.modules.withholdings.models import Withholding
from apps.modules.invoices.factory import InvoiceFactory

class WithholdingFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = Withholding

    invoice = factory.SubFactory(InvoiceFactory)
    amount = factory.Faker("pydecimal", left_digits=4, right_digits=2, positive=True)
    withholding_type = factory.Faker("word")
    date_applied = factory.Faker("date_object")
