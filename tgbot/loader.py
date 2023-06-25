import aioredis
from aiogram import Bot, Dispatcher
from aiogram.enums import ParseMode
from aiogram.fsm.storage.redis import RedisStorage

from tgbot.settings.env import REDIS_IP, BOT_TOKEN

storage = RedisStorage(redis=aioredis.from_url(f"redis://{REDIS_IP}:6379",  db=1))
bot = Bot(token=BOT_TOKEN, parse_mode=ParseMode.HTML)
dp = Dispatcher(storage=storage)
