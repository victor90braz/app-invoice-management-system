import factory
from apps.modules.suppliers.models import Supplier

class SupplierFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = Supplier

    name = factory.Sequence(lambda n: f"Supplier {n}")
    tax_id = factory.Faker("random_number", digits=9, fix_len=True)  
    country = factory.Faker("country_code")
