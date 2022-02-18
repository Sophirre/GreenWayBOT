from aiogram.types import ReplyKeyboardMarkup, KeyboardButton
from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton

from bot.admin import admin_check


def menu_kb(message):
    b1 = KeyboardButton('🛍Каталог')
    b2 = KeyboardButton('⭐Избранное')
    b3 = KeyboardButton('📃История заказов')
    b4 = KeyboardButton('⚙Настройки')
    b5 = KeyboardButton('📅Новости')
    b6 = KeyboardButton('🛒Корзина')
    b7 = KeyboardButton('🔑Админ-панель')

    kb_client = ReplyKeyboardMarkup(resize_keyboard=True)
    if admin_check(message):
        kb_client.row(b1, b2, b3).row(b4, b5, b6).add(b7)
    else:
        kb_client.row(b1, b2, b3).row(b4, b5, b6)
    callback_client = InlineKeyboardMarkup(row_width=1)

    ref = InlineKeyboardButton(text='Реферальная система', callback_data='ref')
    history = InlineKeyboardButton(text='История заказов', callback_data='history')
    about = InlineKeyboardButton(text='О нас', callback_data='about')

    callback_client.add(ref, history, about)

    return {'kb': kb_client,
            'callback': callback_client}


def catalog():
    b1 = KeyboardButton('🏡Меню')
    b2 = KeyboardButton('🛒Корзина')
    b3 = KeyboardButton('⭐Избранное')

    kb_client = ReplyKeyboardMarkup(resize_keyboard=True)
    kb_client.row(b1, b2, b3)

    callback_client = InlineKeyboardMarkup(row_width=1)

    popular = InlineKeyboardButton(text='Популярное', callback_data='popular')
    textile = InlineKeyboardButton(text='Текстиль', callback_data='textile')
    house = InlineKeyboardButton(text='Дом', callback_data='house')
    special = InlineKeyboardButton(text='Акции', callback_data='special')
    back = InlineKeyboardButton(text='◀Назад', callback_data='back')
    callback_client.add(popular, textile, house, special, back)
    return {'kb': kb_client,
            'callback': callback_client}


def subsections_cb(code, btn_names: list):
    callback_client = InlineKeyboardMarkup(row_width=1)
    for btn in btn_names:
        btn = btn[:-5]
        btn = InlineKeyboardButton(text=btn,
                                   callback_data=code + btn)
        callback_client.add(btn)
    return callback_client


def admin_kb():

    b1 = KeyboardButton('🏡Меню')
    b2 = KeyboardButton('Активные заказы')
    kb_client = ReplyKeyboardMarkup(resize_keyboard=True)

    kb_client.add(b1, b2)
    return kb_client
