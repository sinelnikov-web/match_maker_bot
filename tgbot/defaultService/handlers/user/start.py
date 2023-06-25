from aiogram import F
from aiogram.filters import Command, CommandObject
from aiogram.types import Message

from dto import UserDTO
from shared.utils.validate_uuid import is_valid_uuid
from tgbot.matchMakingService.lib.event_text import create_event_text
from tgbot.shared.db.api import get_event_by_team
from tgbot.shared.keyboards import KeyboardManager, Keyboards
from tgbot.shared.keyboards.invite_user import create_invite_keyboard, cancel_invite_keyboard
from .router import router
from ...usecases.authenticate import authenticate_request, register_user


@router.message(Command('start'))
async def start(message: Message, user: UserDTO, command: CommandObject):
    if user.phone is None:
        await authenticate_request(message, user)
    else:
        kb = KeyboardManager.get(Keyboards.MAIN_KEYBOARD).generate_keyboard()
        if command.args is not None and is_valid_uuid(command.args):
            event = await get_event_by_team(command.args)
            if event is not None:
                await message.answer(
                    await create_event_text(event, ['show_teams']),
                    reply_markup=create_invite_keyboard(command.args) if not event.has_participant(
                        user.id) else cancel_invite_keyboard(command.args)
                )
            else:
                await message.answer("Мероприятие не найдено!", reply_markup=kb)
        else:
            await message.answer('Здравствуйте, что Вы хотели бы сделать?', reply_markup=kb)


@router.message(F.contact.phone_number)
async def register(message: Message, user: UserDTO):
    await register_user(message, user, message.contact.phone_number)
