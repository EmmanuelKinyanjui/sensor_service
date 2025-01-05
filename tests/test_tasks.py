import base64
import json
import pytest
from core.tasks.tasks import decode_message

def test_decode_message_success(db_session):
    # Create test data
    test_data = {
        "v0": "test_sensor_1",
        "v11": True,
        "v18": 120,
        "Time": "2023-12-20T10:00:00",
    }

    # Encode the test data
    encoded_data = base64.b64encode(json.dumps(test_data).encode()).decode()
    result = decode_message(encoded_data)
    assert json.loads(result) == test_data


def test_decode_message_invalid_data():
    invalid_data = "not_valid_base64!@#$"

    with pytest.raises(Exception) as exc_info:
        decode_message(invalid_data)

    assert "Failed to decode message" in str(exc_info.value)
