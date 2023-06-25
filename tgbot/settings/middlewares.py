from typing import Callable, Dict, Any, Awaitable

from aiogram import BaseMiddleware
from aiogram.types import Message

from dto import UserDTO
from shared.utils import create_dto
from telegram.services import get_or_create_user


class UserRegisterMiddleware(BaseMiddleware):
    async def __call__(
            self,
            handler: Callable[[Message, Dict[str, Any]], Awaitable[Any]],
            event: Message,
            data: Dict[str, Any]
    ):
        user = event.from_user
        model, _ = await get_or_create_user(
            user.id,
            {
                "username": user.username,
                "full_name": f"{user.first_name} {user.last_name}",
            }
        )
        data['user'] = create_dto(model, UserDTO)
        return await handler(event, data)
