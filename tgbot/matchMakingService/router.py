from aiogram import Router
from .handlers import user_router

module_router = Router()

module_router.include_routers(user_router)
