from django.test import TestCase, Client
from apps.modules.withholdings.factory import WithholdingFactory

class WithholdingListViewTest(TestCase):
    def setUp(self):
        self.withholdings = WithholdingFactory.create_batch(20)
        self.client = Client()

    def test_withholding_list_pagination(self):
        response = self.client.get("/withholdings/", {"page": 1, "limit": 5})
        self.assertEqual(response.status_code, 200)

        data = response.json()
        self.assertEqual(data["page"], 1)
        self.assertEqual(len(data["withholdings"]), 5)
        self.assertEqual(data["total"], 20)

        first_withholding = data["withholdings"][0]
        self.assertEqual(first_withholding["id"], self.withholdings[0].id)
        self.assertEqual(first_withholding["invoice"], self.withholdings[0].invoice_id)
        self.assertEqual(first_withholding["amount"], str(self.withholdings[0].amount))
        self.assertEqual(first_withholding["withholding_type"], self.withholdings[0].withholding_type)
        self.assertEqual(first_withholding["date_applied"], self.withholdings[0].date_applied.isoformat())
