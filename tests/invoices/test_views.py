from django.test import TestCase
from rest_framework.test import APIClient
from django.contrib.auth.models import User
from apps.modules.invoices.factory import InvoiceFactory
from apps.modules.suppliers.factory import SupplierFactory
from apps.modules.invoices.models import Invoice
import json
from datetime import datetime, timedelta


class InvoiceViewTest(TestCase):
    def setUp(self):
        # Arrange: Common setup for all tests
        self.user = User.objects.create_user(username="testuser", password="testpassword")
        self.client = APIClient()
        self.client.force_authenticate(user=self.user)
        self.invoices = InvoiceFactory.create_batch(20)

    def test_invoice_list_pagination(self):
        # Arrange: Set up query parameters for pagination
        query_params = {"page": 1, "limit": 5}

        # Act: Make a GET request to the invoice list endpoint
        response = self.client.get("/invoices/", query_params)

        # Assert: Verify the response status code and paginated data
        self.assertEqual(response.status_code, 200)
        data = response.json()
        self.assertEqual(data["count"], 20)
        self.assertEqual(len(data["results"]), 5)

    def test_create_invoice_success(self):
        # Arrange: Create a supplier and valid invoice data
        supplier = SupplierFactory.create()
        invoice_data = {
            "supplier": supplier.id,
            "due_date": (datetime.today() + timedelta(days=10)).strftime("%Y-%m-%d"),
            "total_amount": "100.50",
        }

        # Act: Make a POST request to create an invoice
        response = self.client.post(
            "/invoices/create/", json.dumps(invoice_data), content_type="application/json"
        )

        # Assert: Verify the response status code and that the invoice was created
        self.assertEqual(response.status_code, 201)
        data = response.json()
        self.assertIn("invoice", data)
        self.assertTrue(Invoice.objects.filter(id=data["invoice"]["id"]).exists())

    def test_create_invoice_negative_total_amount(self):
        # Arrange: Create a supplier and invoice data with a negative total amount
        supplier = SupplierFactory.create()
        invoice_data = {
            "supplier": supplier.id,
            "due_date": (datetime.today() + timedelta(days=10)).strftime("%Y-%m-%d"),
            "total_amount": "-10.00",
        }

        # Act: Make a POST request to create an invoice
        response = self.client.post(
            "/invoices/create/", json.dumps(invoice_data), content_type="application/json"
        )

        # Assert: Verify the response status code and error message
        self.assertEqual(response.status_code, 400)
        self.assertIn("total_amount", response.json()["errors"])
        self.assertEqual(
            response.json()["errors"]["total_amount"][0], "Total amount cannot be negative."
        )

    def test_create_invoice_due_date_in_past(self):
        # Arrange: Create a supplier and invoice data with a past due date
        supplier = SupplierFactory.create()
        past_date = (datetime.today() - timedelta(days=1)).strftime("%Y-%m-%d")
        invoice_data = {
            "supplier": supplier.id,
            "due_date": past_date,
            "total_amount": "50.00",
        }

        # Act: Make a POST request to create an invoice
        response = self.client.post(
            "/invoices/create/", json.dumps(invoice_data), content_type="application/json"
        )

        # Assert: Verify the response status code and error message
        self.assertEqual(response.status_code, 400)
        self.assertIn("due_date", response.json()["errors"])
        self.assertEqual(
            response.json()["errors"]["due_date"][0], "Due date cannot be in the past."
        )

    def test_create_invoice_missing_supplier(self):
        # Arrange: Create invoice data without a supplier
        invoice_data = {
            "due_date": "2025-03-10",
            "total_amount": "50.00",
        }

        # Act: Make a POST request to create an invoice
        response = self.client.post(
            "/invoices/create/", json.dumps(invoice_data), content_type="application/json"
        )

        # Assert: Verify the response status code and error message
        self.assertEqual(response.status_code, 400)
        self.assertIn("supplier", response.json()["errors"])
        self.assertEqual(response.json()["errors"]["supplier"][0], "This field is required.")

    def test_create_invoice_missing_due_date(self):
        # Arrange: Create a supplier and invoice data without a due date
        supplier = SupplierFactory.create()
        invoice_data = {
            "supplier": supplier.id,
            "total_amount": "50.00",
        }

        # Act: Make a POST request to create an invoice
        response = self.client.post(
            "/invoices/create/", json.dumps(invoice_data), content_type="application/json"
        )

        # Assert: Verify the response status code and error message
        self.assertEqual(response.status_code, 400)
        self.assertIn("due_date", response.json()["errors"])
        self.assertEqual(response.json()["errors"]["due_date"][0], "This field is required.")