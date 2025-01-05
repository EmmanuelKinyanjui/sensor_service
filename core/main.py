import json
from fastapi import FastAPI, Depends, HTTPException, status
from sqlalchemy.orm import Session
from . import database
from core.tasks import tasks

from fastapi import FastAPI, Depends, Response, Query
from sqlalchemy.orm import Session
from sqlalchemy import func, asc
from datetime import datetime
from typing import Optional
from . import database, models

app = FastAPI()


@app.post(
        path="/sensor_data/",
        summary="Receive encoded sensor data",
        description="Receives the encoded sensor data in the form below and passes it to a background task for processing",
        response_description="Returns a message indicating successful receipt of the data",
        tags=["Sensor Data"],
)
async def post_sensor_data(data: dict):
    """
    Receives the encoded sensor data in the form below and passes it to a background task for processing
    {
        "message": {
            "attributes": {
                "key": "value"
            },
            "data":"eyJzZXJpYWwiOiIwMDAxMDAwMDAxMDAiLCJhcHBsaWNhdGlvbiI6MTEsIlRpbWUiOiIyMDIyLTExLTA4VDA0OjAwOjA0LjMxNzgwMSIsIlR5cGUiOiJ4a2d3",
            "messageId": "2070443601311540",
            "message_id": "2070443601311540",
            "publishTime": "2021-02-26T19:13:55.749Z",
            "publish_time": "2021-02-26T19:13:55.749Z"
        },
        "subscription": "projects/myproject/subscriptions/mysubscription"
    }
    """

    # get the data field from the above payload
    encoded_data = data["message"]["data"]

    # process the message
    tasks.process_message(encoded_data)

    return Response(content=json.dumps({"message": "Message processed successfully"}), status_code=status.HTTP_200_OK, media_type="application/json")


@app.get(
        path="/sensor_data/",
        summary="Get sensor data",
        description="Retrieves sensor data based on the provided parameters",
        response_description="Returns the sensor data in the specified format",
        tags=["Sensor Data"],
)
def get_sensor_data(
    db: Session = Depends(database.get_db),
    sensor_id: Optional[str] = None,
    start_time: Optional[datetime] = None,
    end_time: Optional[datetime] = None,
    interval: str = Query(
        default="hour", enum=["minute", "hour", "day", "week", "month"]
    ),
):
    # Validate interval
    valid_intervals = ["minute", "hour", "day", "week", "month"]
    if interval not in valid_intervals:
        raise HTTPException(
            status_code=400,
            detail=f"Invalid interval. Must be one of: {', '.join(valid_intervals)}",
        )
    
    # Validate date range
    if start_time and end_time and start_time > end_time:
        raise HTTPException(
            status_code=400,
            detail="start_time cannot be later than end_time"
        )

    # Base query
    query = db.query(
        func.date_trunc(interval, models.SensorData.timestamp).label("time_bucket"),
        func.avg(models.SensorData.human_presence).label("avg_presence"),
        func.avg(models.SensorData.dwell_time).label("avg_dwell_time"),
        func.count(models.SensorData.sensor_id).label("reading_count"),
    )

    # Apply filters
    if sensor_id:
        sensor_exists = (
            db.query(models.SensorData.sensor_id)
            .filter(models.SensorData.sensor_id == sensor_id)
            .first()
        )
        if not sensor_exists:
            raise HTTPException(
                status_code=404, 
                detail=f"Sensor with ID {sensor_id} not found"
            )
        query = query.filter(models.SensorData.sensor_id == sensor_id)

    if start_time:
        query = query.filter(models.SensorData.timestamp >= start_time)
    if end_time:
        query = query.filter(models.SensorData.timestamp <= end_time)

    # Group and order
    query = query.group_by("time_bucket").order_by(asc("time_bucket"))
    results = query.all()

    # Check if any data was found
    if not results:
        raise HTTPException(
            status_code=404,
            detail="No data found for the specified parameters"
        )

    return Response(
        content=json.dumps({
            "chart_data": {
                "timestamps": [r.time_bucket.isoformat() for r in results],
                "presence": [float(r.avg_presence) for r in results],
                "dwell_time": [float(r.avg_dwell_time) for r in results],
                "reading_count": [r.reading_count for r in results],
            }
        }),
        status_code=200,
        media_type="application/json"
    )
