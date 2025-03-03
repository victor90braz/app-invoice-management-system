import factory
from apps.modules.bank_reconciliation.models import BankTransaction
from apps.modules.invoices.factory import InvoiceFactory

class BankTransactionFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = BankTransaction

    invoice = factory.SubFactory(InvoiceFactory)
    transaction_id = factory.Sequence(lambda n: f"txn_{n}")
    amount = factory.Faker("pydecimal", left_digits=4, right_digits=2, positive=True)
    transaction_date = factory.Faker("date_object")
