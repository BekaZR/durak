from redis import Redis
from core.settings import settings

redis_client = Redis(host=f"{settings.REDIS_HOST}", port=settings.REDIS_PORT, db=0, decode_responses=True)
