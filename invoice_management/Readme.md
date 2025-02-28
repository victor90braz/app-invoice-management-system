Here’s the entire updated README with all the clarified steps:

```markdown
# Invoice Management - Setup Guide

This guide provides a quick setup for running the **Invoice Management System** using **Django**, **PostgreSQL (Docker)**, and **GitHub**.

## 📌 **1. Clone the Repository**
```bash
git clone https://github.com/victor90braz/app-invoice-management-system.git
cd app-invoice-management-system
```

## 📌 **2. Create a Virtual Environment & Install Dependencies**
```bash
python -m venv venv
source venv/bin/activate  # On Windows use: venv\Scripts\activate
pip install -r requirements.txt
```

## 📌 **3. Set Up PostgreSQL with Docker**
```bash
docker run --name postgres-db -e POSTGRES_USER=postgres -e POSTGRES_PASSWORD=root -e POSTGRES_DB=invoice_management_db -p 5432:5432 -d postgres
```

Verify the container is running:
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

## 📌 **6. Create Initial Data (Optional)**
If you’d like to populate the database with example suppliers and invoices before running the server, you can do the following:

```bash
python manage.py shell
```

Inside the shell, run:
```python
from apps.modules.suppliers.models import Supplier

# Create 50 suppliers
for index in range(1, 51):
    Supplier.objects.create(
        name=f"Supplier {index}",
        tax_id=f"123456789{index}",
        country="US"
    )

from apps.modules.invoices.factory import InvoiceFactory

# Create 50 invoices
InvoiceFactory.create_batch(50)
```

Exit the shell after you’ve created the data.

## 📌 **7. Run the Server**
```bash
python manage.py runserver
```

Now visit 
**`http://127.0.0.1:8000/suppliers/`** 
**`http://127.0.0.1:8000/invoices/`** 
```