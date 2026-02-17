import pytest
from uuid import uuid4
from app.models.enums import Vertical, TipoProceso, EstadoJob
from app.models.job import Job

BASE_URL = "/api/v1/jobs"

@pytest.mark.asyncio
async def test_create_job_happy_path_admin(client, sample_company, sample_client, admin_token):
    payload = {
        "job_name": "Sr Python Dev",
        "empresa_id": str(sample_company.id),
        "cliente_id": str(sample_client.id),
        "vacancies": 3,
        "vertical": Vertical.DEV.value,
        "tipo_proceso": TipoProceso.STAFFED_LARGO.value,
    }
    response = await client.post(BASE_URL, json=payload, headers=admin_token)
    assert response.status_code == 201
    data = response.json()
    job = await sample_company.get_job_by_id(data["id"])
    assert job is not None

@pytest.mark.asyncio
async def test_create_job_happy_path_selector(client, sample_company, sample_client, selector_token):
    payload = {
        "job_name": "Ssr React Dev",
        "empresa_id": str(sample_company.id),
        "cliente_id": str(sample_client.id),
        "vacancies": 1,
        "vertical": Vertical.DEV.value,
        "tipo_proceso": TipoProceso.STAFFED_CORTO.value,
    }
    response = await client.post(BASE_URL, json=payload, headers=selector_token)
    assert response.status_code == 201
    data = response.json()
    job = await sample_company.get_job_by_id(data["id"])
    assert job is not None

@pytest.mark.asyncio
async def test_create_job_unauthorized_head(client, sample_company, sample_client, head_token):
    payload = {
        "job_name": "Sr Python Dev",
        "empresa_id": str(sample_company.id),
        "cliente_id": str(sample_client.id),
        "vacancies": 3,
        "vertical": Vertical.DEV.value,
        "tipo_proceso": TipoProceso.STAFFED_LARGO.value,
    }
    response = await client.post(BASE_URL, json=payload, headers=head_token)
    assert response.status_code == 403

@pytest.mark.asyncio
async def test_create_job_wrong_data_validation_admin(client, sample_company, sample_client, admin_token):
    payload = {
        "job_name": "", # Inválido: nombre vacío
        "empresa_id": str(sample_company.id),
        "cliente_id": str(sample_client.id),
        "vacancies": 1,
        "vertical": Vertical.DEV.value,
        "tipo_proceso": TipoProceso.RENAISS_SIN_CLIENTE.value,
    }
    response = await client.post(BASE_URL, json=payload, headers=admin_token)
    assert response.status_code == 422

@pytest.mark.asyncio
async def test_create_job_wrong_data_validation_selector(client, sample_company, sample_client, selector_token):
    payload = {
        "job_name": "Sr Fullstack",
        "empresa_id": str(sample_company.id),
        "cliente_id": str(sample_client.id),
        "vacancies": -1, # Inválido: vacantes negativas
        "vertical": Vertical.DEV.value,
        "tipo_proceso": TipoProceso.RENAISS_CON_CLIENTE.value,
    }
    response = await client.post(BASE_URL, json=payload, headers=selector_token)
    assert response.status_code == 422

@pytest.mark.asyncio
async def test_get_job_by_id_admin(client, sample_job, admin_token):
    response = await client.get(f"{BASE_URL}/{sample_job.id}", headers=admin_token)
    assert response.status_code == 200
    assert response.json()["id"] == str(sample_job.id)

@pytest.mark.asyncio
async def test_get_job_by_id_selector(client, sample_job, selector_token):
    response = await client.get(f"{BASE_URL}/{sample_job.id}", headers=selector_token)
    assert response.status_code == 200
    assert response.json()["id"] == str(sample_job.id)

@pytest.mark.asyncio
async def test_get_job_by_id_head(client, sample_job, head_token):
    response = await client.get(f"{BASE_URL}/{sample_job.id}", headers=head_token)
    assert response.status_code == 200

@pytest.mark.asyncio
async def test_list_jobs_admin(client, sample_company, sample_client, admin_token, db_session):
    job1 = Job(id=uuid4(), job_name="J1", empresa_id=sample_company.id, cliente_id=sample_client.id, vacancies=1, vertical=Vertical.DEV, tipo_proceso=TipoProceso.STAFFED_LARGO, state=EstadoJob.ABIERTA)
    job2 = Job(id=uuid4(), job_name="J2", empresa_id=sample_company.id, cliente_id=sample_client.id, vacancies=1, vertical=Vertical.DEV, tipo_proceso=TipoProceso.STAFFED_LARGO, state=EstadoJob.CERRADA)
    db_session.add_all([job1, job2])
    await db_session.commit()
    
    response = await client.get(BASE_URL, headers=admin_token)
    assert response.status_code == 200
    assert len(response.json()) >= 2

@pytest.mark.asyncio
async def test_list_jobs_selector(client, sample_company, sample_client, selector_token, db_session):
    job1 = Job(id=uuid4(), job_name="JS1", empresa_id=sample_company.id, cliente_id=sample_client.id, vacancies=1, vertical=Vertical.DEV, tipo_proceso=TipoProceso.STAFFED_LARGO, state=EstadoJob.ABIERTA)
    db_session.add(job1)
    await db_session.commit()
    
    response = await client.get(BASE_URL, headers=selector_token)
    assert response.status_code == 200

@pytest.mark.asyncio
async def test_list_jobs_head(client, sample_company, sample_client, head_token, db_session):
    job1 = Job(id=uuid4(), job_name="JH1", empresa_id=sample_company.id, cliente_id=sample_client.id, vacancies=1, vertical=Vertical.DEV, tipo_proceso=TipoProceso.STAFFED_LARGO, state=EstadoJob.PAUSADA)
    db_session.add(job1)
    await db_session.commit()
    
    response = await client.get(f"{BASE_URL}?state=PAUSADA", headers=head_token)
    assert response.status_code == 200

@pytest.mark.asyncio
async def test_update_job_status_admin(client, sample_job, admin_token):
    status = {"state": EstadoJob.CERRADA.value}
    response = await client.patch(f"{BASE_URL}/{sample_job.id}/status", json=status, headers=admin_token)
    assert response.status_code == 200
    assert response.json()["state"] == EstadoJob.CERRADA.value

@pytest.mark.asyncio
async def test_update_job_status_selector(client, sample_job, selector_token):
    status = {"state": EstadoJob.PAUSADA.value}
    response = await client.patch(f"{BASE_URL}/{sample_job.id}/status", json=status, headers=selector_token)
    assert response.status_code == 200

@pytest.mark.asyncio
async def test_update_job_status_head(client, sample_job, head_token):
    status = {"state": EstadoJob.CERRADA.value}
    response = await client.patch(f"{BASE_URL}/{sample_job.id}/status", json=status, headers=head_token)
    assert response.status_code == 403

@pytest.mark.asyncio
async def test_soft_delete_job_admin(client, sample_job, admin_token):
    response = await client.patch(f"{BASE_URL}/{sample_job.id}/soft-delete", headers=admin_token)
    assert response.status_code == 200
    assert response.json()["state"] == EstadoJob.CANCELADA.value

@pytest.mark.asyncio
async def test_soft_delete_job_selector(client, sample_job, selector_token):
    response = await client.patch(f"{BASE_URL}/{sample_job.id}/soft-delete", headers=selector_token)
    assert response.status_code == 403

@pytest.mark.asyncio
async def test_soft_delete_job_head(client, sample_job, head_token):
    response = await client.patch(f"{BASE_URL}/{sample_job.id}/soft-delete", headers=head_token)
    assert response.status_code == 403

@pytest.mark.asyncio
async def test_create_job_from_template_admin(client, sample_job_template, sample_company, sample_client, admin_token):
    #Arrange
    payload = {
        "template_id": str(sample_job_template.id),
        "job_name": "Job from template",
        "empresa_id": str(sample_company.id),
        "cliente_id": str(sample_client.id),
        "vacancies": 1
    }
    #Act
    response = await client.post(f"{BASE_URL}/from-template", json=payload, headers=admin_token)
    #Assert
    assert response.status_code == 201
    data = response.json()
    assert data["job_name"] == "Job from template"
    assert data["empresa_id"] == str(sample_company.id)
    assert data["cliente_id"] == str(sample_client.id)
    assert data["vacancies"] == 1
    assert data["vertical"] == sample_job_template.vertical.value
    assert data["type_of_process"] == sample_job_template.type_of_process.value

@pytest.mark.asyncio
async def test_create_job_from_template_selector(client, sample_job_template, sample_company, sample_client, selector_token):
    #Arrange
    payload = {
        "template_id": str(sample_job_template.id),
        "job_name": "Job from template",
        "empresa_id": str(sample_company.id),
        "cliente_id": str(sample_client.id),
        "vacancies": 1
    }
    #Act
    response = await client.post(f"{BASE_URL}/from-template", json=payload, headers=selector_token)
    #Assert
    assert response.status_code == 201
    data = response.json()
    assert data["job_name"] == "Job from template"
    assert data["empresa_id"] == str(sample_company.id)
    assert data["cliente_id"] == str(sample_client.id)
    assert data["vacancies"] == 1
    assert data["vertical"] == sample_job_template.vertical.value
    assert data["type_of_process"] == sample_job_template.type_of_process.value

@pytest.mark.asyncio
async def test_create_job_from_template_head(client, sample_job_template, sample_company, sample_client, head_token):
    #Arrange
    payload = {
        "template_id": str(sample_job_template.id),
        "job_name": "Job from template",
        "empresa_id": str(sample_company.id),
        "cliente_id": str(sample_client.id),
        "vacancies": 1
    }
    #Act
    response = await client.post(f"{BASE_URL}/from-template", json=payload, headers=head_token)
    #Assert
    assert response.status_code == 403