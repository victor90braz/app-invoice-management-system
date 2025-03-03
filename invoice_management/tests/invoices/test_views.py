from django.test import TestCase, Client
from django.contrib.auth.models import User
from apps.modules.invoices.factory import InvoiceFactory
from apps.modules.suppliers.factory import SupplierFactory
from apps.modules.invoices.models import Invoice
import json


class InvoiceListViewTest(TestCase):

    def test_invoice_list_pagination(self):
        # ✅ Create a test user and authenticate
        user = User.objects.create_user(username="testuser", password="testpassword")
        client = Client()
        client.login(username="testuser", password="testpassword")

        # ✅ Create invoices using factory
        invoices = InvoiceFactory.create_batch(20)

        # ✅ Perform authenticated request
        response = client.get("/invoices/", {"page": 1, "limit": 5})
        self.assertEqual(response.status_code, 200)

        # ✅ Validate response JSON
        data = response.json()
        self.assertEqual(data["page"], 1)
        self.assertEqual(len(data["invoices"]), 5)
        self.assertEqual(data["total"], 20)

        # ✅ Validate the first invoice data
        first_invoice = data["invoices"][0]
        self.assertEqual(first_invoice["id"], invoices[0].id)
        self.assertEqual(first_invoice["supplier"]["id"], invoices[0].supplier.id)
        self.assertEqual(first_invoice["total_amount"], str(invoices[0].total_amount))
        self.assertEqual(first_invoice["due_date"], invoices[0].due_date.isoformat())


class CreateInvoiceViewTest(TestCase):

    def test_create_invoice_success(self):
        user = User.objects.create_user(username="testuser", password="testpassword")
        client = Client()
        client.login(username="testuser", password="testpassword")

        # ✅ Use factory to create a supplier
        supplier = SupplierFactory.create()

        # ✅ Invoice data with the supplier from factory
        invoice_data = {
            "supplier": supplier.id,
            "due_date": "2025-03-10",
            "items": ["Item1", "Item2"]
        }

        response = client.post("/invoices/create/", json.dumps(invoice_data), content_type="application/json")
        self.assertEqual(response.status_code, 201)

        data = response.json()
        self.assertIn("invoice_id", data)

        # ✅ Ensure invoice was created
        self.assertTrue(Invoice.objects.filter(id=data["invoice_id"]).exists())

    def test_create_invoice_missing_supplier(self):
        user = User.objects.create_user(username="testuser", password="testpassword")
        client = Client()
        client.login(username="testuser", password="testpassword")

        invoice_data = {
            "due_date": "2025-03-10",
            "items": ["Item1", "Item2"]
        }

        response = client.post("/invoices/create/", json.dumps(invoice_data), content_type="application/json")
        self.assertEqual(response.status_code, 400)
        self.assertEqual(response.json()["error"], "Supplier is required")  # ✅ Fixed error message

    def test_create_invoice_missing_due_date(self):
        user = User.objects.create_user(username="testuser", password="testpassword")
        client = Client()
        client.login(username="testuser", password="testpassword")

        # ✅ Use factory for supplier
        supplier = SupplierFactory.create()

        invoice_data = {
            "supplier": supplier.id,
            "items": ["Item1", "Item2"]
        }

        response = client.post("/invoices/create/", json.dumps(invoice_data), content_type="application/json")
        self.assertEqual(response.status_code, 400)
        self.assertEqual(response.json()["error"], "due_date is required")

    def test_create_invoice_empty_items(self):
        user = User.objects.create_user(username="testuser", password="testpassword")
        client = Client()
        client.login(username="testuser", password="testpassword")

        supplier = SupplierFactory.create()

        invoice_data = {
            "supplier": supplier.id,
            "due_date": "2025-03-10",
            "items": []
        }

        response = client.post("/invoices/create/", json.dumps(invoice_data), content_type="application/json")
        self.assertEqual(response.status_code, 400)
        self.assertEqual(response.json()["error"], "Items must be a non-empty array")
