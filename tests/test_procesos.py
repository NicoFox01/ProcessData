import pytest
from uuid import uuid4, UUID
from app.models.enums import EstadoGeneral
from app.models.proceso import Proceso

BASE_URL = "/api/v1/processes"

@pytest.mark.asyncio
async def test_create_process_admin (client, admin_token, sample_job, sample_candidate):
    payload = {
        "job_id": str(sample_job.id),
        "candidate_id": str(sample_candidate.id),
        "status": EstadoGeneral.SOURCING.value
    }
    response = await client.post(BASE_URL, json=payload, headers=admin_token)
    assert response.status_code == 201
    assert response.json()["job_id"] == str(sample_job.id)
    assert response.json()["candidate_id"] == str(sample_candidate.id)
    assert response.json()["status"] == EstadoGeneral.SOURCING.value
    data = response.json()
    assert "id" in data
    assert UUID(data["id"])

@pytest.mark.asyncio
async def test_create_process_selector (client, selector_token, sample_job, sample_candidate):
    payload = {
        "job_id": str(sample_job.id),
        "candidate_id": str(sample_candidate.id),
        "status": EstadoGeneral.SOURCING.value
    }
    response = await client.post(BASE_URL, json=payload, headers=selector_token)
    assert response.status_code == 201
    assert response.json()["job_id"] == str(sample_job.id)
    assert response.json()["candidate_id"] == str(sample_candidate.id)
    assert response.json()["status"] == EstadoGeneral.SOURCING.value
    data = response.json()
    assert "id" in data
    assert UUID(data["id"])

@pytest.mark.asyncio
async def test_create_process_head_unauthorized (client, head_token, sample_job, sample_candidate):
    payload = {
        "job_id": str(sample_job.id),
        "candidate_id": str(sample_candidate.id),
        "status": EstadoGeneral.SOURCING.value
    }
    response = await client.post(BASE_URL, json=payload, headers=head_token)
    assert response.status_code == 403

@pytest.mark.asyncio
async def test_list_processes_by_job_admin (client, admin_token, sample_job, sample_job_process):
    job_id = str(sample_job.id)
    response = await client.get(f"{BASE_URL}?job_id={job_id}", headers=admin_token)
    assert response.status_code == 200
    assert len(response.json()) > 0
    data = response.json()
    assert "id" in data[0]
    assert UUID(data[0]["id"]) == str(sample_job_process.id)

@pytest.mark.asyncio
async def test_list_processes_by_job_selector (client, selector_token, sample_job, sample_job_process):
    job_id = str(sample_job.id)
    response = await client.get(f"{BASE_URL}?job_id={job_id}", headers=selector_token)
    assert response.status_code == 200
    assert len(response.json()) > 0
    data = response.json()
    assert "id" in data[0]
    assert UUID(data[0]["id"]) == str(sample_job_process.id)

@pytest.mark.asyncio
async def test_list_processes_by_job_head (client, head_token, sample_job, sample_job_process):
    job_id = str(sample_job.id)
    response = await client.get(f"{BASE_URL}?job_id={job_id}", headers=head_token)
    assert response.status_code == 200
    assert len(response.json()) > 0
    data = response.json()
    assert "id" in data[0]
    assert UUID(data[0]["id"]) == str(sample_job_process.id)

@pytest.mark.asyncio
async def test_list_processes_admin (client, admin_token, sample_job_process):
    response = await client.get(BASE_URL, headers=admin_token)
    assert response.status_code == 200
    assert len(response.json()) > 0
    data = response.json()
    assert "id" in data[0]
    assert UUID(data[0]["id"]) == str(sample_job_process.id)

@pytest.mark.asyncio
async def test_list_processes_selector (client, selector_token, sample_job_process):
    response = await client.get(BASE_URL, headers=selector_token)
    assert response.status_code == 200
    assert len(response.json()) > 0
    data = response.json()
    assert "id" in data[0]
    assert UUID(data[0]["id"]) == str(sample_job_process.id)

@pytest.mark.asyncio
async def test_list_processes_head (client, head_token, sample_job_process):
    response = await client.get(BASE_URL, headers=head_token)
    assert response.status_code == 200
    assert len(response.json()) > 0
    data = response.json()
    assert "id" in data[0]
    assert UUID(data[0]["id"]) == str(sample_job_process.id)

@pytest.mark.asyncio
async def test_get_process_by_id_admin (client, admin_token, sample_job_process):
    process_id = str(sample_job_process.id)
    response = await client.get(f"{BASE_URL}/{process_id}", headers=admin_token)
    assert response.status_code == 200
    assert response.json()["id"] == process_id

@pytest.mark.asyncio
async def test_get_process_by_id_selector (client, selector_token, sample_job_process):
    process_id = str(sample_job_process.id)
    response = await client.get(f"{BASE_URL}/{process_id}", headers=selector_token)
    assert response.status_code == 200
    assert response.json()["id"] == process_id

@pytest.mark.asyncio
async def test_get_process_by_id_head (client, head_token, sample_job_process):
    process_id = str(sample_job_process.id)
    response = await client.get(f"{BASE_URL}/{process_id}", headers=head_token)
    assert response.status_code == 200
    assert response.json()["id"] == process_id

@pytest.mark.asyncio
async def test_update_process_admin (client, head_token, sample_job_process):
    proceso_id = str(sample_job_process.id)
    payload = {
        "status": EstadoGeneral.EN_PROCESO.value
    }
    response = await client.put(f"{BASE_URL}/{proceso_id}", json=payload, headers=head_token)
    assert response.status_code == 200
    assert response.json()["id"] == proceso_id
    assert response.json()["status"] == EstadoGeneral.EN_PROCESO.value

@pytest.mark.asyncio
async def test_update_process_selector (client, selector_token, sample_job_process):
    proceso_id = str(sample_job_process.id)
    payload = {
        "status": EstadoGeneral.EN_PROCESO.value
    }
    response = await client.put(f"{BASE_URL}/{proceso_id}", json=payload, headers=selector_token)
    assert response.status_code == 200
    assert response.json()["id"] == proceso_id
    assert response.json()["status"] == EstadoGeneral.EN_PROCESO.value

@pytest.mark.asyncio
async def test_update_process_head_unauthorized (client, head_token, sample_job_process):
    proceso_id = str(sample_job_process.id)
    payload = {
        "status": EstadoGeneral.EN_PROCESO.value
    }
    response = await client.put(f"{BASE_URL}/{proceso_id}", json=payload, headers=head_token)
    assert response.status_code == 403

@pytest.mark.asyncio
async def test_update_process_HR_Interview_admin (client, admin_token, sample_job_process):
    #Arrange
    proceso_id = str(sample_job_process.id)
    payload = {
        "status": EstadoGeneral.EN_PROCESO.value,
        "HR_interview": "2026-02-12",
        "email": "test@example.com",
        "phone": "123456789",
        "residence_area": ProvinciaArgentina.Buenos_Aires.value,
        "salary_expectations": 100000,
        "notice_period": NoticePeriod.TRES_MESES.value,
        "observations": "Test observations"
    }
    #Act
    response = await client.put(f"{BASE_URL}/{proceso_id}", json=payload, headers=admin_token)
    #Assert
    assert response.status_code == 200
    assert response.json()["id"] == proceso_id
    assert response.json()["status"] == EstadoGeneral.EN_PROCESO.value


@pytest.mark.asyncio
async def test_update_process_HR_Interview_selector (client, selector_token, sample_job_process):
    #Arrange
    proceso_id = str(sample_job_process.id)
    payload = {
        "status": EstadoGeneral.EN_PROCESO.value,
        "HR_interview": "2026-02-12",
        "email": "test@example.com",
        "phone": "123456789",
        "residence_area": ProvinciaArgentina.Buenos_Aires.value,
        "salary_expectations": 100000,
        "notice_period": NoticePeriod.TRES_MESES.value,
        "observations": "Test observations"
    }
    #Act
    response = await client.put(f"{BASE_URL}/{proceso_id}", json=payload, headers=selector_token)
    #Assert
    assert response.status_code == 200
    assert response.json()["id"] == proceso_id
    assert response.json()["status"] == EstadoGeneral.EN_PROCESO.value


@pytest.mark.asyncio
async def test_update_process_HR_Interview_head_unauthorized (client, head_token, sample_job_process):
    #Arrange
    proceso_id = str(sample_job_process.id)
    payload = {
        "status": EstadoGeneral.EN_PROCESO.value,
        "HR_interview": "2026-02-12",
        "email": "test@example.com",
        "phone": "123456789",
        "residence_area": ProvinciaArgentina.Buenos_Aires.value,
        "salary_expectations": 100000,
        "notice_period": NoticePeriod.TRES_MESES.value,
        "observations": "Test observations"
    }
    #Act
    response = await client.put(f"{BASE_URL}/{proceso_id}", json=payload, headers=head_token)
    #Assert
    assert response.status_code == 403

@pytest.mark.asyncio
async def test_update_process_HR_missing_data_Interview_admin (client, admin_token, sample_job_process):
    #se actualiza el proceso, pero faltan datos nulleables de candidato antes de pasar de HR interview
    proceso_id = str(sample_job_process.id)
    payload = {
        "status": EstadoGeneral.EN_PROCESO.value,
        "HR_interview": "2026-02-12",
        "email": "test@example.com",
        "phone": "123456789",
        "residence_area": "",
        "salary_expectations": 100000,
        "notice_period": "",
        "observations": "Test observations"
    }
    response = await client.put(f"{BASE_URL}/{proceso_id}", json=payload, headers=admin_token)
    assert response.status_code == 404
    assert response.json()["detail"][0]["msg"] == "Candidate field's required to pass HR interview"

@pytest.mark.asyncio
async def test_update_process_HR_missing_data_Interview_selector (client, selector_token, sample_job_process):
    #se actualiza el proceso, pero faltan datos nulleables de candidato antes de pasar de HR interview
    proceso_id = str(sample_job_process.id)
    payload = {
        "status": EstadoGeneral.EN_PROCESO.value,
        "HR_interview": "2026-02-12",
        "email": "test@example.com",
        "phone": "123456789",
        "residence_area": "",
        "salary_expectations": 100000,
        "notice_period": "",
        "observations": "Test observations"
    }
    response = await client.put(f"{BASE_URL}/{proceso_id}", json=payload, headers=selector_token)
    assert response.status_code == 404
    assert response.json()["detail"][0]["msg"] == "Candidate field's required to pass HR interview"

@pytest.mark.asyncio
async def test_delete_process_admin (client, admin_token, sample_job_process):
    proceso_id = str(sample_job_process.id)
    response = await client.delete(f"{BASE_URL}/{proceso_id}", headers=admin_token)
    assert response.status_code == 204
    new_response = await client.get(f"{BASE_URL}/{proceso_id}", headers=admin_token)
    assert new_response.status_code == 404

@pytest.mark.asyncio
async def test_delete_process_selector_unauthorized (client, selector_token, sample_job_process):
    proceso_id = str(sample_job_process.id)
    response = await client.delete(f"{BASE_URL}/{proceso_id}", headers=selector_token)
    assert response.status_code == 403

@pytest.mark.asyncio
async def test_delete_process_head_unauthorized (client, head_token, sample_job_process):
    proceso_id = str(sample_job_process.id)
    response = await client.delete(f"{BASE_URL}/{proceso_id}", headers=head_token)
    assert response.status_code == 403

@pytest.mark.asyncio
async def test_update_process_rejected_with_reason_admin(client, admin_token, sample_job_process):
    proceso_id = str(sample_job_process.id)
    payload = {
        "status": EstadoGeneral.NO_CONTINUA.value,
        "reason": "No cumple skill técnico"
    }
    response = await client.put(f"{BASE_URL}/{proceso_id}", json=payload, headers=admin_token)
    assert response.status_code == 200
    assert response.json()["id"] == proceso_id
    assert response.json()["status"] == EstadoGeneral.NO_CONTINUA.value

@pytest.mark.asyncio
async def test_update_process_rejected_with_reason_selector(client, selector_token, sample_job_process):
    proceso_id = str(sample_job_process.id)
    payload = {
        "status": EstadoGeneral.NO_CONTINUA.value,
        "reason": "No cumple skill técnico"
    }
    response = await client.put(f"{BASE_URL}/{proceso_id}", json=payload, headers=selector_token)
    assert response.status_code == 200
    assert response.json()["id"] == proceso_id
    assert response.json()["status"] == EstadoGeneral.NO_CONTINUA.value

@pytest.mark.asyncio
async def test_update_process_rejected_without_reason_admin(client, admin_token, sample_job_process):
    proceso_id = str(sample_job_process.id)
    payload = {
        "status": EstadoGeneral.NO_CONTINUA.value
    }
    response = await client.put(f"{BASE_URL}/{proceso_id}", json=payload, headers=admin_token)
    assert response.status_code == 422
    assert response.json()["detail"][0]["msg"] == "Rejection reason is required"

@pytest.mark.asyncio
async def test_update_process_rejected_without_reason_selector(client, selector_token, sample_job_process):
    proceso_id = str(sample_job_process.id)
    payload = {
        "status": EstadoGeneral.NO_CONTINUA.value
    }
    response = await client.put(f"{BASE_URL}/{proceso_id}", json=payload, headers=selector_token)
    assert response.status_code == 422
    assert response.json()["detail"][0]["msg"] == "Rejection reason is required"


@pytest.mark.asyncio
async def test_create_process_duplicate_candidate_admin(client, admin_token, sample_job, sample_candidate, sample_job_process):
    # Ensure sample_job_process links sample_job and sample_candidate
    payload = {
        "job_id": str(sample_job.id),
        "candidate_id": str(sample_candidate.id),
        "status": EstadoGeneral.SOURCING.value
    }
    response = await client.post(BASE_URL, json=payload, headers=admin_token)
    assert response.status_code == 409
    assert response.json()["detail"] == "Candidate already applied to this job"


@pytest.mark.asyncio
async def test_create_process_duplicate_candidate_selector(client, selector_token, sample_job, sample_candidate, sample_job_process):
    payload = {
        "job_id": str(sample_job.id),
        "candidate_id": str(sample_candidate.id),
        "status": EstadoGeneral.SOURCING.value
    }
    response = await client.post(BASE_URL, json=payload, headers=selector_token)
    assert response.status_code == 409
    assert response.json()["detail"] == "Candidate already applied to this job"

