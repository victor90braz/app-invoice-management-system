from django.test import TestCase, Client
from django.contrib.auth.models import User
from apps.modules.invoices.factory import InvoiceFactory
from apps.modules.suppliers.factory import SupplierFactory
from apps.modules.invoices.models import Invoice
import json


class InvoiceViewTest(TestCase):

    def setUp(self):
        # Arrange
        self.username = "testuser"
        self.password = "testpassword"
        self.user = User.objects.create_user(username=self.username, password=self.password)
        self.client = Client()
        self.client.login(username=self.username, password=self.password)
        self.invoices = InvoiceFactory.create_batch(20)

    def test_invoice_list_pagination(self):
        # Act
        response = self.client.get("/invoices/", {"page": 1, "limit": 5})
        # Assert
        self.assertEqual(response.status_code, 200)
        data = response.json()
        self.assertEqual(data["page"], 1)
        self.assertEqual(len(data["invoices"]), 5)
        self.assertEqual(data["total"], 20)
        first_invoice = data["invoices"][0]
        self.assertEqual(first_invoice["id"], self.invoices[0].id)
        self.assertEqual(first_invoice["supplier"]["id"], self.invoices[0].supplier.id)
        self.assertEqual(first_invoice["total_amount"], str(self.invoices[0].total_amount))
        self.assertEqual(first_invoice["due_date"], self.invoices[0].due_date.isoformat())

    def test_create_invoice_success(self):
        # Arrange
        supplier = SupplierFactory.create()
        invoice_data = {
            "supplier": supplier.id,
            "due_date": "2025-03-10",
            "items": ["Item1", "Item2"]
        }
        # Act
        response = self.client.post("/invoices/create/", json.dumps(invoice_data), content_type="application/json")
        # Assert
        self.assertEqual(response.status_code, 201)
        data = response.json()
        self.assertIn("invoice_id", data)
        self.assertTrue(Invoice.objects.filter(id=data["invoice_id"]).exists())

    def test_create_invoice_missing_supplier(self):
        # Arrange
        invoice_data = {
            "due_date": "2025-03-10",
            "items": ["Item1", "Item2"]
        }
        # Act
        response = self.client.post("/invoices/create/", json.dumps(invoice_data), content_type="application/json")
        # Assert
        self.assertEqual(response.status_code, 400)
        self.assertEqual(response.json()["error"], "Supplier is required")

    def test_create_invoice_missing_due_date(self):
        # Arrange
        supplier = SupplierFactory.create()
        invoice_data = {
            "supplier": supplier.id,
            "items": ["Item1", "Item2"]
        }
        # Act
        response = self.client.post("/invoices/create/", json.dumps(invoice_data), content_type="application/json")
        # Assert
        self.assertEqual(response.status_code, 400)
        self.assertEqual(response.json()["error"], "due_date is required")

    def test_create_invoice_empty_items(self):
        # Arrange
        supplier = SupplierFactory.create()
        invoice_data = {
            "supplier": supplier.id,
            "due_date": "2025-03-10",
            "items": []
        }
        # Act
        response = self.client.post("/invoices/create/", json.dumps(invoice_data), content_type="application/json")
        # Assert
        self.assertEqual(response.status_code, 400)
        self.assertEqual(response.json()["error"], "Items must be a non-empty array")
