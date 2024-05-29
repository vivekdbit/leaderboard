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

def test_upsert_score(client):
    # Create a user first
    response = client.post('/api/v1/users', json={}, headers={"Authorization": "Basic YWRtaW46cGFzc3dvcmQ="})
    user_id = response.json['data']['_id']

    # Upsert score for the created user
    response = client.post('/api/v1/users/score', json={"user_id": user_id, "score": 25}, headers={"Authorization": "Basic YWRtaW46cGFzc3dvcmQ="})
    assert response.status_code == 200
    data = response.json
    assert 'data' in data
    assert data['data']['user_id'] == user_id
    assert data['data']['score'] == 25

def test_get_users_grouped_by_score(client):
    response = client.get('/api/v1/users/aggregate', headers={"Authorization": "Basic YWRtaW46cGFzc3dvcmQ="})
    assert response.status_code == 200
    data = response.json
    assert 'data' in data
    assert isinstance(data['data'], dict)