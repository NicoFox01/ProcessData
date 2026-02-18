import pytest
from uuid import uuid4, UUID
from app.models.enums import ProvinciaArgentina, NoticePeriod
from app.models.candidato import Candidato

BASE_URL = "/api/v1/candidates"

@pytest.mark.asyncio
async def test_create_candidate_admin(client, admin_token, sample_candidate):
    payload={
    "full_name": "Nicolás Gonzalez",
    "linkedin_url": "http://linkedin.com.ar/es/nicolas-gonzalez"
    }
    response = await client.post(BASE_URL, json=payload, headers=admin_token)
    assert response.status_code == 201
    assert response.json()["full_name"] == "Nicolás Gonzalez"
    assert response.json()["linkedin_url"] == "http://linkedin.com.ar/es/nicolas-gonzalez"
    data = response.json()
    assert isinstance(data["id"], UUID)

@pytest.mark.asyncio
async def test_create_candidate_selector(client, selector_token, sample_candidate):
    payload={
    "full_name": "Nicolás Gonzalez",
    "linkedin_url": "http://linkedin.com.ar/es/nicolas-gonzalez"
    }
    response = await client.post(BASE_URL, json=payload, headers=selector_token)
    assert response.status_code == 201
    assert response.json()["full_name"] == "Nicolás Gonzalez"
    assert response.json()["linkedin_url"] == "http://linkedin.com.ar/es/nicolas-gonzalez"
    data = response.json()
    assert isinstance(data["id"], UUID)

@pytest.mark.asyncio
async def test_create_candidate_head_unauthorized(client, head_token, sample_candidate):
    payload={
    "full_name": "Nicolás Gonzalez",
    "linkedin_url": "http://linkedin.com.ar/es/nicolas-gonzalez"
    }
    response = await client.post(BASE_URL, json=payload, headers=head_token)
    assert response.status_code == 403

@pytest.mark.asyncio
async def test_create_candidate_with_complete_data_admin(client, admin_token, sample_candidate):
    payload={
    "full_name": "Joaquin Perez",
    "linkedin_url": "http://linkedin.com.ar/es/joaquin-perez",
    "email": "joaquin.perez@gmail.com",
    "phone": "123456789",
    "residence_area": ProvinciaArgentina.CHUBUT.value,
    "salary_expectations": 100000,
    "notice_period": NoticePeriod.IMMEDIATE.value,
    "observations": "Nada"
    }
    response = await client.post(BASE_URL, json=payload, headers=admin_token)
    assert response.status_code == 201
    assert response.json()["full_name"] == "Joaquin Perez"
    assert response.json()["linkedin_url"] == "http://linkedin.com.ar/es/joaquin-perez"
    assert response.json()["email"] == "joaquin.perez@gmail.com"
    assert response.json()["phone"] == "123456789"
    assert response.json()["residence_area"] == ProvinciaArgentina.CHUBUT.value
    assert response.json()["salary_expectations"] == 100000
    assert response.json()["notice_period"] == NoticePeriod.IMMEDIATE.value
    assert response.json()["observations"] == "Nada"
    data = response.json()
    assert isinstance(data["id"], UUID)

@pytest.mark.asyncio
async def test_create_candidate_with_complete_data_selector(client, selector_token, sample_candidate):
    payload={
    "full_name": "Joaquin Perez",
    "linkedin_url": "http://linkedin.com.ar/es/joaquin-perez",
    "email": "joaquin.perez@gmail.com",
    "phone": "123456789",
    "residence_area": ProvinciaArgentina.CORDOBA.value,
    "salary_expectations": 100000,
    "notice_period": NoticePeriod.THREE_WEEKS.value,
    "observations": "Nada"
    }
    response = await client.post(BASE_URL, json=payload, headers=selector_token)
    assert response.status_code == 201
    assert response.json()["full_name"] == "Joaquin Perez"
    assert response.json()["linkedin_url"] == "http://linkedin.com.ar/es/joaquin-perez"
    assert response.json()["email"] == "joaquin.perez@gmail.com"
    assert response.json()["phone"] == "123456789"
    assert response.json()["residence_area"] == ProvinciaArgentina.CORDOBA.value
    assert response.json()["salary_expectations"] == 100000
    assert response.json()["notice_period"] == NoticePeriod.THREE_WEEKS.value
    assert response.json()["observations"] == "Nada"
    data = response.json()
    assert isinstance(data["id"], UUID)

@pytest.mark.asyncio
async def test_create_candidate_duplicate_admin(client, admin_token, sample_candidate):
    payload = {
        "full_name": "J. L. Rodriguez",
        "linkedin_url": "https://www.linkedin.com/in/joseluisrodriguezp/"
    }
    response = await client.post(BASE_URL, json=payload, headers=admin_token)
    assert response.status_code == 400
    assert response.json()["detail"] == "Candidate already exists"

@pytest.mark.asyncio
async def test_create_candidate_duplicate_selector(client, selector_token, sample_candidate):
    payload = {
        "full_name": "J. L. Rodriguez",
        "linkedin_url": "https://www.linkedin.com/in/joseluisrodriguezp/"
    }
    response = await client.post(BASE_URL, json=payload, headers=selector_token)
    assert response.status_code == 400
    assert response.json()["detail"] == "Candidate already exists"

@pytest.mark.asyncio
async def test_list_candidates_admin(client, admin_token, sample_candidate):
    response = await client.get(BASE_URL, headers=admin_token)
    assert response.status_code == 200
    assert len(response.json()) > 0

@pytest.mark.asyncio
async def test_list_candidates_selector(client, selector_token, sample_candidate):
    response = await client.get(BASE_URL, headers=selector_token)
    assert response.status_code == 200
    assert len(response.json()) > 0

@pytest.mark.asyncio
async def test_list_candidates_head(client, head_token, sample_candidate):
    response = await client.get(BASE_URL, headers=head_token)
    assert response.status_code == 200
    assert len(response.json()) > 0

@pytest.mark.asyncio
async def test_get_candidate_by_id_admin(client, admin_token, sample_candidate):
    response = await client.get(f"{BASE_URL}/{sample_candidate.id}", headers=admin_token)
    assert response.status_code == 200
    data = response.json()
    assert data["id"] == sample_candidate.id
    assert data["email"] == sample_candidate.email

@pytest.mark.asyncio
async def test_get_candidate_by_id_selector(client, selector_token, sample_candidate):
    response = await client.get(f"{BASE_URL}/{sample_candidate.id}", headers=selector_token)
    assert response.status_code == 200
    data = response.json()
    assert data["id"] == sample_candidate.id
    assert data["email"] == sample_candidate.email


@pytest.mark.asyncio
async def test_get_candidate_by_id_head(client, head_token, sample_candidate):
    response = await client.get(f"{BASE_URL}/{sample_candidate.id}", headers=head_token)
    assert response.status_code == 200
    data = response.json()
    assert data["id"] == sample_candidate.id
    assert data["email"] == sample_candidate.email

@pytest.mark.asyncio
async def test_update_candidate_admin(client, admin_token, sample_candidate):
    candidato_id = str(sample_candidate.id)
    payload = {
        "phone": "+5491122334455",
        "email": "email_test@gmail.com",
        "residence_area": ProvinciaArgentina.BUENOS_AIRES.value
    }
    response = await client.put(f"{BASE_URL}/{candidato_id}", json=payload, headers=admin_token, follow_redirects=True)
    assert response.status_code == 200
    data = response.json()
    assert data["phone"] == "+5491122334455"
    assert data["email"] == "email_test@gmail.com"
    assert data["residence_area"] == ProvinciaArgentina.BUENOS_AIRES.value

@pytest.mark.asyncio
async def test_update_candidate_selector(client, selector_token, sample_candidate):
    candidato_id = str(sample_candidate.id)
    payload = {
        "phone": "+5491122334456",
        "email": "email_testing@gmail.com",
        "residence_area": ProvinciaArgentina.CATAMARCA.value
    }
    response = await client.put(f"{BASE_URL}/{candidato_id}", json=payload, headers=selector_token, follow_redirects=True)
    assert response.status_code == 200
    data = response.json()
    assert data["phone"] == "+5491122334456"
    assert data["email"] == "email_testing@gmail.com"
    assert data["residence_area"] == ProvinciaArgentina.CATAMARCA.value

@pytest.mark.asyncio
async def test_update_candidate_head_unauthorized(client, head_token, sample_candidate):
    candidato_id = str(sample_candidate.id)
    payload = {
        "phone": "+5491122334458",
        "email": "email_testing_head@gmail.com",
        "residence_area": ProvinciaArgentina.LA_PAMPA.value
    }
    response = await client.put(f"{BASE_URL}/{candidato_id}", json=payload, headers=head_token, follow_redirects=True)
    assert response.status_code == 403

@pytest.mark.asyncio
async def test_delete_candidate_admin(client, admin_token, sample_candidate):
    candidato_id = str(sample_candidate.id)
    response = await client.delete(f"{BASE_URL}/{candidato_id}", headers=admin_token, follow_redirects=True)
    assert response.status_code == 204
    check_response = await client.get(f"{BASE_URL}/{candidato_id}", headers=admin_token, follow_redirects=True)
    assert check_response.status_code == 404

@pytest.mark.asyncio
async def test_delete_candidate_selector(client, selector_token, sample_candidate):
    candidato_id = str(sample_candidate.id)
    response = await client.delete(f"{BASE_URL}/{candidato_id}", headers=selector_token, follow_redirects=True)
    assert response.status_code == 204
    check_response = await client.get(f"{BASE_URL}/{candidato_id}", headers=selector_token, follow_redirects=True)
    assert check_response.status_code == 404

@pytest.mark.asyncio
async def test_delete_candidate_head_unauthorized(client, head_token, sample_candidate):
    candidato_id = str(sample_candidate.id)
    response = await client.delete(f"{BASE_URL}/{candidato_id}", headers=head_token, follow_redirects=True)
    assert response.status_code == 403
