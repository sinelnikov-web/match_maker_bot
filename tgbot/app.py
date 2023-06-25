import os
import sys

sys.path.append(os.path.join(os.getcwd(), 'tgbot'))
sys.path.append(os.getcwd())

import django


def setup_django():
    os.environ.setdefault("DJANGO_SETTINGS_MODULE", "match_maker_bot.settings")
    django.setup()


setup_django()

import asyncio
import logging
from typing import List
from aiogram import Router
from tgbot.loader import bot, dp
from settings import UserRegisterMiddleware
from .matchMakingService import match_making_service
from .defaultService import default_router

logging.basicConfig(level=logging.INFO)

ROUTERS: List[Router] = [
    match_making_service,
    default_router,
]


async def main():

    for router in ROUTERS:
        dp.include_routers(router)

    dp.message.outer_middleware.register(UserRegisterMiddleware())
    dp.callback_query.outer_middleware.register(UserRegisterMiddleware())

    await bot.delete_webhook(drop_pending_updates=True)
    await dp.start_polling(bot)


if __name__ == "__main__":
    asyncio.run(main())
