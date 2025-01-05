from huey import PriorityRedisHuey
from redis import ConnectionPool

import settings

huey = PriorityRedisHuey(
    name="sensor-service-huey",
    results=False,
    immediate=False,
    utc=True,
    blocking=True,
    connection_pool=ConnectionPool(
        host=settings.REDIS_HOST, port=settings.REDIS_PORT, max_connections=20
    ),
)
