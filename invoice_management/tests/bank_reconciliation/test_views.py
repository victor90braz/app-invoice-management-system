from django.test import TestCase, Client

from apps.modules.bank_reconciliation.factory import BankTransactionFactory

class BankTransactionListViewTest(TestCase):
    def setUp(self):
        self.transactions = BankTransactionFactory.create_batch(20)
        self.client = Client()

    def test_bank_transaction_list_pagination(self):
        response = self.client.get("/bank-reconciliation/", {"page": 1, "limit": 5})
        self.assertEqual(response.status_code, 200)

        data = response.json()
        self.assertEqual(data["page"], 1)
        self.assertEqual(len(data["transactions"]), 5)
        self.assertEqual(data["total"], 20)

        first_txn = data["transactions"][0]
        self.assertEqual(first_txn["id"], self.transactions[0].id)
        self.assertEqual(first_txn["invoice"], self.transactions[0].invoice_id)
        self.assertEqual(first_txn["transaction_id"], self.transactions[0].transaction_id)
        self.assertEqual(first_txn["amount"], str(self.transactions[0].amount))
        self.assertEqual(first_txn["transaction_date"], self.transactions[0].transaction_date.isoformat())
