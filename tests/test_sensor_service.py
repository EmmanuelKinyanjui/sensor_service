import pytest
from fastapi.testclient import TestClient
from datetime import datetime, timedelta
from core.main import app
from core.models import SensorData

client = TestClient(app)

@pytest.fixture
def sample_data(db_session):
    sensor_data = [
        SensorData(
            sensor_id="SENSOR_001",
            human_presence=5,
            dwell_time=2.5,
            timestamp=datetime.now() - timedelta(hours=i),
            raw_data={"test": "data"}
        ) for i in range(24)  # Last 24 hours of data
    ]
    db_session.bulk_save_objects(sensor_data)
    db_session.commit()
    return sensor_data

def test_get_sensor_data_success(sample_data):
    response = client.get("/sensor_data/?sensor_id=SENSOR_001")
    print("responsee", response.json())
    assert response.status_code == 200
    data = response.json()
    assert "chart_data" in data
    assert len(data["chart_data"]["timestamps"]) > 0

def test_get_sensor_data_not_found(sample_data):
    response = client.get("/sensor_data/?sensor_id=NONEXISTENT")
    assert response.status_code == 404

def test_get_sensor_data_time_intervals(sample_data):
    intervals = ["minute", "hour", "day", "week", "month"]
    for interval in intervals:
        response = client.get(f"/sensor_data/?interval={interval}")
        assert response.status_code == 200
        data = response.json()
        assert "chart_data" in data

def test_get_sensor_data_time_range(sample_data):
    start_time = (datetime.now() - timedelta(hours=12)).isoformat()
    end_time = datetime.now().isoformat()
    response = client.get(
        f"/sensor_data/?start_time={start_time}&end_time={end_time}"
    )
    assert response.status_code == 200
    data = response.json()
    assert "chart_data" in data

def test_get_sensor_data_invalid_interval(sample_data):
    response = client.get("/sensor_data/?interval=invalid_interval")
    assert response.status_code == 400
    data = response.json()
    assert "detail" in data

def test_get_sensor_data_invalid_date_range(sample_data):
    future_time = (datetime.now() + timedelta(days=7)).isoformat()
    response = client.get(
        f"/sensor_data/?start_time={future_time}&end_time={future_time}"
    )
    assert response.status_code == 404
    data = response.json()
    assert "detail" in data

def test_get_sensor_data_reversed_date_range(sample_data):
    end_time = (datetime.now() - timedelta(hours=24)).isoformat()
    start_time = datetime.now().isoformat()
    response = client.get(
        f"/sensor_data/?start_time={start_time}&end_time={end_time}"
    )
    assert response.status_code == 400
    data = response.json()
    assert "detail" in data
