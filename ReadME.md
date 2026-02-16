# ProcessData - Backend (PD-BE)

Backend Serverless construido con **FastAPI** (Python) y **Supabase** (PostgreSQL).

## 🚀 Requisitos Previos

- Python 3.11+
- Cuenta en Supabase
- Cuenta en Vercel (opcional, para despliegue)

## 🛠️ Instalación y Configuración

### 1. Preparar Entorno

```bash
# Crear entorno virtual
python -m venv venv

# Activar entorno (Windows PowerShell)
.\venv\Scripts\Activate.ps1

# Instalar dependencias
pip install -r requirements.txt
```

### 2. Variables de Entorno

Copia el archivo de ejemplo y complétalo con tus credenciales de Supabase:

```powershell
Copy-Item .env.example .env
```

Asegúrate de definir `DATABASE_URL` (formato `postgresql+psycopg2://...` o `postgresql+asyncpg://...`) y las keys de Supabase.

## ▶️ Ejecución

Para desarrollo local con recarga automática (hot-reload):

```bash
uvicorn app.main:app --reload
```

La API estará disponible en: [http://127.0.0.1:8000](http://127.0.0.1:8000)
Documentación interactiva: [http://127.0.0.1:8000/docs](http://127.0.0.1:8000/docs)

## 🗄️ Migraciones (Alembic)

### Inicialización (Solo la primera vez)
Si el proyecto no tiene la carpeta `alembic` inicializada:
```bash
alembic init alembic
```
*Nota: Luego debes configurar `alembic.ini` y `alembic/env.py` para usar tu `DATABASE_URL`.*

### Gestión de Migraciones
Generar una nueva migración (detecta cambios en modelos):
```bash
alembic revision --autogenerate -m "descripcion_del_cambio"
```

Aplicar migraciones a la base de datos (Supabase):
```bash
alembic upgrade head
```

🔄 Versionado (Workflow)
1. Nueva Rama
git checkout develop -> git pull origin develop -> git checkout -b GES-XX

2. Ciclo de Desarrollo
git status -> git add . -> git commit -m "GES-XX: descripción corta del cambio"

3. Subida a GitHub
git push origin GES-XX

4. Integración (En la web de GitHub)
Entrar al repo y hacer clic en "Compare & pull request" asegurando como destino base: develop. Merge pull request & Delete branch.

5. Limpieza y Sincronización Local
git checkout develop -> git pull origin develop -> git branch -d GES-XX -> git fetch --prune

## 🧪 Testing

Para ejecutar las pruebas (asegúrate de tener `pytest` instalado):

```bash
pytest
```

para ejecutar todas las pruebas, hay que ejecutar:
    pytest tests/ -v

para ejecutar las pruebas de un archivo test en particular:
    pytest tests/test_auth.py -v
    pytest tests/test_commercial.py -v
    pytest tests/test_security.py -v

para ejecutar una prueba en particular:
    pytest tests/test_auth.py::test_login_success -v

## 📂 Estructura

```text
PD-BE/
├── app/
│   ├── main.py        # Punto de entrada (FastAPI + Mangum)
│   ├── api/           # Endpoints de la API
│   ├── core/          # Configuración y conexión a DB
│   ├── models/        # Modelos SQLAlchemy
│   └── schemas/       # Esquemas Pydantic
├── tests/             # Tests unitarios y de integración
├── .env.example       # Plantilla de variables de entorno
└── requirements.txt   # Dependencias del proyecto
```
