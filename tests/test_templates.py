import pytest

BASE_URL = "/api/v1/templates/"

@pytest.mark.asyncio
async def test_create_template_happy_path_admin(client, sample_job, admin_token):
    payload = {
        "job_id": str(sample_job.id),
        "name": "Template 1",
        "description": "Template basado en el Job de muestra",
    }
    
    response = await client.post(BASE_URL, json=payload, headers=admin_token)
    
    assert response.status_code == 201
    data = response.json()
    
    assert data["name"] == payload["name"]
    assert "id" in data
    
    assert data["vertical"] == sample_job.vertical.value
    assert data["type_of_process"] == sample_job.type_of_process.value

@pytest.mark.asyncio
async def test_create_template_happy_path_selector(client, sample_job, selector_token):
    payload = {
        "job_id": str(sample_job.id),
        "name": "Template 1",
        "description": "Template basado en el Job de muestra",
    }
    
    response = await client.post(BASE_URL, json=payload, headers=selector_token)
    
    assert response.status_code == 201
    data = response.json()
    
    assert data["name"] == payload["name"]
    assert "id" in data
    
    assert data["vertical"] == sample_job.vertical.value
    assert data["type_of_process"] == sample_job.type_of_process.value

@pytest.mark.asyncio
async def test_create_template_unauthorized_head(client, sample_job, head_token):
    payload = {
        "job_id": str(sample_job.id),
        "name": "Template 1",
        "description": "Template basado en el Job de muestra",
    }
    response = await client.post(BASE_URL, json=payload, headers=head_token)
    assert response.status_code == 403

@pytest.mark.asyncio
async def test_list_templates_admin(client, sample_job, admin_token):
    response = await client.get(BASE_URL, headers=admin_token)
    assert response.status_code == 200
    data = response.json()
    assert isinstance(data, list)

@pytest.mark.asyncio
async def test_list_templates_selector(client, sample_job, selector_token):
    response = await client.get(BASE_URL, headers=selector_token)
    assert response.status_code == 200
    data = response.json()
    assert isinstance(data, list)

@pytest.mark.asyncio
async def test_list_templates_head(client, sample_job, head_token):
    response = await client.get(BASE_URL, headers=head_token)
    assert response.status_code == 403

