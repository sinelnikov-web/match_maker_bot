import os

from dotenv import load_dotenv
load_dotenv(os.path.join(os.getcwd(), 'tgbot', '.env'))

BOT_TOKEN = os.getenv('BOT_TOKEN')
REDIS_IP = os.getenv('REDIS_IP')
