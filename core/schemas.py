from pydantic import BaseModel
from datetime import datetime


class SensorDataIn(BaseModel):
    serial: str
    v11: int
    v18: float
    Time: datetime


class SensorDataOut(SensorDataIn):
    id: int

    class Config:
        orm_mode = True
