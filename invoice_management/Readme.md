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

## 📌 **6. Run the Server**
```bash
python manage.py runserver
```

Now visit **`http://127.0.0.1:8000/admin`** and log in with your superuser credentials.

🚀 Your project is now set up and running!
