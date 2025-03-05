# Invoice Management - Setup Guide

Tecnoligies: **Python (Django)**, **Testing**, **PostgreSQL (Docker Compose)**.

## 📌 **1. Clone the Repository**
```bash
git clone https://github.com/victor90braz/app-invoice-management-system.git
```

## 📌 **2. Create a Virtual Environment & Install Dependencies**
```bash
python -m venv venv
source venv/bin/activate  # On Windows use: venv\Scripts\activate
pip install -r requirements.txt
```

## 📌 **3. Set Up PostgreSQL with Docker Compose**
Ensure you have a `docker-compose.yml` file with the following content:

```yaml
version: '3.8'

services:
  db:
    image: postgres
    container_name: postgres-db
    restart: always
    environment:
      POSTGRES_USER: postgres
      POSTGRES_PASSWORD: root
      POSTGRES_DB: invoice_management_db
    ports:
      - "5432:5432"
    volumes:
      - postgres_data:/var/lib/postgresql/data

volumes:
  postgres_data:
```

Then, start PostgreSQL with:
```bash
docker-compose up -d
```

Verify that the container is running:
```bash
docker ps
```

## 📌 **4. Configure the Database in `settings.py`**
Edit `invoice_management/settings.py`:
```python
DATABASES = {
    "default": {
        "ENGINE": "django.db.backends.postgresql",
        "NAME": "invoice_management_db",
        "USER": "postgres",
        "PASSWORD": "root",
        "HOST": "localhost",  
        "PORT": "5432",
    }
}
```

## 📌 **5. Apply Migrations & Create a Superuser**
```bash
python manage.py makemigrations
python manage.py migrate
python manage.py createsuperuser
```

## 📌 **6. Clean & Populate the Database (Optional)**
If you’d like to reset and populate the database with example suppliers, invoices, transactions, and withholdings before running the server, follow these steps:

### **6.1 Clean the Database**
```bash
python manage.py shell
```
Inside the shell, run:
```python
from apps.modules.suppliers.models import Supplier
from apps.modules.invoices.models import Invoice
from apps.modules.bank_reconciliation.models import BankTransaction
from apps.modules.withholdings.models import Withholding

Supplier.objects.all().delete()
Invoice.objects.all().delete()
BankTransaction.objects.all().delete()
Withholding.objects.all().delete()

print("✅ Database cleaned")
```

### **6.2 Populate the Database**

```bash
python manage.py shell
```
Inside the shell, run:

```python
from apps.modules.suppliers.factory import SupplierFactory
from apps.modules.invoices.factory import InvoiceFactory
from apps.modules.bank_reconciliation.factory import BankTransactionFactory
from apps.modules.withholdings.factory import WithholdingFactory

SupplierFactory.create_batch(50)
InvoiceFactory.create_batch(50)
BankTransactionFactory.create_batch(50)
WithholdingFactory.create_batch(50)

print("✅ Data generated successfully")
exit()
```

## 📌 **7. Run the Server**
```bash
python manage.py runserver
```

Now visit the following endpoints:
- **Suppliers:** `http://127.0.0.1:8000/suppliers/`
- **Invoices:** `http://127.0.0.1:8000/invoices/`
- **Bank Transactions:** `http://127.0.0.1:8000/transactions/`
- **Withholdings:** `http://127.0.0.1:8000/withholdings/`

