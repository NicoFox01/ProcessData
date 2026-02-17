import asyncio
import pytest
from httpx import AsyncClient, ASGITransport
from sqlalchemy.ext.asyncio import create_async_engine, AsyncSession, async_sessionmaker
from sqlalchemy.orm import sessionmaker # and keep other orm imports if needed, but async_sessionmaker is in ext.asyncio
from uuid import uuid4

from app.main import app
from app.core.config import settings
from app.models.base import Base
from app.core.database import get_db
from app.models.user import User
from app.models.empresa import Empresa
from app.models.cliente import Cliente
from app.models.template import Template
from app.models.enums import UserRole
from app.core.security import get_password_hash, create_access_token
from app.models.job import Job
from app.models.enums import Vertical, TipoProceso, EstadoJob

# Configurar pytest-asyncio
pytest_plugins = ('pytest_asyncio',)

# ============================================
# 1. Motor y Sesión de Base de Datos de Testing
# ============================================

TEST_DATABASE_URL = "sqlite+aiosqlite:///:memory:"

engine = create_async_engine(
    TEST_DATABASE_URL,
    connect_args={"check_same_thread": False},
    echo=False  # Cambiar a True si quieres ver las queries SQL
)

AsyncTestingSessionLocal = async_sessionmaker(
    engine,
    class_=AsyncSession,
    expire_on_commit=False,
    autocommit=False,
    autoflush=False
)

# ============================================
# 2. Fixture: Sesión de Base de Datos
# ============================================

@pytest.fixture(scope="function")
async def db_session():
    """
    Crea una sesión de BD limpia para cada test.
    Crea las tablas antes y las elimina después.
    """
    # Crear todas las tablas
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)
    
    # Proveer la sesión al test
    async with AsyncTestingSessionLocal() as session:
        yield session
        await session.rollback()
    
    # Eliminar todas las tablas después del test
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.drop_all)

# ============================================
# 3. Fixture: Cliente HTTP de Testing
# ============================================

@pytest.fixture(scope="function")
async def client(db_session):
    """
    Cliente HTTP async para hacer requests a la app.
    Sobrescribe la dependencia get_db para usar db_session de testing.
    """
    # Override de la dependencia de DB
    async def override_get_db():
        yield db_session
    
    app.dependency_overrides[get_db] = override_get_db
    
    # Crear cliente HTTP
    async with AsyncClient(
        transport=ASGITransport(app=app),
        base_url="http://test"
    ) as ac:
        yield ac
    
    # Limpiar overrides
    app.dependency_overrides.clear()

# ============================================
# 4. Fixtures: Usuarios de Testing
# ============================================

@pytest.fixture(scope="function")
async def admin_user(db_session):
    """
    Usuario con rol ADMIN activo.
    """
    user = User(
        id=uuid4(),
        email="admin@test.com",
        full_name="Admin Test",
        hashed_password=get_password_hash("admin123"),
        is_active=True,
        role=UserRole.ADMIN
    )
    db_session.add(user)
    await db_session.commit()
    await db_session.refresh(user)
    return user

@pytest.fixture(scope="function")
async def selector_user(db_session):
    """
    Usuario con rol SELECTOR activo.
    """
    user = User(
        id=uuid4(),
        email="selector@test.com",
        full_name="Selector Test",
        hashed_password=get_password_hash("selector123"),
        is_active=True,
        role=UserRole.SELECTOR
    )
    db_session.add(user)
    await db_session.commit()
    await db_session.refresh(user)
    return user

@pytest.fixture(scope="function")
async def inactive_user(db_session):
    """
    Usuario inactivo (is_active=False) para testear rechazo de login.
    """
    user = User(
        id=uuid4(),
        email="inactive@test.com",
        full_name="Inactive Test",
        hashed_password=get_password_hash("inactive123"),
        is_active=False,
        role=UserRole.SELECTOR
    )
    db_session.add(user)
    await db_session.commit()
    await db_session.refresh(user)
    return user

@pytest.fixture(scope="function")
async def head_user(db_session):
    """
    Usuario con rol HEAD activo.
    Para testear que HEAD no puede acceder a rutas de gestión comercial.
    """
    user = User(
        id=uuid4(),
        email="head@test.com",
        full_name="Head Test",
        hashed_password=get_password_hash("head123"),
        is_active=True,
        role=UserRole.HEAD
    )
    db_session.add(user)
    await db_session.commit()
    await db_session.refresh(user)
    return user

# ============================================
# 5. Fixtures: Tokens JWT para Autenticación
# ============================================

@pytest.fixture(scope="function")
def admin_token(admin_user):
    """
    Token JWT válido para admin_user.
    Retorna headers listos para usar en requests.
    """
    access_token = create_access_token(
        data={"sub": admin_user.email, "role": admin_user.role.value}
    )
    return {"Authorization": f"Bearer {access_token}"}

@pytest.fixture(scope="function")
def selector_token(selector_user):
    """
    Token JWT válido para selector_user.
    Retorna headers listos para usar en requests.
    """
    access_token = create_access_token(
        data={"sub": selector_user.email, "role": selector_user.role.value}
    )
    return {"Authorization": f"Bearer {access_token}"}

@pytest.fixture(scope="function")
def head_token(head_user):
    """
    Token JWT válido para head_user.
    Retorna headers listos para usar en requests.
    Para testear que HEAD no tiene acceso a gestión comercial.
    """
    access_token = create_access_token(
        data={"sub": head_user.email, "role": head_user.role.value}
    )
    return {"Authorization": f"Bearer {access_token}"}

# ============================================
# 6. Fixtures: Datos Comerciales (Empresa/Cliente)
# ============================================

@pytest.fixture(scope="function")
async def sample_company(db_session):
    """
    Empresa de ejemplo para tests.
    """
    company = Empresa(
        id=uuid4(),
        company_name="Test Company S.A."
    )
    db_session.add(company)
    await db_session.commit()
    await db_session.refresh(company)
    return company

@pytest.fixture(scope="function")
async def sample_client(db_session, sample_company):
    """
    Cliente de ejemplo vinculado a sample_company.
    """
    client = Cliente(
        id=uuid4(),
        client_name="Test Client Corp",
        empresa_id=sample_company.id
    )
    db_session.add(client)
    await db_session.commit()
    await db_session.refresh(client)
    return client

@pytest.fixture(scope="function")
async def sample_job(db_session, sample_company, sample_client):

    job = Job(
        id=uuid4(),
        job_name=f"Test Job {uuid4()}",
        empresa_id=sample_company.id,
        cliente_id=sample_client.id,
        vacancies=1,
        vertical=Vertical.DEV,
        type_of_process=TipoProceso.STAFFED_LARGO,
        state=EstadoJob.ABIERTA
    )
    db_session.add(job)
    await db_session.commit()
    await db_session.refresh(job)
    return job

@pytest.fixture(scope="function")
async def sample_job_template(db_session, sample_job):
    template = Template(
        id=uuid4(),
        job_id=sample_job.id,
        name="Job Template",
        description="Job Description",
        vertical=sample_job.vertical, 
        type_of_process=sample_job.type_of_process 
    )
    db_session.add(template)
    await db_session.commit()
    await db_session.refresh(template)
    return template
