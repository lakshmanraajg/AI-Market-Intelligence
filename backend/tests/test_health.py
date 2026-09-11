from fastapi.testclient import TestClient
from app.main import app

def test_health():
    response = TestClient(app).get('/health')
    assert response.status_code == 200
    assert response.json()['status'] == 'ok'

def test_unavailable_market_is_never_live():
    data = TestClient(app).get('/api/v1/markets/snapshots/NIFTY50').json()
    assert data['freshness'] == 'UNAVAILABLE'
