# Invoice Management - Setup Guide

Technologies: **Python (Django)**, **Testing**, **PostgreSQL (Docker Compose)**.

## 📌 **1. Clone the Repository**

```bash
git clone https://github.com/victor90braz/app-invoice-management-system.git
```

## 📌 **2. Set Up Environment**

```bash
python -m venv venv
```

**For Linux & macOS:**

```bash
source venv/bin/activate
```

**For Windows using Terminal PowerShell:**

```powershell
venv\Scripts\activate
```

## 📌 **3. Install Dependencies and Verify Requirements**

```bash
pip install -r requirements.txt
pip list
python manage.py check
```

## 📌 **4. Start PostgreSQL with Docker Compose**

Ensure `docker-compose.yml` exists, then run:

```bash
docker-compose down 
docker-compose up -d
```

Verify:

```bash
docker ps
```

## 📌 **5. Set Up Environment Variables**

Before running the project, copy the `.env.example` file and create your own `.env` file:

```bash
cp .env.example .env
```

Then update `.env` with your database credentials:

```
DB_NAME=invoice_management_db
DB_USER=postgres
DB_PASSWORD=your_password_here
DB_HOST=localhost
DB_PORT=5432

DEBUG=True
```

## 📌 **6. Apply Migrations & Create Superuser**

```bash
python manage.py migrate
python manage.py createsuperuser
```

## 📌 **7. Reset & Populate Database (Optional)**

```bash
python manage.py shell
```

Inside the shell:

```python
from apps.modules.suppliers.models import Supplier
from apps.modules.invoices.models import Invoice
from apps.modules.bank_reconciliation.models import BankTransaction
from apps.modules.withholdings.models import Withholding
from apps.modules.suppliers.factory import SupplierFactory
from apps.modules.invoices.factory import InvoiceFactory
from apps.modules.bank_reconciliation.factory import BankTransactionFactory
from apps.modules.withholdings.factory import WithholdingFactory

Supplier.objects.all().delete()
Invoice.objects.all().delete()
BankTransaction.objects.all().delete()
Withholding.objects.all().delete()

SupplierFactory.create_batch(50)
InvoiceFactory.create_batch(50)
BankTransactionFactory.create_batch(50)
WithholdingFactory.create_batch(50)

print("\u2705 Database reset and populated")
exit()
```

## 📌 **8. Run the Server**

```bash
python manage.py runserver
```

### **Endpoints:**

- **Suppliers:** `http://127.0.0.1:8000/suppliers/`
- **Invoices:** `http://127.0.0.1:8000/invoices/`
- **Bank Transactions:** `http://127.0.0.1:8000/transactions/`
- **Withholdings:** `http://127.0.0.1:8000/withholdings/`

## 📌 **9. Run Tests and Check Coverage**

Run all tests:

```bash
python manage.py test
```

Check code coverage:

```bash
coverage run --source='apps' manage.py test
coverage report -m
coverage html
```