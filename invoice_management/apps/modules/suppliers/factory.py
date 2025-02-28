import factory
from apps.modules.suppliers.models import Supplier

class SupplierFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = Supplier

    name = factory.Faker("company")
    tax_id = factory.Sequence(lambda n: f"tax_id_{n}")
    country = factory.Faker("country_code")
