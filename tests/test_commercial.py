import pytest
from uuid import uuid4

# TEST PARA EMPRESAS
@pytest.mark.asyncio
async def test_create_company_admin_success(client, admin_token):
    #Arrange
    payload = {
        "company_name": "Empresa Test"
    }
    #Act
    response = await client.post("/api/v1/companies", json=payload, headers = admin_token) 
    #Assert
    assert response.status_code == 201
    data = response.json()
    assert data["company_name"] == payload["company_name"]

@pytest.mark.asyncio
async def test_create_company_forbidden_for_selector(client, selector_token):
    #Arrange
    payload = {
        "company_name": "Empresa Test"
    }
    #Act
    response = await client.post("/api/v1/companies", json=payload, headers = selector_token) 
    #Assert
    assert response.status_code == 403

@pytest.mark.asyncio
async def test_create_company_forbidden_for_head(client, head_token):
    #Arrange
    payload = {
        "company_name": "Empresa Test"
    }
    #Act
    response = await client.post("/api/v1/companies", json=payload, headers = head_token) 
    #Assert
    assert response.status_code == 403

@pytest.mark.asyncio
async def test_read_companies_admin_success(client, admin_token, sample_company):
    #Arrange
    
    #Act
    response = await client.get("/api/v1/companies/", headers = admin_token)
    #Assert
    assert response.status_code == 200
    data = response.json()
    assert isinstance(data, list)
    assert len(data) > 0

@pytest.mark.asyncio
async def test_read_companies_selector_success(client, selector_token, sample_client):
    #Arrange
    
    #Act
    response = await client.get("/api/v1/companies/", headers = selector_token)
    #Assert
    assert response.status_code == 200
    data = response.json()
    assert isinstance(data, list)
    assert len(data) > 0

@pytest.mark.asyncio
async def test_read_companies_head_success(client, head_token, sample_company):
    #Arrange
    
    #Act
    response = await client.get("/api/v1/companies/", headers = head_token)
    #Assert
    assert response.status_code == 200
    data = response.json()
    assert isinstance(data, list)
    assert len(data) > 0

@pytest.mark.asyncio
async def test_read_company_by_id_admin_success(client, admin_token, sample_company):
    #Arrange
    #Act
    response = await client.get(f"/api/v1/companies/{sample_company.id}", headers = admin_token)
    #Assert
    assert response.status_code == 200
    data = response.json()
    assert data["id"] == str(sample_company.id)

@pytest.mark.asyncio
async def test_read_company_by_id_selector_success(client, selector_token, sample_company):
    #Arrange
    #Act
    response = await client.get(f"/api/v1/companies/{sample_company.id}", headers = selector_token)
    #Assert
    assert response.status_code == 200
    data = response.json()
    assert data["id"] == str(sample_company.id)

@pytest.mark.asyncio
async def test_read_company_by_id_head_success(client, head_token, sample_company):
    #Arrange
    #Act
    response = await client.get(f"/api/v1/companies/{sample_company.id}", headers = head_token)
    #Assert
    assert response.status_code == 200
    data = response.json()
    assert data["id"] == str(sample_company.id)

@pytest.mark.asyncio
async def test_update_company_admin_success(client, admin_token, sample_company):
    #Arrange
    payload = {
        "company_name": "Empresa Test1"
    }
    #Act
    response = await client.put(f"/api/v1/companies/{sample_company.id}", json=payload, headers=admin_token)
    #Assert
    assert response.status_code == 200
    data = response.json()
    assert data["company_name"] == payload["company_name"]
@pytest.mark.asyncio
async def test_update_company_forbidden_for_selector(client, selector_token, sample_company):
    #Arrange
    payload = {
        "company_name": "Empresa Test1"
    }
    #Act
    response = await client.put(f"/api/v1/companies/{sample_company.id}", json=payload, headers=selector_token)
    #Assert
    assert response.status_code == 403
@pytest.mark.asyncio
async def test_update_company_forbidden_for_head(client, head_token, sample_company):
    #Arrange
    payload = {
        "company_name": "Empresa Test1"
    }
    #Act
    response = await client.put(f"/api/v1/companies/{sample_company.id}", json=payload, headers=head_token)
    #Assert
    assert response.status_code == 403

@pytest.mark.asyncio
async def test_delete_company_admin_success(client, admin_token, sample_company):
    #Arrange

    #act
    response = await client.delete(f"/api/v1/companies/{sample_company.id}", headers=admin_token)
    #Assert
    assert response.status_code == 204
@pytest.mark.asyncio
async def test_delete_company_forbidden_for_selector(client, selector_token, sample_company):
    #Arrange

    #act
    response = await client.delete(f"/api/v1/companies/{sample_company.id}", headers=selector_token)
    #Assert
    assert response.status_code == 403
@pytest.mark.asyncio
async def test_delete_company_forbidden_for_head(client, head_token, sample_company):
    #Arrange

    #act
    response = await client.delete(f"/api/v1/companies/{sample_company.id}", headers=head_token)
    #Assert
    assert response.status_code == 403
# TEST PARA CLIENTES
@pytest.mark.asyncio
async def test_create_client_valid_company(client, admin_token, sample_company):
    #Arrange
    payload = {
        "client_name": "Cliente de Prueba",
        "empresa_id": str(sample_company.id)
    }
    #Act
    response = await client.post("/api/v1/clients/", json=payload, headers=admin_token)
    #Assert
    assert response.status_code == 201
    data = response.json()
    assert data["empresa_id"] == payload["empresa_id"]

@pytest.mark.asyncio
async def test_create_client_invalid_company(client, admin_token):
    #Arrange
    payload = {
        "client_name": "Cliente Huérfano",
        "empresa_id": str(uuid4())
    }
    #Act
    response = await client.post("/api/v1/clients/", json=payload, headers=admin_token)
    #Assert
    assert response.status_code == 404

@pytest.mark.asyncio
async def test_create_client_forbidden_for_selector(client, selector_token, sample_company):
    #Arrange
    payload = {
        "client_name": "Cliente de Prueba",
        "empresa_id": str(sample_company.id)
    }
    #Act
    response = await client.post("/api/v1/clients/", json=payload, headers=selector_token)
    #Assert
    assert response.status_code == 403

@pytest.mark.asyncio
async def test_create_client_forbidden_for_head(client, head_token, sample_company):
    #Arrange
    payload = {
        "client_name": "Cliente de Prueba",
        "empresa_id": str(sample_company.id)
    }
    #Act
    response = await client.post("/api/v1/clients/", json=payload, headers=head_token)
    #Assert
    assert response.status_code == 403

@pytest.mark.asyncio
async def test_read_clients_admin_success(client, admin_token, sample_client):
    #Arrange

    #Act
    response = await client.get("/api/v1/clients/", headers = admin_token)
    #Assert
    assert response.status_code == 200
    data = response.json()
    assert isinstance(data, list)
    assert len(data) > 0

@pytest.mark.asyncio
async def test_read_clients_selector_success(client, selector_token, sample_client):
    #Arrange
    #Act
    response = await client.get("/api/v1/clients/", headers = selector_token)
    #Assert
    assert response.status_code == 200
    data = response.json()
    assert isinstance(data, list)
    assert len(data) > 0

@pytest.mark.asyncio
async def test_read_clients_head_success(client, head_token, sample_client):
    #Arrange
    #Act
    response = await client.get("/api/v1/clients/", headers = head_token)
    #Assert
    assert response.status_code == 200
    data = response.json()
    assert isinstance(data, list)
    assert len(data) > 0

@pytest.mark.asyncio
async def test_read_client_by_id_admin_success(client, admin_token, sample_client):
    #Arrange
    #Act
    response = await client.get(f"/api/v1/clients/{sample_client.id}", headers = admin_token)
    #Assert
    assert response.status_code == 200
    data = response.json()
    assert data["id"] == str(sample_client.id)

@pytest.mark.asyncio
async def test_read_client_by_id_selector_success(client, selector_token, sample_client):
    #Arrange
    #Act
    response = await client.get(f"/api/v1/clients/{sample_client.id}", headers = selector_token)
    #Assert
    assert response.status_code == 200
    data = response.json()
    assert data["id"] == str(sample_client.id)

@pytest.mark.asyncio
async def test_read_client_by_id_head_success(client, head_token, sample_client):
    #Arrange
    #Act
    response = await client.get(f"/api/v1/clients/{sample_client.id}", headers = head_token)
    #Assert
    assert response.status_code == 200
    data = response.json()
    assert data["id"] == str(sample_client.id)

@pytest.mark.asyncio
async def test_update_client_admin_success(client, admin_token, sample_client):
    #Arrange
    payload = {
        "client_name": "Cliente de Prueba 1"
    }
    #Act
    response = await client.put(f"/api/v1/clients/{sample_client.id}", json=payload, headers=admin_token)
    #Assert
    assert response.status_code == 200
    data = response.json()
    assert data["client_name"] == payload["client_name"]
@pytest.mark.asyncio
async def test_update_client_forbidden_for_selector(client, selector_token, sample_client):
    #Arrange
    payload = {
        "client_name": "Cliente de Prueba 1"
    }
    #Act
    response = await client.put(f"/api/v1/clients/{sample_client.id}", json=payload, headers=selector_token)
    #Assert
    assert response.status_code == 403
@pytest.mark.asyncio
async def test_update_client_forbidden_for_head(client, head_token, sample_client):
    #Arrange
    payload = {
        "client_name": "Cliente de Prueba 1"
    }
    #Act
    response = await client.put(f"/api/v1/clients/{sample_client.id}", json=payload, headers=head_token)
    #Assert
    assert response.status_code == 403

@pytest.mark.asyncio
async def test_delete_client_admin_success(client, admin_token, sample_client):
    #Arrange

    #Act
    response = await client.delete(f"/api/v1/clients/{sample_client.id}", headers=admin_token)
    #Assert
    assert response.status_code == 204
@pytest.mark.asyncio
async def test_delete_client_forbidden_for_selector(client, selector_token, sample_client):
    #Arrange

    #Act
    response = await client.delete(f"/api/v1/clients/{sample_client.id}", headers=selector_token)
    #Assert
    assert response.status_code == 403
@pytest.mark.asyncio
async def test_delete_client_forbidden_for_head(client, head_token, sample_client):
    #Arrange

    #Act
    response = await client.delete(f"/api/v1/clients/{sample_client.id}", headers=head_token)
    #Assert
    assert response.status_code == 403
