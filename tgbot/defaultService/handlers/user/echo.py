from aiogram.types import Message

from .router import router


@router.message()
async def echo(message: Message):
    await message.answer(message.text)
