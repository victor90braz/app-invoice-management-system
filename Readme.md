# Invoice Management - Setup Steps

Este documento describe los pasos para construir la aplicación en Django siguiendo la arquitectura vertical y los requerimientos de la prueba técnica.

## 📌 **1. Configuración Inicial**

### 🛠️ **Paso 1: Instalar Django y Crear Proyecto**
```bash
pip install django
django-admin startproject invoice_management
```

### 🛠️ **Paso 2: Crear la Estructura de Carpetas**
```bash
mkdir -p invoice_management/apps/modules
mkdir -p invoice_management/database/migrations
mkdir -p invoice_management/core
mkdir -p invoice_management/tests
mkdir -p invoice_management/requirements
```


## 📌 **2. Configurar el Proyecto Django**

### 🛠️ **Paso 3: Modificar `settings.py` para Soportar Múltiples Aplicaciones**
- Agregar `apps.modules.suppliers`, `apps.modules.invoices`, `apps.modules.bank_reconciliation`, `apps.modules.withholdings` en `INSTALLED_APPS`.


## 📌 **3. Crear los Módulos**

### 🛠️ **Paso 4: Crear Módulo de Proveedores (`suppliers`)**
```bash
mkdir -p invoice_management/apps/modules/suppliers/tests
cd invoice_management/apps/modules/suppliers

# Crear archivos
touch __init__.py models.py views.py urls.py services.py repositories.py
```

### 🛠️ **Paso 5: Crear Módulo de Facturas (`invoices`)**
```bash
mkdir -p invoice_management/apps/modules/invoices/tests
cd invoice_management/apps/modules/invoices

# Crear archivos
touch __init__.py models.py views.py urls.py services.py repositories.py
```

### 🛠️ **Paso 6: Crear Módulo de Conciliación Bancaria (`bank_reconciliation`)**
```bash
mkdir -p invoice_management/apps/modules/bank_reconciliation/tests
cd invoice_management/apps/modules/bank_reconciliation

# Crear archivos
touch __init__.py models.py views.py urls.py services.py repositories.py
```

### 🛠️ **Paso 7: Crear Módulo de Retenciones (`withholdings`)**
```bash
mkdir -p invoice_management/apps/modules/withholdings/tests
cd invoice_management/apps/modules/withholdings

# Crear archivos
touch __init__.py models.py views.py urls.py services.py repositories.py
```


## 📌 **4. Implementar Seguridad y Validaciones**

### 🛠️ **Paso 8: Configurar Seguridad en `core/`**
```bash
cd invoice_management/core

# Crear archivos
touch __init__.py authentication.py middleware.py permissions.py exceptions.py validators.py
```


## 📌 **5. Configurar la Base de Datos**

### 🛠️ **Paso 9: Agregar Módulo de Base de Datos**
```bash
cd invoice_management/database

# Crear archivos
touch __init__.py queries.py
```


## 📌 **6. Agregar Configuraciones Adicionales**

### 🛠️ **Paso 10: Configurar Entornos**
```bash
cd invoice_management/settings

# Crear configuraciones separadas
touch __init__.py base.py development.py production.py
```


## 📌 **7. Configurar Dependencias y Variables de Entorno**

### 🛠️ **Paso 11: Crear Archivos de Dependencias**
```bash
cd invoice_management/requirements

# Crear archivos
touch base.txt development.txt production.txt
```

### 🛠️ **Paso 12: Configurar Variables de Entorno**
```bash
touch .env
```


## 📌 **8. Preparar Docker y Automatización**

### 🛠️ **Paso 13: Crear Archivos Docker y Makefile**
```bash
touch docker-compose.yml Dockerfile Makefile
```


## 📌 **9. Crear Pruebas**

### 🛠️ **Paso 14: Agregar Archivos de Pruebas**
```bash
cd invoice_management/tests

# Crear archivos
touch __init__.py test_auth.py test_performance.py
```


## 🚀 **Siguientes Pasos**
- Implementar modelos en cada módulo.
- Definir las reglas de negocio en `services.py`.
- Implementar validaciones en `validators.py`.
- Configurar permisos y seguridad.
- Crear endpoints y probar la API.

Este esquema cubre **el mínimo necesario** para la arquitectura vertical y es escalable para producción. ¡Sigue los pasos y avancemos juntos! 🚀
