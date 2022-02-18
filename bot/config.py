from aiogram import Bot, types
from aiogram.dispatcher import Dispatcher

from TKN_reader import token_get

TOKEN = token_get()

bot = Bot(token=TOKEN, parse_mode="HTML")
dp = Dispatcher(bot)

URL = f'https://api.telegram.org/bot{TOKEN}/'