from typing import Dict, Any

from dto import UserDTO
from telegram.models import TelegramUser


async def get_or_create_user(id: int, defaults: Dict[str, Any]) -> TelegramUser:
    return await TelegramUser.objects.aget_or_create(id=id, defaults=defaults)


async def update_user(id: int, user_dto: UserDTO):
    return await TelegramUser.objects.aupdate_or_create(id=id, defaults={
        "username": user_dto.username,
        "email": user_dto.email,
        "language": user_dto.language.value,
        "phone": user_dto.phone,
        "full_name": user_dto.full_name
    })
