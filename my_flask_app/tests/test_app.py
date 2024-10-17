import pytest
from app import app

@pytest.fixture
def client():
    with app.test_client() as client:
        yield client

def test_healthcheck(client):
    """Test the /healthcheck endpoint."""

    response = client.get('/healthcheck')
    json_data = response.get_json()

    assert response.status_code == 200
    assert "myapplication" in json_data
    assert json_data["myapplication"][0]["version"] == "1.0"
    assert json_data["myapplication"][0]["description"] == "dmod-1/app.py"
    assert json_data["myapplication"][0]["lastcommitsha"] == "abc57858585"

def test_404_error(client):
    """Test a non-existent endpoint to trigger 404."""
    
    response = client.get('/nonexistent')
    assert response.status_code == 404
    assert response.get_json() == {"error": "Resource not found"}
