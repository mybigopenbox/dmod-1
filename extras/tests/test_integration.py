import pytest
import os
from flask import Flask
from app import app

DATABASE_URL = os.getenv('DATABASE_URL', 'postgresql://user:password@localhost/test_db')

@pytest.fixture
def client():
    """Flask test client fixture."""

    app.config['TESTING'] = True
    with app.test_client() as client:
        yield client

def test_db_connection(client):
    """Simple integration test to check database connection."""
    
    response = client.get('/healthcheck')
    assert response.status_code == 200
    assert "myapplication" in response.get_json()
