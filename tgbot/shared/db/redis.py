import aioredis

from dto import UserDTO
from tgbot.settings.env import REDIS_IP

redis_instance = aioredis.from_url(f"redis://{REDIS_IP}:6379")

class RedisService:

    @staticmethod
    async def set(user: UserDTO, data: dict):
        old_data = await redis_instance.hgetall(user.id) or {}
        await redis_instance.hset(user.id, mapping={
            **old_data,
            **data
        })

    @staticmethod
    async def get(user: UserDTO) -> dict:
        return await redis_instance.hgetall(user.id)