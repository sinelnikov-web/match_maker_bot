from aiogram.types import Message

from dto import UserDTO
from telegram.services import update_user
from tgbot.shared.keyboards import KeyboardManager, Keyboards


async def authenticate_request(msg: Message, user: UserDTO):
    await msg.answer(
        'Нажмите кнопку "зарегистрироваться для регистрации',
        reply_markup=KeyboardManager.get(Keyboards.AUTH_KEYBOARD).generate_keyboard(user.language)
    )


async def register_user(msg: Message, user: UserDTO, contact: str):
    user.phone = contact
    await update_user(user.id, user)
    await msg.answer(
        "Вы успешно зарегистрированы",
        reply_markup=KeyboardManager.get(Keyboards.MAIN_KEYBOARD).generate_keyboard(user.language)
    )
