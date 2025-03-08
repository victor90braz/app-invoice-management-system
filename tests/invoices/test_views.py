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
        self.user = User.objects.create_user(username="testuser", password="testpassword")
        self.client = APIClient()
        self.client.force_authenticate(user=self.user)
        self.invoices = InvoiceFactory.create_batch(20)

    def test_invoice_list_pagination(self):
        query_params = {"page": 1, "limit": 5}
        response = self.client.get("/invoices/", query_params)
        self.assertEqual(response.status_code, 200)
        data = response.json()
        self.assertEqual(data["count"], 20)
        self.assertEqual(len(data["results"]), 5)

    def test_create_invoice_success(self):
        supplier = SupplierFactory.create()
        invoice_data = {
            "supplier": supplier.id,
            "due_date": (datetime.today() + timedelta(days=10)).strftime("%Y-%m-%d"),
            "total_amount": "100.50",
        }
        response = self.client.post(
            "/invoices/create/", json.dumps(invoice_data), content_type="application/json"
        )
        self.assertEqual(response.status_code, 201)
        data = response.json()
        self.assertIn("invoice", data)
        self.assertTrue(Invoice.objects.filter(id=data["invoice"]["id"]).exists())

    def test_create_invoice_negative_total_amount(self):
        supplier = SupplierFactory.create()
        invoice_data = {
            "supplier": supplier.id,
            "due_date": (datetime.today() + timedelta(days=10)).strftime("%Y-%m-%d"),
            "total_amount": "-10.00",
        }
        response = self.client.post(
            "/invoices/create/", json.dumps(invoice_data), content_type="application/json"
        )
        self.assertEqual(response.status_code, 400)
        response_data = response.json()
        self.assertIn("total_amount", response_data)
        self.assertEqual(response_data["total_amount"][0], "Total amount cannot be negative.")

    def test_create_invoice_due_date_in_past(self):
        supplier = SupplierFactory.create()
        past_date = (datetime.today() - timedelta(days=1)).strftime("%Y-%m-%d")
        invoice_data = {
            "supplier": supplier.id,
            "due_date": past_date,
            "total_amount": "50.00",
        }
        response = self.client.post(
            "/invoices/create/", json.dumps(invoice_data), content_type="application/json"
        )
        self.assertEqual(response.status_code, 400)
        response_data = response.json()
        self.assertIn("due_date", response_data)
        self.assertEqual(response_data["due_date"][0], "Due date cannot be in the past.")

    def test_create_invoice_missing_supplier(self):
        invoice_data = {
            "due_date": "2025-03-10",
            "total_amount": "50.00",
        }
        response = self.client.post(
            "/invoices/create/", json.dumps(invoice_data), content_type="application/json"
        )
        self.assertEqual(response.status_code, 400)
        response_data = response.json()
        self.assertIn("supplier", response_data)
        self.assertEqual(response_data["supplier"][0], "This field is required.")

    def test_create_invoice_missing_due_date(self):
        supplier = SupplierFactory.create()
        invoice_data = {
            "supplier": supplier.id,
            "total_amount": "50.00",
        }
        response = self.client.post(
            "/invoices/create/", json.dumps(invoice_data), content_type="application/json"
        )
        self.assertEqual(response.status_code, 400)
        response_data = response.json()
        self.assertIn("due_date", response_data)
        self.assertEqual(response_data["due_date"][0], "This field is required.")
