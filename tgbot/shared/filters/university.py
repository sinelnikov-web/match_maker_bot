from aiogram.filters import BaseFilter
from aiogram.types import Message

from dto import UserDTO
from tgbot.shared.enums import AuthType


class AuthenticatedUser(BaseFilter):
    def __init__(self, authentication_type: AuthType):
        self.auth_type = authentication_type

    async def __call__(self, message: Message, user: UserDTO) -> bool:
        return len(getattr(user, f"{self.auth_type.value}_accounts")) > 0
