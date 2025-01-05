import base64
import json
import logging
import huey

from core.database import SessionLocal
from core import models
from core.tasks import huey

logger = logging.getLogger("huey")

def decode_message(data_encoded: str) -> str:
    try:
        return base64.b64decode(data_encoded).decode("utf-8")
    except Exception as e:
        raise ValueError(f"Failed to decode message: {str(e)}")


@huey.task()
def process_message(data_encoded: str):
    db = SessionLocal()
    try:
        data_decoded = decode_message(data_encoded)
        parsed_data = json.loads(data_decoded)

        required_fields = ["v0", "v11", "v18", "Time"] # as per the specification provided 
        if not all(field in parsed_data for field in required_fields):
            logger.error("Missing required fields in the data")

        sensor_data = models.SensorData(
            sensor_id=parsed_data["v0"],
            human_presence=parsed_data["v11"],
            dwell_time=parsed_data["v18"],
            timestamp=parsed_data["Time"],
            raw_data=parsed_data,
        )
        db.add(sensor_data)
        db.commit()
    except json.JSONDecodeError as e:
        logger.error("Invalid JSON data")
    except Exception as e:
        logger.error(f"An error occurred in the decoding process: {str(e)}")
    finally:
        db.close()
