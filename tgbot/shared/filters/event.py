from typing import Union

from aiogram.filters import BaseFilter
from aiogram.types import Message

from dto import UserDTO
from shared.enums import EventStatus
from tgbot.shared.db.api import get_event_by_team
from tgbot.shared.keyboards.invite_user import InviteCallback, LeaveCallback


class ActiveEvent(BaseFilter):

    async def __call__(self, message: Message, user: UserDTO, callback_data: Union[LeaveCallback, InviteCallback]) -> bool:
        event = await get_event_by_team(callback_data.team)
        return event.status != EventStatus.CANCELED and event.status != EventStatus.CONDUCTED
