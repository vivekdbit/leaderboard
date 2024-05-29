import pytest
from app import create_app

@pytest.fixture
def app():
    app = create_app()
    yield app

@pytest.fixture
def client(app):
    # Create a test client
    with app.test_client() as client:
        yield client

def test_add_user(client):
    # Simulate a POST request to add a user
    response = client.post('/api/v1/users', json={}, headers={"Authorization": "Basic YWRtaW46cGFzc3dvcmQ="})
    assert response.status_code == 201
    data = response.json
    assert data['message'] == 'User created successfully'

def test_delete_user(client):
    # Create a user first
    response = client.post('/api/v1/users', json={}, headers={"Authorization": "Basic YWRtaW46cGFzc3dvcmQ="})
    user_id = response.json['data']['_id']

    # Delete the created user
    response = client.delete(f'/api/v1/users/{user_id}', headers={"Authorization": "Basic YWRtaW46cGFzc3dvcmQ="})
    assert response.status_code == 200
    data = response.json
    assert data['message'] == 'User deleted'

def test_get_users(client):
    response = client.get('/api/v1/users', headers={"Authorization": "Basic YWRtaW46cGFzc3dvcmQ="})
    assert response.status_code == 200
    data = response.json
    assert 'data' in data
    assert isinstance(data['data'], list)