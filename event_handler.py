#!/usr/bin/env python3

from requests import post, get
from json import load, dumps, dump
from os.path import exists
from time import sleep

from aiogram import Bot, types
from aiogram.dispatcher import Dispatcher
from aiogram.utils import executor
from aiogram.types import ReplyKeyboardRemove, ReplyKeyboardMarkup, KeyboardButton
from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton

from TKN_reader import token_get


TOKEN = token_get()
URL = f'https://api.telegram.org/bot{TOKEN}/'

bot = Bot(token=TOKEN, parse_mode="HTML")
dp = Dispatcher(bot)


def history_record(req, file='json/history.json'):
    with open(file, 'a') as f:
        dump(req, f, indent=4, ensure_ascii=False)
        f.write('\n')
    return True


def send_message(chat_id, text):
    keyboard =  []
    answer = {
        'chat_id': chat_id,
        'text': text,
        'parse_mode': 'HTML',
    }
    req = post(f'{URL}sendMessage', json=answer)

    return req.json()


@dp.message_handler(commands=['start'])
async def start(message: types.Message):
    start_message_text = '''🍀<b>Вас приветствует GreenWayShop</b>🍀
    
Мы с заботой относимся к защите окружающей среды, поэтому каждый наш продукт разработан по принципу безопасности и экологичности

Здесь вы можете найти всё что вам нужно для:

🏡 <b>Дома</b>
🚗 <b>Машины</b>
✨ <b>Ухода за собой</b>
🐶 <b>Ваших любимых питомцев</b>.

У нас присутствует <b>бонусная система</b> Приводите друзей - получайте подарки, и предложения специально для вас😊'''

    await bot.send_message(message.from_user.id, start_message_text)


def json_get(file_name):
    path_to_file = f'json/{file_name}.json'
    if not exists(path_to_file):
        return 'File is not found'
    with open(path_to_file) as f:
        return str(load(f))


# def main():
#     if request.method != 'POST':
#         return 'None'
#     try:
#         req = request.get_json()  # Get message info from request to Telegram chat
#         history_record(req)  # record request to file json/history.json
#         message = req['message']
#         message_text = message['text']
#         send_message(message['chat']['id'], message['chat']['id'])
#         if '/start' in message_text:
#             start(message)
#         return jsonify(req)
#     except UnicodeEncodeError as e:
#         print(e)
#         return 'None'


if __name__ == '__main__':
    executor.start_polling(dp)
