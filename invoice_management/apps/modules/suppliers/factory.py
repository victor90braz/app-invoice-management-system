import factory
import random
import string
from apps.modules.suppliers.models import Supplier

def generate_valid_tax_id():
    return "".join(random.choices(string.ascii_uppercase + string.digits, k=10))

class SupplierFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = Supplier

    name = factory.Faker("company")
    tax_id = factory.LazyFunction(generate_valid_tax_id)  
    country = factory.Faker("country_code")
