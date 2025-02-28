from django.test import TestCase, Client
from apps.modules.invoices.factory import InvoiceFactory

class InvoiceListViewTest(TestCase):
    def setUp(self):
        # Create 20 invoices using the factory
        self.invoices = InvoiceFactory.create_batch(20)
        self.client = Client()

    def test_invoice_list_pagination(self):
        # Request the first page with a limit of 5 items
        response = self.client.get("/invoices/", {"page": 1, "limit": 5})
        self.assertEqual(response.status_code, 200)

        # Verify the response JSON
        data = response.json()
        self.assertEqual(data["page"], 1)
        self.assertEqual(len(data["invoices"]), 5)
        self.assertEqual(data["total"], 20)

        # Verify that the first invoice matches what we expect
        first_invoice = data["invoices"][0]
        self.assertEqual(first_invoice["id"], self.invoices[0].id)
        self.assertEqual(first_invoice["supplier"], self.invoices[0].supplier_id)
        self.assertEqual(first_invoice["total_amount"], str(self.invoices[0].total_amount))
        self.assertEqual(first_invoice["due_date"], self.invoices[0].due_date.isoformat())
