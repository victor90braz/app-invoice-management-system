from django.test import TestCase, Client
from apps.modules.suppliers.factory import SupplierFactory

class SupplierListViewTest(TestCase):
    def setUp(self):
        # Create 20 suppliers using the factory
        self.suppliers = SupplierFactory.create_batch(20)
        self.client = Client()

    def test_supplier_list_pagination(self):
        # Request the first page with a limit of 5 items
        response = self.client.get("/suppliers/", {"page": 1, "limit": 5})
        self.assertEqual(response.status_code, 200)

        # Verify the response JSON
        data = response.json()
        self.assertEqual(data["page"], 1)
        self.assertEqual(len(data["suppliers"]), 5)
        self.assertEqual(data["total"], 20)

        # Verify that the first supplier matches what we expect
        first_supplier = data["suppliers"][0]
        self.assertEqual(first_supplier["id"], self.suppliers[0].id)
        self.assertEqual(first_supplier["name"], self.suppliers[0].name)
        self.assertEqual(first_supplier["tax_id"], self.suppliers[0].tax_id)
        self.assertEqual(first_supplier["country"], self.suppliers[0].country)
